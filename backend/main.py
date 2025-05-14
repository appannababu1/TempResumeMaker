from fastapi import FastAPI
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import uvicorn
import shutil
import os
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse, FileResponse
from typing import List, Annotated # Recommended for newer Python/FastAPI versions
import io
import asyncio
import aiofiles # pip install aiofiles
from fastapi.responses import StreamingResponse


app = FastAPI()

####################################################################################################################
########################################## API ENDPOINTS ###########################################################

@app.get("/")
async def root():
    return JSONResponse(content={"message": "Hello, World!"})

@app.get("/get_call")
async def get_call():
    return JSONResponse(content={"message": "GET call successful!"})

class ClassName(BaseModel):
    arg1 : str
    arg2 : str
@app.post("/post_call")
async def post_call(data : ClassName):
    return JSONResponse(content={"arg1": data.arg1, "arg2": data.arg2})

#####################################################################################################################
########################################## FILE UPLOAD ENDPOINTS ####################################################

# Define a directory to store uploaded files
UPLOAD_DIRECTORY = "./uploaded_files"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True) # Create the directory if it doesn't exist

@app.post("/uploadfile/")
# Modern syntax using Annotated:
async def create_upload_file(file: Annotated[UploadFile, File()]):
# Older syntax (still works):
# async def create_upload_file(file: UploadFile = File(...)):
    """
    Receives a single file upload.
    Saves the file to the UPLOAD_DIRECTORY.
    """
    if not file:
        return JSONResponse(status_code=400, content={"message": "No file sent"})

    # Construct the full path to save the file
    file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)

    try:
        # Open the destination file in binary write mode
        with open(file_location, "wb") as buffer:
            # Read the uploaded file chunk by chunk and write to the destination
            # This is memory-efficient for large files
            while content := await file.read(1024 * 1024): # Read 1MB chunks
                buffer.write(content)
    except Exception as e:
        # Handle potential errors during file writing
        return JSONResponse(
            status_code=500,
            content={"message": f"Could not save file: {e}"}
        )
    finally:
        # Ensure the uploaded file handle is closed
        await file.close()

    return {
        "message": f"Successfully uploaded {file.filename}",
        "filename": file.filename,
        "content_type": file.content_type,
        "saved_location": file_location
    }

@app.post("/uploadfiles/")
# Modern syntax using Annotated:
async def create_upload_files(files: Annotated[List[UploadFile], File()]):
# Older syntax (still works):
# async def create_upload_files(files: List[UploadFile] = File(...)):
    """
    Receives multiple file uploads.
    Saves each file to the UPLOAD_DIRECTORY.
    """
    results = []
    for file in files:
        file_location = os.path.join(UPLOAD_DIRECTORY, file.filename)
        try:
            with open(file_location, "wb") as buffer:
                 while content := await file.read(1024 * 1024): # Read 1MB chunks
                    buffer.write(content)
            results.append({
                "filename": file.filename,
                "content_type": file.content_type,
                "status": "uploaded"
            })
        except Exception as e:
            results.append({
                "filename": file.filename,
                "status": "failed",
                "error": str(e)
            })
        finally:
            # Ensure each file is closed, even if others fail
             await file.close()

    return {"uploaded_files_status": results}

# Optional: Add an endpoint to list uploaded files (for verification)
@app.get("/files/")
async def list_files():
    """Lists files in the upload directory."""
    files = os.listdir(UPLOAD_DIRECTORY)
    return {"uploaded_files": files}

DOWNLOADS_DIR = UPLOAD_DIRECTORY # "./downloadable_files/"

# Create the directory and a sample file for testing
os.makedirs(DOWNLOADS_DIR, exist_ok=True)
sample_file_path = os.path.join(DOWNLOADS_DIR, "my_report.txt")
with open(sample_file_path, "w") as f:
    f.write("This is the content of the downloadable report.\n")
    f.write(f"Generated on: {__import__('datetime').datetime.now()}\n") # Using current time for example

@app.get("/download/file/{filename}")
async def download_file(filename: str):
    """
    Downloads a file from the DOWNLOADS_DIR.

    Args:
        filename (str): The name of the file to download.

    Returns:
        FileResponse: Sends the file to the client.

    Raises:
        HTTPException(404): If the file is not found.
        HTTPException(400): If the filename is potentially insecure.
    """
    # --- SECURITY ---
    # Basic validation to prevent path traversal attacks.
    # You might need more robust validation depending on your use case.
    if ".." in filename or filename.startswith("/") or filename.startswith("\\"):
        raise HTTPException(status_code=400, detail="Invalid filename.")

    file_path = os.path.join(DOWNLOADS_DIR, filename)

    # --- CHECK FILE EXISTENCE ---
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")

    # --- SEND FILE ---
    # FileResponse will infer the media type based on the filename extension
    # and set Content-Disposition to 'attachment' by default.
    return FileResponse(
        path=file_path,
        filename=filename, # This filename is suggested to the browser for saving
        media_type='application/octet-stream' # Optional: Force download as binary stream
        # media_type='text/plain' # Optional: Explicitly set media type if needed
    )

# Example of how to trigger a download with a different suggested name
@app.get("/download/report")
async def download_latest_report():
     # Assume sample_file_path holds the path to the latest report
     if not os.path.isfile(sample_file_path):
        raise HTTPException(status_code=404, detail="Report file not found.")

     return FileResponse(
        path=sample_file_path,
        filename="latest_financial_report.txt", # Suggest a different name
        media_type='text/plain'
    )

# Example 1: Streaming dynamically generated text content
@app.get("/download/stream/generated")
async def download_generated_stream():
    """Streams generated text content."""

    # Generator function (can be async or sync)
    async def generate_content():
        yield "Report Header\n"
        yield "="*20 + "\n"
        for i in range(1, 11):
            yield f"Data line {i}: Value {i*i}\n"
            await asyncio.sleep(0.1) # Simulate some work/delay
        yield "="*20 + "\n"
        yield "Report Footer\n"

    # Define headers, especially Content-Disposition for filename
    headers = {
        'Content-Disposition': 'attachment; filename="generated_report.txt"'
    }

    return StreamingResponse(generate_content(), media_type="text/plain", headers=headers)

# Example 2: Streaming an existing large file (using async iteration)
@app.get("/download/stream/largefile/{filename}")
async def download_large_file_stream(filename: str):
    """Streams an existing large file chunk by chunk asynchronously."""
    # --- SECURITY (same as FileResponse example) ---
    if ".." in filename or filename.startswith("/") or filename.startswith("\\"):
        raise HTTPException(status_code=400, detail="Invalid filename.")

    file_path = os.path.join(DOWNLOADS_DIR, filename)

    # --- CHECK FILE EXISTENCE ---
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail=f"File '{filename}' not found.")

    # --- ASYNC FILE ITERATOR ---
    async def file_iterator(file_path: str, chunk_size: int = 1024*64): # 64KB chunks
        try:
            async with aiofiles.open(file_path, mode="rb") as file:
                while chunk := await file.read(chunk_size):
                    yield chunk
        except FileNotFoundError:
             # This might be redundant if checked before, but good practice
             print(f"Error: File not found during iteration: {file_path}")
             # You might want a different way to signal error from generator
             # Raising exception here might not be caught by FastAPI easily
        except Exception as e:
            print(f"Error reading file chunk: {e}")


    # Determine media type (StreamingResponse doesn't guess)
    media_type = 'application/octet-stream' # Default
    if filename.lower().endswith('.txt'):
        media_type = 'text/plain'
    elif filename.lower().endswith('.pdf'):
        media_type = 'application/pdf'
    # Add more types as needed...

    headers = {
        'Content-Disposition': f'attachment; filename="{filename}"'
    }

    return StreamingResponse(
        file_iterator(file_path),
        media_type=media_type,
        headers=headers
    )


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)