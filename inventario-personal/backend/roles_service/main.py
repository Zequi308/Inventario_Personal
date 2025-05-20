from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from database import SessionLocal, Base, engine
from models import Role
from schemas import Role
from fastapi.security import OAuth2PasswordBearer
from jose import jwt

app = FastAPI()
SECRET_KEY = "your-secret-key"  # Debe coincidir con auth_service
ALGORITHM = "HS256"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="http://localhost:8000/token")

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user = db.query(User).filter(User.username == username).first()
        if user is None or user.role_id != 3:  # Solo Admin
            raise HTTPException(status_code=403, detail="No autorizado")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.get("/roles/", response_model=list[Role])
def read_roles(user=Depends(get_current_user), db: Session = Depends(get_db)):
    return db.query(Role).all()