# Gemini API Competition

## Time to competition end

<p align="center">
  <img src="http://i.countdownmail.com/3baikt.gif" />
</p>

## StartUp for Frontend

### Software Requirements

node js

#### First navigate to directory /Frontend/gemini-chat-app

cd Frontend/gemini-chat-app

#### Install all dependencies

npm i

Run the development server:

```bash
npm run dev
# or
yarn dev
# or
pnpm dev
# or
bun dev
```

Open [http://localhost:3000](http://localhost:3000) with your browser to see the result.

You can start editing the page by modifying `app/page.tsx`. The page auto-updates as you edit the file.

This project uses [`next/font`](https://nextjs.org/docs/basic-features/font-optimization) to automatically optimize and load Inter, a custom Google Font.

## Deploy on Vercel

The easiest way to deploy your Next.js app is to use the [Vercel Platform](https://vercel.com/new?utm_medium=default-template&filter=next.js&utm_source=create-next-app&utm_campaign=create-next-app-readme) from the creators of Next.js.

Check out our [Next.js deployment documentation](https://nextjs.org/docs/deployment) for more details.

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
