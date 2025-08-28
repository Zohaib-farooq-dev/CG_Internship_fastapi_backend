import json
from fastapi import HTTPException,Path,Query
from fastapi.responses import JSONResponse
from app.models.patients import Patient, PatientUpdate
from app.storage.json_storage import load_data, save_data 


def view():
    data = load_data()
    return data 

def view_patient(patient_id:str = Path(...,description='ID of the patient in DB',example='P001')):
    data = load_data()
    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail='Patient not Found!')

def sorted_patients(sort_by:str = Query('weight', description='Sort on the basis of weight ,hieght and bmi'), order:str= Query('asc',description="Sosrt values in ascending or descending order")):
    valid_fields =['height','weight','bmi']
    if sort_by not in valid_fields:
        raise HTTPException(status_code='400',detail=f'Invalid fields select from {valid_fields}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code='400',detail='Invalid order select asc or desc')
    
    data = load_data()
    sort_order = True if order =='desc' else False
    sort = sorted(data.values(),key= lambda x:x.get(sort_by,0),reverse=sort_order)
    return sort

def create_patient(patient:Patient):

    data = load_data()

    if patient.id in data:
        raise HTTPException(status_code=400,detail='Patient already exists in database')
    
    data[patient.id] = patient.model_dump(exclude=['id'])
    save_data(data)
    return JSONResponse(status_code=201, content='Patient created succesfully')


def update_patient(patient_id : str, patient:PatientUpdate):
    
    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404, detail='Patient Not Found!')
    
    existing_patient = data[patient_id]
    updated_patient = patient.model_dump(exclude_unset=True)
    for key,values in updated_patient.items():
        existing_patient[key] = values
    
    existing_patient['id']= patient_id
    updated = Patient(**existing_patient)
    existing_patient = updated.model_dump(exclude='id')
    data[patient_id]= existing_patient

    save_data(data)
    return JSONResponse(status_code=200,content={'mesage':'Patient Updated'})



def patient_delete(patient_id:str):

    data = load_data()
    if patient_id not in data:
        raise HTTPException(status_code=404,detail='Patient doesnt exist')
    
    del data[patient_id]
    save_data(data)
    return JSONResponse(status_code=200,content={'message':'Patient deleted'})









