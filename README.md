# AI Chatbot with Django and OpenAI

This project implements an AI chatbot with user authentication and chat history using Django REST Framework and OpenAI's GPT API.

## Features

- User registration and login with JWT authentication
- Secure password hashing
- Chat with AI using OpenAI's GPT API
- Chat history storage and retrieval
- RESTful API endpoints

## Setup Instructions

### Prerequisites

- Python 3.8+
- pip

### Installation

1. Clone the repository:
\`\`\`bash
https://github.com/Shaiksha9741/Ai-chatbot.git
cd ai-chatbot
\`\`\`

2. Create a virtual environment and activate it:
\`\`\`bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
\`\`\`

3. Install dependencies:
\`\`\`bash
pip install -r requirements.txt
\`\`\`

4. Set up environment variables:
Create a `.env` file in the project root with the following:
\`\`\`
SECRET_KEY=your_django_secret_key
DEBUG=True
OPENAI_API_KEY=your_openai_api_key
\`\`\`

5. Run migrations:
\`\`\`bash
python manage.py migrate
\`\`\`

6. Start the development server:
\`\`\`bash
python manage.py runserver
\`\`\`

The API will be available at `http://localhost:8000/api/`.

## API Documentation

### Authentication Endpoints

#### Register a new user
- **URL**: `/api/register/`
- **Method**: `POST`
- **Request Body**:
  \`\`\`json
  {
    "username": "testuser",
    "password": "securepassword123",
    "email": "user@example.com"
  }
  \`\`\`
- **Response**: 
  \`\`\`json
  {
    "id": 1,
    "username": "testuser",
    "email": "user@example.com"
  }
  \`\`\`

#### Login
- **URL**: `/api/login/`
- **Method**: `POST`
- **Request Body**:
  \`\`\`json
  {
    "username": "testuser",
    "password": "securepassword123"
  }
  \`\`\`
- **Response**: 
  \`\`\`json
  {
    "token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
  }
  \`\`\`

### Chat Endpoints

#### Send a message to the chatbot
- **URL**: `/api/chat/`
- **Method**: `POST`
- **Headers**: `Authorization: Bearer <token>`
- **Request Body**:
  \`\`\`json
  {
    "message": "Hello, how are you today?"
  }
  \`\`\`
- **Response**: 
  \`\`\`json
  {
    "id": 1,
    "user_message": "Hello, how are you today?",
    "bot_response": "I'm doing well, thank you for asking! How can I assist you today?",
    "timestamp": "2023-06-04T12:34:56.789Z"
  }
  \`\`\`

#### Get chat history
- **URL**: `/api/chat/history/`
- **Method**: `GET`
- **Headers**: `Authorization: Bearer <token>`
- **Response**: 
  \`\`\`json
  [
    {
      "id": 1,
      "user_message": "Hello, how are you today?",
      "bot_response": "I'm doing well, thank you for asking! How can I assist you today?",
      "timestamp": "2023-06-04T12:34:56.789Z"
    },
    {
      "id": 2,
      "user_message": "What's the weather like?",
      "bot_response": "I don't have access to real-time weather data. You might want to check a weather service or app for that information.",
      "timestamp": "2023-06-04T12:35:30.123Z"
    }
  ]
  \`\`\`

## Deployment

### Using Docker

1. Build the Docker image:
\`\`\`bash
docker build -t ai-chatbot .
\`\`\`

2. Run the container:
\`\`\`bash
docker run -p 8000:8000 -e SECRET_KEY=your_secret_key -e OPENAI_API_KEY=your_openai_api_key ai-chatbot
\`\`\`

The API will be available at `http://localhost:8000/api/`.
