from fastapi import FastAPI, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from chatbot import Chatbot, UploadFiles  
app = FastAPI()

# Initialize instances of UploadFiles and Chatbot
upload_file = UploadFiles()
chatbot = Chatbot()

app.mount("/static", StaticFiles(directory="static"), name="static")

class QueryModel(BaseModel):
    query: str

@app.post("/upload_file")
async def upload_file_and_process(file: UploadFile = File(...)):
    try:
        file_content = await file.read()  # Read the file content
        upload_file.text_spliter(file_content.decode('utf-8'))  # Process the file
        return {"response": "File processed successfully"}  # Return the response to the client
    except Exception as e:
        return {"error": str(e)}  # Return any errors encountered during processing

@app.post("/get_query_result")
async def get_chatbot_response(query_model: QueryModel):
    try:
        query = query_model.query
        response = chatbot.generate_reply(query, upload_file)  # Generate a reply from the chatbot
        return {"response": response}  # Return the response to the client
    except Exception as e:
        return {"error": str(e)}  # Return any errors encountered during processing

# Run the FastAPI app with Uvicorn
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="localhost", port=8000)
