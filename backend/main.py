from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from simplifier import LegalSimplifier
import uvicorn
import subprocess
import os

def kill_port_process(port):
    """Automatically find and kill any process using the specified port."""
    try:
        # Find PIDs using the port on Windows
        result = subprocess.run(
            ["netstat", "-ano"], 
            capture_output=True, 
            text=True, 
            check=False
        )
        if result.returncode != 0:
            return

        lines = result.stdout.splitlines()
        pids_to_kill = set()
        for line in lines:
            # Look for lines containing the port and LISTENING status
            if f":{port}" in line and "LISTENING" in line:
                parts = line.split()
                if len(parts) > 0:
                    pid = parts[-1]
                    # Don't kill the current process
                    if pid != str(os.getpid()):
                        pids_to_kill.add(pid)
        
        for pid in pids_to_kill:
            print(f"Cleaning up port {port}: Terminating process {pid}...")
            subprocess.run(["taskkill", "/F", "/PID", pid], capture_output=True)
            
    except Exception as e:
        # Silently fail if something goes wrong with cleanup
        pass

app = FastAPI(title="LegalEase API", description="Simplifying legal text using NLP")

# Enable CORS for frontend interaction
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize the simplifier
simplifier = LegalSimplifier()

class SimplificationRequest(BaseModel):
    text: str

class SimplificationResponse(BaseModel):
    original_text: str
    simplified_text: str

@app.post("/simplify", response_model=SimplificationResponse)
@app.post("/_/backend/simplify", response_model=SimplificationResponse)
async def simplify_text(request: SimplificationRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Text cannot be empty")
    
    try:
        simplified = simplifier.simplify(request.text)
        return {
            "original_text": request.text,
            "simplified_text": simplified
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
@app.get("/_/backend")
@app.get("/_/backend/")
async def root():
    return {"message": "LegalEase API is running"}

if __name__ == "__main__":
    kill_port_process(8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
