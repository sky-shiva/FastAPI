from fastapi import FastAPI,Path,HTTPException
from typing import Optional
import json
app = FastAPI()


def load_data():
    with open("patients.json",'r') as f:
        data=json.load(f)
    return data
        
@app.get("/data/{idp}")
def get_patient_data(idp:Optional[str]=None):
    data=load_data()
    if idp is None:
        return data
    if idp not in data:
        raise HTTPException(status_code=404,detail="Patient not found with this details")
    return data[idp]
    