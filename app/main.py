from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from . import models, schemas, crud, auth
from .database import engine, get_db
from .logging import logger
from .worker import process_turnover_file

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"Request: {request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Response: {response.status_code}")
    return response

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile = File(...)):
    file_location = f"files/{file.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(file.file.read())
    process_turnover_file.delay(file_location)
    return {"filename": file.filename}

@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()):
    user = auth.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.config.settings.access_token_expire_minutes)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.get("/users/me/", response_model=schemas.User)
async def read_users_me(current_user: schemas.User = Depends(auth.get_current_user)):
    return current_user

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