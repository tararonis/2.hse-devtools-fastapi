# uvicorn main:app --reload
# uvicorn main:app --host 0.0.0.0 --port 8000

from enum import Enum
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import time

app = FastAPI()


class DogType(str, Enum):
    terrier = "terrier"
    bulldog = "bulldog"
    dalmatian = "dalmatian"


class Dog(BaseModel):
    name: str
    pk: int
    kind: DogType


class Timestamp(BaseModel):
    id: int
    timestamp: int


dogs_db = {
    0: Dog(name="Bob", pk=0, kind="terrier"),
    1: Dog(name="Marli", pk=1, kind="bulldog"),
    2: Dog(name="Snoopy", pk=2, kind="dalmatian"),
    3: Dog(name="Rex", pk=3, kind="dalmatian"),
    4: Dog(name="Pongo", pk=4, kind="dalmatian"),
    5: Dog(name="Tillman", pk=5, kind="bulldog"),
    6: Dog(name="Uga", pk=6, kind="bulldog"),
}

post_db = [Timestamp(id=0, timestamp=12), Timestamp(id=1, timestamp=10)]


# 1. Реализован путь / – 1 балл
@app.get("/")
def root():
    return "It's dangerous to go alone! Take this. (===||:::::::::::::::>"


# 2. Реализован путь /post – 1 балла
@app.post("/post")
def return_timestamp() -> Timestamp:
    latest_timestamp = post_db[-1]
    new_timestamp = Timestamp(latest_timestamp.id + 1, time.time())
    post_db.append(new_timestamp)
    return new_timestamp


# 3. Реализована запись собак – 1 балл
@app.post("/dog")
def create_dog(new_dog: Dog) -> Dog:
    if not all(new_dog.pk != dog.pk for dog in dogs_db.values()):
        raise HTTPException(
            status_code=422, detail=f'PK param: "{new_dog.pk}" is not uniq'
        )
    dogs_db[new_dog.pk] = new_dog
    return new_dog


# 4. Реализовано получение списка собак – 1 балл
@app.get("/dog")
def get_dogs_list(kind: DogType = None):
    if kind:
        # 6. Реализовано получение собак по типу – 1 балл
        return [dog for dog in dogs_db.values() if dog.kind == kind]
    else:
        return [dog for dog in dogs_db.values()]


# 5. Реализовано получение собаки по id – 1 балл
@app.get("/dog/{pk}")
def get_dog_by_id(pk: int) -> Dog:
    required_dog = dogs_db.get(pk, None)

    if required_dog:
        return required_dog
    else:
        raise HTTPException(
            status_code=422, detail=f'Can\'t find dog with pk "{pk}" in the DB'
        )


# 7. Реализовано обновление собаки по id – 1 балл
@app.patch("/dog/{pk}")
def patch_dog(pk: int, dog: Dog) -> Dog:
    required_dog = dogs_db.get(pk, None)
    if required_dog:
        if dog.pk == pk:
            dogs_db[pk] = dog
            return dog
        else:
            raise HTTPException(
                status_code=422,
                detail=f'The pk from new object data: "{dog.pk}" doesn\'t match pk from URL "{pk}"',
            )
    else:
        raise HTTPException(
            status_code=422, detail=f'The dog with pk "{pk}" doens\t exist in the DB'
        )
