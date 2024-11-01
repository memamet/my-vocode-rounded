<a href="https://rounded.com">
  <img alt="Donny, Rounded's AI Assistant" src="public/donny_logo.avif">
  <h1 align="center">Meet Donny – Rounded's AI Assistant</h1>
</a>

<p align="center">
  Donny is your guide to everything Rounded! Built with Vocode, Next.js, and FastAPI, Donny is here to provide seamless, interactive insights into the world of Rounded.
</p>

## TL;DR: Docker Quickstart

Get Donny up and running in two simple steps:

### 1. **Create your `.env` file:**

Create a `.env` file in your project folder. This file will store the necessary environment variables. To do this, you will copy the .env.sample file at the root of the project – replace placeholders with your actual API keys and settings.

### 2. **Run locally:**

With your `.env` file ready, execute the following command to start Donny’s service.

```bash
npm install
npm run dev
```

After running the command, Donny will be available at [http://localhost:3000](http://localhost:3000).

### 3. **Run the Docker container:** (WIP)

With your `.env` file ready, execute the following command to build the Docker image.

```bash
docker build --build-arg BUILD_DATE=$(date -u +'%Y-%m-%dT%H:%M:%SZ') \
             --build-arg VCS_REF=$(git rev-parse --short HEAD) \
 --build-arg VERSION=0.1.111 \
 -t vocode/vocode:0.1.111 .
```

Then, run the Docker container with the following command:

```bash
docker run --env-file .env -p 3000:3000 vocode/vocode:0.1.111
```

This will pull the Docker image and run both frontend and backend services.

After running the command, Donny will be available at [http://localhost:3000](http://localhost:3000).

## Introduction

This project combines Next.js for the frontend and FastAPI for the backend to create Donny, Rounded's AI assistant. It uses Vocode's Python library to deliver seamless AI-powered voice interactions, making Donny a knowledgeable companion for all things Rounded.

## Features

- **Quick Setup**: Get Donny running locally with minimal setup.
- **Hybrid Stack**: Combines Next.js (frontend) and FastAPI (backend).
- **AI-Powered Voice Interaction**: Uses Vocode for real-time conversation handling with AI.
- **Customizable**: Tailor prompts, messages, and configurations to match Rounded’s evolving needs.

## How It Works

Donny’s backend, built with FastAPI, integrates with the Vocode library to connect to AI services like OpenAI, Azure Speech, and Deepgram. These connections enable real-time, AI-driven conversation with Donny, allowing it to provide answers and information about Rounded and its products.

## Prerequisites

- [Node.js and npm](https://nodejs.org/en/download/)
- [Python 3.9+](https://www.python.org/downloads/)
- [Poetry](https://python-poetry.org/docs/#installation)
- [OpenSSL 1.1.1](https://learn.microsoft.com/en-us/azure/ai-services/speech-service/quickstarts/setup-platform?tabs=linux%2Cubuntu%2Cdotnetcli%2Cdotnet%2Cjre%2Cmaven%2Cnodejs%2Cmac%2Cpypi&pivots=programming-language-python)
- [FFmpeg](https://ffmpeg.org/download.html)

## License

This project is licensed under the [MIT License](./LICENSE).

## Contact

For questions, feedback, or collaboration, visit our [GitHub](https://github.com/memamet/my-vocode-rounded)
