from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os
from pymongo import MongoClient
from bson.objectid import ObjectId
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')
DATABASE_NAME = os.getenv('DATABASE_NAME')
MONGO_USERNAME = os.getenv('MONGO_USERNAME')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

client = MongoClient(MONGO_URI, username=MONGO_USERNAME, password=MONGO_PASSWORD)
db = client[DATABASE_NAME]

scenarios_collection = db['scenario']
jobs_collection = db['job']
actions_collection = db['action']

scenarios_collection.drop()
jobs_collection.drop()
actions_collection.drop()

actions = [
    {
        "_id": ObjectId("6640ae3412f4c109e563dd60"),
        "name": "Get Balance",
        "type": 1,
        "input": {
            "token": {
                "value": None,
                "type": "text"
            }
        },
        "output": ["balance"],
        "additional_params": {
            "url": "http://bank:30004/api/v1/wallet",
            "method": "GET"
        }
    },
    {
        "_id": ObjectId("6640b20ea992c6f3eb368046"),
        "name": "Transfer Money",
        "type": 1,
        "input": {
            "token": {
                "value": None,
                "type": "text"
            },
            "to": {
                "value": None,
                "type": "phone-number"
            },
            "amount": {
                "value": None,
                "type": "amount"
            }
        },
        "output": [],
        "additional_params": {
            "url": "http://bank:30004/api/v1/transfer",
            "method": "POST"
        }
    }
]

actions_collection.insert_many(actions)

jobs = [
    {
        "_id": ObjectId("6640d74b84049cbd5e07a70c"),
        "name": "Transfer Money",
        "actions": [
            {
                "id": ObjectId("6640b20ea992c6f3eb368046"),
                "output": ["id", "receiver_id"]
            }
        ],
        "output": {
            "ask": {
                "message": "Provide arguments",
                "type": 1,
                "variable": None
            },
            "onsuccess": {
                "message": "Successful transfer money",
                "type": 2,
                "variable": None
            },
            "onfailure": {
                "message": "Failed transfer money",
                "type": 3,
                "variable": None
            }
        }
    },
    {
    "_id": ObjectId("6640ae3412f4c109e563dd60"),
    "name": "Get Balance",
    "actions": [
      {
        "id": ObjectId("6640ae3412f4c109e563dd60"),
        "output": [
          "balance"
        ]
      }
    ],
    "output": {
        "ask": {
        "message": "Not enough arguments",
        "type": 1,
        "variable": None
        },
        "onsuccess": {
        "message": "Your current balance is {{.balance}}.",
        "type": 2,
        "variable": {
            "balance": {
                "type": "text",
                "value": "null"
            }
        }
        },
        "onfailure": {
        "message": "Failed to get Balance",
        "type": 3,
        "variable": None
        }
    }
  }
]

jobs_collection.insert_many(jobs)

scenarios = [
    {
        "name": "Get Balance",
        "examples": [
            {"text": "хочу узнать баланс"},
            {"text": "какой у меня баланс"},
            {"text": "показать баланс"}
        ],
        "type": 1,
        "root_job_id": ObjectId("6640ae3412f4c109e563dd60"),
        "job_sequence": {},
        "input": {
            "token": {
                "value": None,
                "type": "text"
            }
        },
        "output": ["balance"],
        "additional_params": {
            "url": "http://bank:30004/api/v1/wallet",
            "method": "GET"
        }
    },
    {
        "name": "Transfer Money",
        "examples": [
            {"text": "хочу перевести деньги"},
            {"text": "отправить деньги"},
            {"text": "сделать перевод"}
        ],
        "type": 1,
        "root_job_id": ObjectId("6640d74b84049cbd5e07a70c"),
        "job_sequence": {},
        "input": {
            "token": {
                "value": None,
                "type": "text"
            },
            "to": {
                "value": None,
                "type": "text"
            },
            "amount": {
                "value": None,
                "type": "number"
            }
        },
        "output": [],
        "additional_params": {
            "url": "http://bank:30004/api/v1/transfer",
            "method": "POST"
        }
    }
]

scenarios_collection.insert_many(scenarios)

print("Data inserted successfully!")
