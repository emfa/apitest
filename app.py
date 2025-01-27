from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import apitest

app = FastAPI()

class TestRequest(BaseModel):
    input_file_name: str
    output_file_name: str

@app.get("/")
def read_root():
    return {"Name": "API Test Automation", "Version": "1.0"}

@app.post("/run-tests/")
def run_tests(request: TestRequest):
    try:
        apitest.run(input_file_name=request.input_file_name, output_file_name=request.output_file_name)
        return {"status": "success", "message": f"Tests executed and results saved to {request.output_file_name}"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))