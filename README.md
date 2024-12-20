Changi Airport Chatbot
Project Overview
The Changi Airport Chatbot is a Retrieval-Augmented Generation (RAG) application that leverages a Large Language Model (LLM) and a vector database to answer user queries based on information from the Changi Airport and Jewel Changi Airport websites. This chatbot combines web scraping, embeddings, and API deployment to provide accurate and contextual answers.

Features
Data Scraping: Extracts website content and processes it for querying.
Vector Embeddings: Converts text into vector representations using OpenAI embeddings.
Vector Database: Stores embeddings in Pinecone for efficient retrieval.
Chatbot Framework: Uses LangChain for integrating retrieval and response generation.
REST API: Accessible via FastAPI for seamless integration.
Installation and Setup
Prerequisites
Python: Version 3.8 or higher.
API Keys:
OpenAI API Key
Pinecone API Key
Environment Setup:
Install required dependencies using the requirements.txt file.
Steps to Run Locally
Clone the Repository:

bash
Copy code
git clone https://github.com/your-username/changi-airport-chatbot.git
cd changi-airport-chatbot
Set Up Virtual Environment:

bash
Copy code
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\\Scripts\\activate
Install Dependencies:

bash
Copy code
pip install -r requirements.txt
Set Up Environment Variables:

Create a .env file in the project root and add the following:
env
Copy code
OPENAI_API_KEY=your_openai_api_key
PINECONE_API_KEY=your_pinecone_api_key
PINECONE_ENV=your_pinecone_environment
Run the Application:

bash
Copy code
uvicorn main:app --reload --host 0.0.0.0 --port 8000
Access the API:

Base URL: http://127.0.0.1:8000
Use tools like Postman or curl to query the API.
API Usage
Endpoint: /query
Method: POST

Request Body:

json
Copy code
{
  "query": "What are the attractions at Jewel Changi Airport?"
}
Response:

json
Copy code
{
  "answer": "Jewel Changi Airport features attractions like the Rain Vortex, Canopy Park, and numerous dining and shopping options."
}
Deployment
Cloud Deployment (Optional)
You can deploy the application to platforms like AWS, GCP, or Azure using Docker.

Example Docker Setup:
Create a Dockerfile:

dockerfile
Copy code
FROM python:3.9-slim
WORKDIR /app
COPY . ./
RUN pip install -r requirements.txt
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
Build and Run:

bash
Copy code
docker build -t changi-chatbot .
docker run -d -p 8000:8000 changi-chatbot
Deploy the container to your preferred cloud platform.

Example Queries
Query: "What is the Rain Vortex?"

Response: "The Rain Vortex is the world's tallest indoor waterfall, located in Jewel Changi Airport. It is surrounded by lush greenery and is a popular attraction."
Query: "What dining options are available at Changi Airport?"

Response: "Changi Airport offers a wide variety of dining options, including international cuisines, fast food, and fine dining."
Future Enhancements
Add multi-language support for broader accessibility.
Improve web scraping to dynamically adapt to website changes.
Integrate additional features like flight status queries or live updates.

Contributing
Contributions are welcome! Feel free to fork the repository and submit a pull request.

