from fastapi import FastAPI , status , HTTPException
from pydantic import BaseModel 
from database import SessionLocal
from sqlalchemy.orm import Session
import models

app = FastAPI()
db = SessionLocal()

class OurBaseModel(BaseModel):      #Error - Await Serialize response
    class Config:
        orm_mode = True        

class Person(OurBaseModel):
    id: int
    firstname: str
    lastname: str
    isMale: bool

@app.get('/', response_model=list[Person], status_code=status.HTTP_200_OK)
def getAll_Persons():
    getAllPersons = db.query(models.Person).all()

    return getAllPersons

@app.get('/getbyid/{person_id}', response_model= Person, status_code=status.HTTP_200_OK)
def get_Single_Person(person_id:int):
    getsingle_person = db.query(models.Person).filter(models.Person.id == person_id).first()

    if getsingle_person is not None:
        return getsingle_person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person not found")


@app.post('/addperson', response_model=Person, status_code=status.HTTP_201_CREATED)
def add_Person(person: Person):
    newPerson = models.Person(
        id = person.id,
        firstname = person.firstname,
        lastname = person. lastname,
        isMale = person.isMale
    )
    
    find_person = db.query(models.Person).filter(models.Person.id == person.id).first()

    if find_person is not None:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail="Person with this id already exist")

    db.add(newPerson)
    db.commit()

    return newPerson

@app.put('/update_person/{person_id}', response_model=Person, status_code=status.HTTP_202_ACCEPTED)
def updatePerson(person_id:int, person: Person):
    find_person = db.query(models.Person).filter(models.Person.id == person_id).first()

    if find_person is not None:
        find_person.id = person.id
        find_person.firstname = person.firstname
        find_person.lastname = person.lastname 
        find_person.isMale = person.isMale

        db.commit
        return find_person
    
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person with this id not found")


@app.delete("/delete_person/{person_id}", response_model=Person, status_code=200)
def deletePerson(person_id:int):
    find_person = db.query(models.Person).filter(models.Person.id == person_id).first()

    if find_person is not None:
        db.delete(find_person)
    
        db.commit()
        return find_person
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Person with this id not found")


# @app.get('/', status_code=200)
# def getCar_Info():
#     return {"message" : "Server is running"}

# @app.get('/', status_code=200)
# def getPerson_info():
#     return {"message" : "Server is running"}

# @app.get('/getpersonbyid/{person_id}', status_code=200)
# def getPerson_By_Id(person_id: int):
#     return {"message" : f"Your Person Id is {person_id}"}
  
# @app.post('/addpersoninfo', status_code=200)
# def addPerson_Info(person: Person):
#     return {
#         "id" : person.id,
#         "firstname" : person.firstname,
#         "lastname": person. lastname,
#         "isMale" : person.isMale
#     }
