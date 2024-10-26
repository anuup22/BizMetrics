from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from . import models, schemas, crud
from .database import engine, get_db
import pandas as pd
from PyPDF2 import PdfFileReader
import io

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    if file.content_type == 'application/pdf':
        pdf_reader = PdfFileReader(file.file)
        # Process PDF file
    elif file.content_type == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
        df = pd.read_excel(file.file)
        # Process Excel file
    elif file.content_type == 'text/csv':
        df = pd.read_csv(file.file)
        # Process CSV file
    else:
        raise HTTPException(status_code=400, detail="Invalid file type")
    return {"filename": file.filename}

@app.post("/turnovers/", response_model=schemas.Turnover)
def create_turnover(turnover: schemas.TurnoverCreate, db: Session = Depends(get_db)):
    return crud.create_turnover(db=db, turnover=turnover)

@app.get("/turnovers/", response_model=list[schemas.Turnover])
def read_turnovers(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    turnovers = crud.get_turnovers(db, skip=skip, limit=limit)
    return turnovers

@app.get("/turnovers/{turnover_id}", response_model=schemas.Turnover)
def read_turnover(turnover_id: int, db: Session = Depends(get_db)):
    db_turnover = crud.get_turnover(db, turnover_id=turnover_id)
    if db_turnover is None:
        raise HTTPException(status_code=404, detail="Turnover not found")
    return db_turnover