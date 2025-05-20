from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from jose import jwt
from database import SessionLocal, Base, engine
from models import Item
from schemas import ItemCreate, Item
from fastapi.security import OAuth2PasswordBearer

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
        if username is None:
            raise HTTPException(status_code=401, detail="Token inválido")
        user = db.query(User).filter(User.username == username).first()
        if user is None:
            raise HTTPException(status_code=401, detail="Usuario no encontrado")
        return user
    except JWTError:
        raise HTTPException(status_code=401, detail="Token inválido")

@app.post("/items/", response_model=Item)
def create_item(item: ItemCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role_id not in [2, 3]:  # Solo Dueño o Admin
        raise HTTPException(status_code=403, detail="No autorizado")
    db_item = Item(**item.dict(), owner_id=user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/items/", response_model=list[Item])
def read_items(user=Depends(get_current_user), db: Session = Depends(get_db)):
    if user.role_id == 3:  # Admin ve todos los ítems
        return db.query(Item).all()
    return db.query(Item).filter(Item.owner_id == user.id).all()

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: ItemCreate, user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item or (db_item.owner_id != user.id and user.role_id != 3):
        raise HTTPException(status_code=403, detail="No autorizado")
    for key, value in item.dict().items():
        setattr(db_item, key, value)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/items/{item_id}")
def delete_item(item_id: int, user=Depends(get_current_user), db: Session = Depends(get_db)):
    db_item = db.query(Item).filter(Item.id == item_id).first()
    if not db_item or (db_item.owner_id != user.id and user.role_id != 3):
        raise HTTPException(status_code=403, detail="No autorizado")
    db.delete(db_item)
    db.commit()
    return {"message": "Ítem eliminado"}