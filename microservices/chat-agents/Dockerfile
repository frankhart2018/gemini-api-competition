FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ARG GEMINI_API_KEY

CMD python gemini_executor.py --gemini-api-key $GEMINI_API_KEY