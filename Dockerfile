FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt-get update && apt-get install -y wget && \
    wget https://storage.yandexcloud.net/natasha-navec/packs/navec_hudlit_v1_12B_500K_300d_100q.tar && \
    mkdir -p /app/models && \
    tar -xvf navec_hudlit_v1_12B_500K_300d_100q.tar -C /app/models && \
    rm navec_hudlit_v1_12B_500K_300d_100q.tar

ENV NAVEC_MODEL_PATH=/app/models/navec_hudlit_v1_12B_500K_300d_100q

RUN chmod +x ./mig.py
RUN chmod +x ./main.py

CMD ["sh", "-c", "python mig.py && python main.py"]