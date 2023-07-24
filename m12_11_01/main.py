import os
import pathlib
import time
from typing import List

from fastapi import FastAPI, Depends, HTTPException, status, Path, Query, Request, File, UploadFile
from sqlalchemy import text
from sqlalchemy.orm import Session

from db import get_db
from middleware import CustomHeaderMiddleware
from models import Owner, Cat
from schemas import OwnerModel, OwnerResponse, CatModel, CatResponse, CatVaccinatedModel

app = FastAPI()


@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


app.add_middleware(CustomHeaderMiddleware)


@app.get("/")
def read_root():
    return {"message": "Application started"}


@app.get("/api/healthchecker")
def healthchecker(db: Session = Depends(get_db)):
    try:
        # Make request
        result = db.execute(text("SELECT 1")).fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.get("/owners", response_model=List[OwnerResponse], tags=["owners"])
async def get_owners(db: Session = Depends(get_db)):
    owners = db.query(Owner).all()
    return owners


@app.get("/owners/{owner_id}", response_model=OwnerResponse, tags=["owners"])
async def get_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return owner


@app.post("/owners", response_model=OwnerResponse, tags=["owners"])
async def create_owner(body: OwnerModel, db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(email=body.email).first()
    if owner:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email is existing!",
        )
    owner = Owner(email=body.email)
    db.add(owner)
    db.commit()
    return owner


@app.put("/owners/{owner_id}", response_model=OwnerResponse, tags=["owners"])
async def update_owner(body: OwnerModel, owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    owner.email = body.email
    db.commit()
    return owner


@app.delete("/owners/{owner_id}", response_model=OwnerResponse, tags=["owners"])
async def delete_owner(owner_id: int = Path(ge=1), db: Session = Depends(get_db)):
    owner = db.query(Owner).filter_by(id=owner_id).first()
    if owner is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    db.delete(owner)
    db.commit()
    return owner


@app.get("/cats", response_model=List[CatResponse], tags=["cats"])
async def get_cats(limit: int = Query(10, ge=10, le=500), offset: int = Query(0, ge=0, le=200),
                   db: Session = Depends(get_db)):
    cats = db.query(Cat).limit(limit).offset(offset).all()
    return cats


@app.get("/cats/{cat_id}", response_model=CatResponse, tags=["cats"])
async def get_cats(cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    return cat


@app.post("/cats", response_model=CatResponse, tags=["cats"])
async def create_cat(body: CatModel, db: Session = Depends(get_db)):
    cat = Cat(**body.model_dump())
    db.add(cat)
    db.commit()
    return cat


@app.put("/cats/{cat_id}", response_model=CatResponse, tags=["cats"])
async def update_cat(body: CatModel, cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    cat.nick = body.nick
    cat.age = body.age
    cat.description = body.description
    cat.vaccinated = body.vaccinated
    cat.owner_id = body.owner_id
    db.commit()
    return cat


@app.delete("/cats/{cat_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["cats"])
async def get_cats(cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    db.delete(cat)
    db.commit()
    return cat


@app.patch("/cats/{cat_id}/vaccinated", response_model=CatResponse, tags=["cats"])
async def update_cat(body: CatVaccinatedModel, cat_id: int = Path(ge=1), db: Session = Depends(get_db)):
    cat = db.query(Cat).filter_by(id=cat_id).first()
    if cat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="NOT FOUND",
        )
    cat.vaccinated = body.vaccinated
    db.commit()
    return cat


# @app.post("/uploadfile/")
# async def create_upload_file(file: UploadFile = File()):
#     pathlib.Path("uploads").mkdir(exist_ok=True)
#     file_path = f"uploads/{file.filename}"
#     with open(file_path, "wb") as f:
#         f.write(await file.read())
#     return {"file_path": file_path}

MAX_FILE_SIZE = 1_000_000


@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File()):
    pathlib.Path("uploads").mkdir(exist_ok=True)
    file_path = f"uploads/{file.filename}"
    file_size = 0
    with open(file_path, "wb+") as f:
        while True:
            chunk = await file.read(1024)
            if not chunk:
                break
            file_size += len(chunk)
            if file_size > MAX_FILE_SIZE:
                f.close()
                # os.unlink(file_path)
                pathlib.Path(file_path).unlink()
                raise HTTPException(status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
                                    detail="File size is over the limit")
            f.write(chunk)
    return {"file_path": file_path}
