from langchain.vectorstores import FAISS
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
import google.generativeai as genai

MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
FAISS_INDEX = "XYZ"
GEMINI_KEY = "your_gemini_key_here"
class UploadFiles:
    def __init__(self):
        self.docs = []
        self.retriever = None

    def upload_text(self, file_content):
        try:
            splitter = CharacterTextSplitter()
            self.docs.extend(splitter.split_text(file_content))
        except Exception as e:
            print(f"Error processing text content: {e}")

    def text_spliter(self, file_content):
        self.upload_text(file_content)
        faiss_index = FAISS.from_documents(self.docs, HuggingFaceEmbeddings(model_name=MODEL_NAME))
        faiss_index.save_local(FAISS_INDEX)
        db = FAISS.load_local(FAISS_INDEX, HuggingFaceEmbeddings(model_name=MODEL_NAME))
        self.retriever = db.as_retriever()
        self.retriever.search_kwargs["distance_metric"] = 'cos'
        self.retriever.search_kwargs["fetch_k"] = 100
        self.retriever.search_kwargs["maximal_marginal_relevance"] = True
        self.retriever.search_kwargs["k"] = 20

    def retrieve_documents(self, query):
        if not self.retriever:
            raise ValueError("Retriever not initialized. Please run text_spliter first.")
        results = self.retriever.get_relevant_documents(query)
        return results

class Chatbot:
    def __init__(self):
        genai.configure(api_key=GEMINI_KEY)
        self.generation_config = {
            "temperature": 0.5,
            "top_p": 1,
            "top_k": 1,
            "max_output_tokens": 8192,
        }
        self.safety_settings = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]
        self.model = genai.GenerativeModel(
            model_name="gemini-1.5-pro-latest",
            generation_config=self.generation_config,
            safety_settings=self.safety_settings
        )

    def chat_bot(self, query, related_docs):
        prompt = f"""
        You are a Question and Answer chat bot. Your task is to follow the steps below:
        You will be given a user query: {query}
        You have to develop an answer based on the results given by the Vector Database: {related_docs}
        <Note: please provide a relevant answer to the given query>
        """
        convo = self.model.start_chat()
        response = convo.send_message(prompt)
        return response["text"]

    def generate_reply(self, query, retriever):
        related_docs = retriever.retrieve_documents(query)
        print('Related docs:', related_docs)
        reply = self.chat_bot(query, related_docs)
        return reply
