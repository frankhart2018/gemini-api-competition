FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

# Required to install pylib which is hosted in GitHub
RUN apt-get update && apt-get install -y git

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG GEMINI_API_KEY
ARG LOGGER_URL
ARG LOGGER_TOKEN

ENV LOGGER_URL=$LOGGER_URL
ENV LOGGER_TOKEN=$LOGGER_TOKEN

CMD python gemini_executor.py --gemini-api-key $GEMINI_API_KEY