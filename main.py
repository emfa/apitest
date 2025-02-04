from typing import Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import apitest
import os

app = FastAPI()


class TestRequest(BaseModel):
    input_file_name: str
    output_file_name: str
    environment: str


@app.get("/")
def read_root():
    return {"Name": "API Test Automation", "Version": "1.0"}


@app.post("/test/")
def run_tests(request: TestRequest):
    try:
        apitest.runtest(
            input_file_name=request.input_file_name,
            output_file_name=request.output_file_name,
            folder_name=request.environment.lower()
        )
        return {
            "status": "success",
            "message": f"Tests executed and results saved to {request.output_file_name}",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@app.get("/testall/")
@app.get("/testall/{region}")
def run_all_tests(region: Optional[str] = None):
    try:
        if region:
            region = region.lower()

        base_dir= "testfiles"
        target_dir = os.path.join(base_dir, region) if region else base_dir

        if not os.path.exists(target_dir) or not os.path.isdir(target_dir):
            raise HTTPException(status_code=404, detail=f"Region {region} not found")
        
        for root, _, files in os.walk(target_dir):
            for file in files:
                output_file = os.path.splitext(file)[0]

                apitest.runtest(
                    input_file_name=file,
                    output_file_name=f"{output_file}.xlsx",
                    folder_name=os.path.basename(root)
                )

        return {
            "status": "success",
            "message": "All tests executed successfully",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))