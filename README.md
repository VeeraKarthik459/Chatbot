# Chatbot
Sure, here's a README file explaining the code:

# ChatBot with Vector Database

This project demonstrates how to build a chatbot using the Google Generative AI (Gemini) model and a vector database for retrieving relevant information from a given text corpus. The code is written in Python and uses the following libraries:

- `langchain` for text processing and vector retrieval
- `faiss` for efficient vector similarity search
- `google.generativeai` for interacting with the Gemini model

## Prerequisites

Before running the code, make sure you have the following:

1. Python 3.7 or higher installed
2. Google Cloud project with the Generative AI API enabled
3. A Gemini API key (replace `"your_gemini_key_here"` in the code with your actual key)

## Installation

1. Clone the repository or copy the provided code.
2. Install the required Python packages by running:

```
pip install langchain google-generativeai-python faiss
```

## Usage

1. Import the necessary classes and functions from the provided code.
2. Create an instance of the `UploadFiles` class and call the `upload_text` method to load your text corpus.
3. Call the `text_spliter` method to split the text into smaller chunks and create a vector database.
4. Create an instance of the `Chatbot` class.
5. Call the `generate_reply` method with a user query and the `retriever` object from the `UploadFiles` instance.

Example:

```python
# Load text corpus
uploader = UploadFiles()
uploader.upload_text("Your text corpus goes here.")
uploader.text_spliter("")  # Pass an empty string to create the vector database

# Create a chatbot instance
chatbot = Chatbot()

# Generate a reply to a user query
#query should be realted to docs which you have given in the start
query = "What is the meaning of life?"
reply = chatbot.generate_reply(query, uploader.retriever)
print(reply)
```

## Configuration

The code includes the following configurable parameters:

- `MODEL_NAME`: The name of the Hugging Face model used for text embeddings (default: `"sentence-transformers/all-MiniLM-L6-v2"`).
- `FAISS_INDEX`: The file name for storing and loading the FAISS index (default: `"XYZ"`).
- `GEMINI_KEY`: Your Gemini API key (replace `"your_gemini_key_here"` with your actual key).
- `generation_config`: Configuration for the Gemini model, including temperature, top-p, top-k, and max output tokens.
- `safety_settings`: Safety settings for the Gemini model, specifying harm categories and thresholds.

Feel free to modify these parameters according to your requirements.

## License

This project is licensed under the [MIT License](LICENSE). 
