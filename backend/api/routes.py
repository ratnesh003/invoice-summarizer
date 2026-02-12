from fastapi import APIRouter, UploadFile, File, HTTPException
from fastapi.responses import FileResponse, PlainTextResponse
import shutil
import os
import json
import uuid
from datetime import datetime
from typing import List, Dict
from ..core.processor import process_file_content

router = APIRouter()

DATA_DIR = "backend/data"
UPLOAD_DIR = os.path.join(DATA_DIR, "uploads")
OUTPUT_DIR = os.path.join(DATA_DIR, "outputs")
ERROR_DIR = os.path.join(DATA_DIR, "errors")
HISTORY_FILE = os.path.join(DATA_DIR, "history.json")

# Ensure directories exist
for directory in [UPLOAD_DIR, OUTPUT_DIR, ERROR_DIR]:
    os.makedirs(directory, exist_ok=True)

# Initialize history file if not exists
if not os.path.exists(HISTORY_FILE):
    with open(HISTORY_FILE, "w") as f:
        json.dump([], f)

def load_history() -> List[Dict]:
    try:
        with open(HISTORY_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_history(history: List[Dict]):
    with open(HISTORY_FILE, "w") as f:
        json.dump(history, f, indent=4)

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    submission_id = str(uuid.uuid4())
    timestamp = datetime.now().isoformat()
    processed_files = []
    
    for file in files:
        file_id = str(uuid.uuid4())
        
        # Save uploaded file
        file_path = os.path.join(UPLOAD_DIR, f"{file_id}_{file.filename}")
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
            
        # Read content for processing
        with open(file_path, "r") as f:
            content = f.read()
            
        # Process content
        output_content, error_content = process_file_content(content)
        
        # Save output and error files
        output_filename = f"{file_id}_output.txt"
        error_filename = f"{file_id}_error.txt"
        
        output_path = os.path.join(OUTPUT_DIR, output_filename)
        error_path = os.path.join(ERROR_DIR, error_filename)
        
        with open(output_path, "w") as f:
            f.write(output_content)
            
        with open(error_path, "w") as f:
            f.write(error_content)
            
        processed_files.append({
            "id": file_id,
            "filename": file.filename,
            "output_file": output_filename,
            "error_file": error_filename
        })
        
    # Create Submission Entry
    submission_entry = {
        "id": submission_id,
        "timestamp": timestamp,
        "files": processed_files
    }
    
    history = load_history()
    # Handle legacy history migration if needed (simple check if items have 'files' key)
    # If legacy items exist and don't match new structure, we might want to filter or migrate them.
    # For this assignment, assuming we can just append new structure and frontend handles valid ones, 
    # or we clear old history. Let's append and filter in frontend or migration here.
    # Simple migration:
    new_history = []
    for item in history:
        if "files" in item:
            new_history.append(item)
    
    new_history.insert(0, submission_entry)
    save_history(new_history)
    
    return submission_entry

@router.delete("/history/{submission_id}")
async def delete_submission(submission_id: str):
    history = load_history()
    submission = next((item for item in history if item["id"] == submission_id), None)
    
    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")
    
    # Delete associated files
    for file_entry in submission["files"]:
        try:
            # Construct paths (assuming patterns from upload)
            # We don't have original upload filename stored fully with ID prefix, but we have output/error
            # Upload file: {id}_{filename} -> we need to find it or store it better.
            # Current storage: UPLOAD_DIR/{file_id}_{filename}
            # We have file_id and filename.
            upload_path = os.path.join(UPLOAD_DIR, f"{file_entry['id']}_{file_entry['filename']}")
            output_path = os.path.join(OUTPUT_DIR, file_entry['output_file'])
            error_path = os.path.join(ERROR_DIR, file_entry['error_file'])
            
            for path in [upload_path, output_path, error_path]:
                if os.path.exists(path):
                    os.remove(path)
        except Exception as e:
            print(f"Error deleting info for file {file_entry['id']}: {e}")
            
    # Remove from history
    new_history = [item for item in history if item["id"] != submission_id]
    save_history(new_history)
    
    return {"message": "Submission deleted successfully"}

@router.get("/history")
async def get_history():
    return load_history()

@router.get("/file/{file_id}/output")
async def get_output_file(file_id: str):
    # Find filename from history or construct it (assuming pattern)
    # Constructing is riskier if we change naming convention, but faster.
    # Let's verify existence.
    files = os.listdir(OUTPUT_DIR)
    target_file = None
    for f in files:
        if f.startswith(file_id):
            target_file = f
            break
            
    if not target_file:
        raise HTTPException(status_code=404, detail="Output file not found")
        
    path = os.path.join(OUTPUT_DIR, target_file)
    with open(path, "r") as f:
        content = f.read()
    return PlainTextResponse(content)

@router.get("/file/{file_id}/error")
async def get_error_file(file_id: str):
    files = os.listdir(ERROR_DIR)
    target_file = None
    for f in files:
        if f.startswith(file_id):
            target_file = f
            break
            
    if not target_file:
        raise HTTPException(status_code=404, detail="Error file not found")
        
    path = os.path.join(ERROR_DIR, target_file)
    with open(path, "r") as f:
        content = f.read()
    return PlainTextResponse(content)

@router.get("/download/{file_id}/{type}")
async def download_file(file_id: str, type: str):
    if type not in ["output", "error"]:
        raise HTTPException(status_code=400, detail="Invalid file type")
        
    directory = OUTPUT_DIR if type == "output" else ERROR_DIR
    files = os.listdir(directory)
    target_file = None
    for f in files:
        if f.startswith(file_id):
            target_file = f
            break
            
    if not target_file:
        raise HTTPException(status_code=404, detail="File not found")
        
    return FileResponse(path=os.path.join(directory, target_file), filename=target_file, media_type='text/plain')
