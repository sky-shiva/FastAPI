from pydantic import BaseModel,EmailStr,Field
from typing import List,Dict,Optional,Annotated

class Schema(BaseModel):
    # defining the schema
    name=Annotated[str,Field(max_length=50,title="Name of the patient",examples=["Nitish","Shiva"],description="Enter the valid name")]
    age:int=Field(gt=18,lte=60)
    email:EmailStr
    weight:float
    height:float
    married:Annotated[bool,Field(default=None)]
    problem:Optional[list[str]]=None# list[str] we cannot do this
    contact_details:Dict[str,str]

def insert_patient_data(patient:Schema):
    print(patient.name)
    print(patient.age)
    print(patient.height)
    print(patient.weight)
    print(patient.problem)
    print(patient.married)
    print(patient.contact_details)
    print(patient.email)
    print("done")

patient_info={'name':"skyss",
              "age":'19',
              "email":"abc@gmail.com",
              "weight":78.2,
              "height":1.57,
              "married":1,
              "contact_details":{"email":"abc@gmail.com","phone":"9032399527"}
            }   

patient1=Schema(**patient_info)

insert_patient_data(patient1)