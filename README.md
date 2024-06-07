# Gemini API Competition

## Time to competition end

<p align="center">
  <img src="http://i.countdownmail.com/3baikt.gif" />
</p>

## Frontend Setup

### Software requirements

Node Js

#### Steps to Follow

1. cd Frontend/gemini-chat-app
2. npm install / npm i (to install dependencies)
3. npm run dev

## Chat Systems Microservice

### Software Requirements

1. Docker
2. Python (>= 3.10)

### Steps to run

1. Run rabbitmq in docker:

```
docker run -d -it --rm --name rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management
```

2. Install all dependencies:

```
pip install -r requirements.txt
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


## MS1

### Software Requirements

1. MongoDB
2. Node Js

### Steps to run
1. cd MS1
2. Either run `mongod --config /opt/homebrew/etc/mongod.conf` to run the MongoDB server locally on your machine( Make sure you have MongoDB compass installed to view the database) or you can use MongoDB Atlas to create a cluster and connect to it. 
3. In case you are using MongoDB Atlas, you need to add username and password of your cluster into .env file in the MS1 directory.
4. npm install
5. npm start