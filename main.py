import grpc
from concurrent import futures
import nlp_pb2
import nlp_pb2_grpc
from pymongo import MongoClient
import stanza
import navec
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import re
from dotenv import load_dotenv
import os
import json
import requests
import tqdm

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
COLLECTION_NAME = os.getenv('COLLECTION_NAME')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')
NAVEC_MODEL_PATH = os.getenv('NAVEC_MODEL_PATH')
EXAMPLES_FILE_PATH = os.getenv('EXAMPLES_FILE_PATH')

navec_model_tar = "navec_hudlit_v1_12B_500K_300d_100q.tar"
response = requests.get("https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar", stream=True)
with open(navec_model_tar, "wb") as f:
    for data in tqdm.tqdm(response.iter_content(chunk_size=4*1024*1024), total=13):
        f.write(data)

navec_model = navec.Navec.load(navec_model_tar)

stanza.download('ru')
nlp = stanza.Pipeline('ru')

client = MongoClient(MONGO_URI, username=MONGO_USERNAME, password=MONGO_PASSWORD)
db = client[DATABASE_NAME]
collection = db[COLLECTION_NAME]

def load_examples_from_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def insert_examples_to_mongo(examples):
    for example in examples:
        existing = collection.find_one({'name': example['name']})
        if existing:
            collection.update_one({'name': example['name']}, {'$set': {'examples': example['examples']}})
        else:
            collection.insert_one(example)

def load_scenarios():
    return list(collection.find())

scenarios = load_scenarios()

def embed_sentence(sentence, model):
    tokens = sentence.lower().split()
    embeddings = [model[token] for token in tokens if token in model]
    if not embeddings:
        return np.zeros(model.pq.dim)
    return np.mean(embeddings, axis=0)

for scenario in scenarios:
    scenario['embeddings'] = [embed_sentence(phrase['text'], navec_model) for phrase in scenario['examples']]

class NLPServiceServicer(nlp_pb2_grpc.NLPServiceServicer):
    def MatchScenario(self, request, context):
        user_prompt = request.user_prompt
        user_embedding = embed_sentence(user_prompt, navec_model)
        
        best_match_score = -1
        best_scenario = None
        
        for scenario in scenarios:
            scenario_embeddings = scenario['embeddings']
            similarities = cosine_similarity([user_embedding], scenario_embeddings)
            max_similarity = np.max(similarities)
            if max_similarity > best_match_score:
                best_match_score = max_similarity
                best_scenario = scenario
        
        response = nlp_pb2.MatchScenarioResponse(
            root_id=str(best_scenario['_id'])
        )
        return response

    def ExtractArguments(self, request, context):
        user_prompt = request.user_prompt
        doc = nlp(user_prompt)
        arguments = {}

        amount_pattern = re.compile(r'\b\d+(\.\d{1,2})?\b')
        amount_match = amount_pattern.search(user_prompt)
        if amount_match:
            arguments["amount"] = amount_match.group(0)
        
        for ent in doc.entities:
            if ent.type == "PERSON":
                arguments["name"] = ent.text
        
        phone_number_pattern = re.compile(r'\b\d{10,11}\b')
        ordinal_pattern = re.compile(r'\b(первый|второй|третий)\b')

        phone_match = phone_number_pattern.search(user_prompt)
        if phone_match:
            arguments["phone_number"] = phone_match.group(0)

        ordinal_match = ordinal_pattern.search(user_prompt)
        if ordinal_match:
            arguments["ordinal"] = ordinal_match.group(0)
        
        currency = "RUB"
        if "доллар" in user_prompt or "долларов" in user_prompt:
            currency = "USD"
        elif "евро" in user_prompt or "евро" in user_prompt:
            currency = "EUR"
        arguments["currency"] = currency
        
        response = nlp_pb2.ExtractArgumentsResponse(arguments=arguments)
        return response
    
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    nlp_pb2_grpc.add_NLPServiceServicer_to_server(NLPServiceServicer(), server)
    server.add_insecure_port('[::]:50052')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()
