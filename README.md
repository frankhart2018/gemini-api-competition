# Gemini API Competition

## Chat Systems Microservice

### Steps to run

1. Run rabbitmq in docker:

```
docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

2. Run `gemini_executor.py` that consumes values from queue and prompts Gemini:

```
python gemini_executor --gemini-api-key <YOUR-GEMINI-KEY>
```

3. Run `send_prompt.py` that is for testing the executor, sends a prompt to queue:

```
python send_prompt.py <PROMPT>
```

At this point you should see the output of Gemini from `gemini_executor.py`.