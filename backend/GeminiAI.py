from google import genai
from google.genai import types

from uuid import uuid4
import mimetypes

API_KEY = "AIzaSyAHD59o8t3l_Hopn5vSnSdNcPzkbuowpa4"
CHAT_MODEL = "gemini-2.0-flash"

['models/chat-bison-001',
 'models/text-bison-001',
 'models/embedding-gecko-001',
 'models/gemini-1.0-pro-vision-latest',
 'models/gemini-pro-vision',
 'models/gemini-1.5-pro-latest',
 'models/gemini-1.5-pro-001',
 'models/gemini-1.5-pro-002',
 'models/gemini-1.5-pro',
 'models/gemini-1.5-flash-latest',
 'models/gemini-1.5-flash-001',
 'models/gemini-1.5-flash-001-tuning',
 'models/gemini-1.5-flash',
 'models/gemini-1.5-flash-002',
 'models/gemini-1.5-flash-8b',
 'models/gemini-1.5-flash-8b-001',
 'models/gemini-1.5-flash-8b-latest',
 'models/gemini-1.5-flash-8b-exp-0827',
 'models/gemini-1.5-flash-8b-exp-0924',
 'models/gemini-2.5-pro-exp-03-25',
 'models/gemini-2.5-pro-preview-03-25',
 'models/gemini-2.5-flash-preview-04-17',
 'models/gemini-2.0-flash-exp',
 'models/gemini-2.0-flash',
 'models/gemini-2.0-flash-001',
 'models/gemini-2.0-flash-exp-image-generation',
 'models/gemini-2.0-flash-lite-001',
 'models/gemini-2.0-flash-lite',
 'models/gemini-2.0-flash-lite-preview-02-05',
 'models/gemini-2.0-flash-lite-preview',
 'models/gemini-2.0-pro-exp',
 'models/gemini-2.0-pro-exp-02-05',
 'models/gemini-exp-1206',
 'models/gemini-2.0-flash-thinking-exp-01-21',
 'models/gemini-2.0-flash-thinking-exp',
 'models/gemini-2.0-flash-thinking-exp-1219',
 'models/learnlm-1.5-pro-experimental',
 'models/learnlm-2.0-flash-experimental',
 'models/gemma-3-1b-it',
 'models/gemma-3-4b-it',
 'models/gemma-3-12b-it',
 'models/gemma-3-27b-it',
 'models/embedding-001',
 'models/text-embedding-004',
 'models/gemini-embedding-exp-03-07',
 'models/gemini-embedding-exp',
 'models/aqa',
 'models/imagen-3.0-generate-002',
 'models/gemini-2.0-flash-live-001']

class AI:
    def __init__(self):
        self.client = genai.Client(api_key=API_KEY)
        self.chat = self.client.chats.create(model=CHAT_MODEL)
        self.uploaded_files = {}
        self.selected_file_ids = []

    def get_list_of_available_models(self):
        # Get the list of available models
        models = self.client.models.list()
        return [model.name for model in models]

    def send_message(self, message):
        response = self.chat.send_message(message)
        return response.text
    
    def __add_AI_file_type(self, file_id, file_data, file_name, file_type):
        # Upload a file to the chat
        AI_File_type = types.Part.from_bytes(data=file_data, mime_type=file_type)
        self.uploaded_files[file_id] = {
            "file_data": file_data,
            "file_name": file_name,
            "file_type": file_type,
            "AI_File_type": AI_File_type
        }
    
    def add_file(self, file_name, file_data, file_type=None):
        # Upload a file to the chat
        file_id = str(uuid4())
        if file_type is None:
            # Get the MIME type of the file
            file_type, _ = mimetypes.guess_type(file_name)
            if file_type is None:
                raise ValueError(f"Could not determine MIME type for file: {file_name} \
                                 Upload the file with a specified MIME type")
        self.__add_AI_file_type(file_id, file_data, file_name, file_type)
        self.selected_file_ids.append(file_id)
        return file_id

    def prompt_on_files(self, prompt):
        required_contents = []
        
        # Add chat history to the required contents
        chat_history = self.chat.get_history()
        required_contents.extend(chat_history)

        # Send a prompt to the chat with the uploaded files
        for file_id in self.selected_file_ids:
            if file_id in self.uploaded_files:
                required_contents.append(self.uploaded_files[file_id]["AI_File_type"])
        required_contents.append(prompt)

        # Call the model with the required contents
        response = self.client.models.generate_content(
            model=CHAT_MODEL,
            contents=required_contents,
        )

        # Add the response to the chat historyif response.candidates and response.candidates[0].content.parts:
        if response.candidates and response.candidates[0].content.parts:
            user_input_ai = types.UserContent(parts = types.Part.from_text(text=prompt))
            self.chat.record_history(user_input=user_input_ai,
                                     model_output=[response.candidates[0].content],
                                     automatic_function_calling_history=[],
                                     is_valid=True)

        return response.candidates[0].content.parts[0].text


# o = AI()
# o.send_message("Hi, My name is ab")
# print(o.send_message("what is my name"))