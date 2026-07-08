from fastapi import FastAPI,Path,HTTPException,Query
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
import json
from typing import Annotated,Literal

app=FastAPI() # created object with name app

class Patient(BaseModel):
    
    patient_id:Annotated[str,Field(...,description="id of the patiend",example="P001")]
    name:Annotated[str,Field(...,description="Name of the patient",example="Shivakumar")]
    city:Annotated[str,Field(...,description="Name of the city",example="Hyderabad")]
    age:Annotated[int,Field(...,description="Age of the patient",example="18",gt=0,lt=120)]
    gender: Annotated[Literal['male', 'female', 'others'], Field(..., description="Gender")]
    height:Annotated[float,Field(...,description="Height of the patient",example="1.8",gt=0)]
    weight:Annotated[float,Field(...,description="Weight of the patient",example="150",gt=0)]
    
    @computed_field
    @property
    def bmi(self)->float:
        bmi=round(self.weight/(self.height**2),2)
        return bmi
    
    
    @computed_field
    @property
    def verdict(self)->str:
        if self.bmi<18.5:
            return 'Underweight'
        elif self.bmi<25:
            return "Normal"
        elif self.bmi<30:
            return "Normal"
        else:
            return "Obese"
    

def load_data():
    with open ('patients.json','r') as f:
        data=json.load(f)
    return data

def save_data(data):
    with open('patients.json','w') as f:
        json.dump(data,f)
    

@app.get("/")
def hello():
    return {"message":"Patient Mangement System API"}

@app.get("/about")
def about():
    return {"message":"Fully functional api to manage your patient records"}

# creating endpoint with name view
@app.get("/view")
def view():
    data=load_data()
    return data
# creating new end point to see specific patient details using path parameters
@app.get("/patient/{patient_id}")
def view_patient(patient_id:str=Path(
    ..., 
    description="ID of the patient in the DB",
    example="P001"
    )
):
    #load all the patients data
    data=load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404,detail="patient not found")

@app.get("/sort")
def sort_patients(sort_by:str=Query(
    ...,
    description="Sort on the basis of height , weight or BMI"),
    order:str=Query('asc',descrition="sort in ascending or descending"
    )
):
    valid_fields=['height','weight','BMI']
    if sort_by not in valid_fields:
        raise HTTPException(status_code=400,detail=f"Invalid Field select from {valid_fields}")
    if order not in ['asc','desc']:
        raise HTTPException(status_code=400,detail="Invalid order select ascending or descending")
    data=load_data()
    
    sort_order=True if order=="desc" else False
    sorted_data=sorted(data.values(),key=lambda x:x.get(sort_by,0),reverse=sort_order)
    return sorted_data
    
    
@app.post("/create")
def create_patient(patient:Patient): # pydantic moodel loading in patient variable
    
    # load existing data
    data=load_data()
    # new patient id is already their?
    if patient.patient_id in data:
        raise HTTPException(status_code=400,detail="patient already exists")
    # new patient add to the database
    data[patient.patient_id]=patient.model_dump(exclude=['patient_id'])
    # save into json
    save_data(data)
    
    return JSONResponse(status_code=201,content={'message':'patient created successfully'})

@app.delete("/delete/{idp}")
def delete_data(idp:str=Path(...,description="Enter the patient id to delete",example="P001")):
    data = load_data()
    if idp not in data:
        raise HTTPException(status_code=404,detail=f"Patient not found with {idp}")
    del data[idp]
    save_data(data)
    return {"message": f"Patient {idp} deleted successfully"}


    
    
    
    