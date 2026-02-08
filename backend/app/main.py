from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import sqlite3
import uvicorn

# Absolute imports
from app.database import init_db, get_db
from app.schemas import UserCreate, UserUpdate, UserResponse

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Enterprise CRM API", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/users", response_model=list[UserResponse])
def fetch_users():
    with get_db() as db:
        cursor = db.execute("SELECT * FROM usersinfo")
        return [dict(row) for row in cursor.fetchall()]

@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate):
    with get_db() as db:
        try:
            cursor = db.execute(
                "INSERT INTO usersinfo (first_name, last_name, email, tel, password) VALUES (?, ?, ?, ?, ?)",
                (user.first_name, user.last_name, user.email, user.tel, user.password)
            )
            db.commit()
            row = db.execute("SELECT * FROM usersinfo WHERE id = ?", (cursor.lastrowid,)).fetchone()
            return dict(row)
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail={"error": "Email already exists"})

@app.put("/api/users/{id}", response_model=UserResponse)
def update_user(id: int, user_data: UserUpdate):
    with get_db() as db:
        current = db.execute("SELECT * FROM usersinfo WHERE id = ?", (id,)).fetchone()
        if not current:
            raise HTTPException(status_code=404, detail={"error": "User not found"})
        
        update_info = dict(current)
        # model_dump is the new version of .dict() in Pydantic v2
        update_info.update(user_data.model_dump(exclude_unset=True))
        
        db.execute(
            """UPDATE usersinfo SET first_name=?, last_name=?, email=?, tel=?, password=?, updated_at=CURRENT_TIMESTAMP 
               WHERE id=?""",
            (update_info['first_name'], update_info['last_name'], update_info['email'], 
             update_info['tel'], update_info['password'], id)
        )
        db.commit()
        return dict(db.execute("SELECT * FROM usersinfo WHERE id = ?", (id,)).fetchone())

@app.delete("/api/users/{id}")
def delete_user(id: int):
    with get_db() as db:
        cursor = db.execute("DELETE FROM usersinfo WHERE id = ?", (id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail={"error": "User not found"})
        return {"message": "User deleted successfully"}

if __name__ == "__main__":
    # Note: We use "app.main:app" string format for the reload to work correctly
    uvicorn.run("app.main:app", host="127.0.0.1", port=5000, reload=True)