from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware

from datetime import datetime
import sqlite3
from database import init_db, get_db
from schemas import UserCreate, UserResponse, UserUpdate

app = FastAPI()

# Fixes the "Failed to fetch" error for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    init_db()

@app.get("/api/users", response_model=list[UserResponse])
def fetch_users():
    db = get_db()
    cursor = db.execute("SELECT * FROM usersinfo")
    rows = cursor.fetchall()
    # Convert sqlite3.Row objects to dictionaries so Pydantic is happy
    return [dict(row) for row in rows]

@app.post("/api/users", response_model=UserResponse)
def create_user(user: UserCreate):
    # Using 'with' ensures the connection closes even if there's an error
    with get_db() as db:
        try:
            cursor = db.execute(
                "INSERT INTO usersinfo (first_name, last_name, email, tel, password) VALUES (?, ?, ?, ?, ?)",
                (user.first_name, user.last_name, user.email, user.tel, user.password)
            )
            db.commit()
            id = cursor.lastrowid
            
            # Fetch and return the new row
            row = db.execute("SELECT * FROM usersinfo WHERE id = ?", (id,)).fetchone()
            return dict(row)
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail={"error": "Email already registered"})
        except sqlite3.OperationalError as e:
            raise HTTPException(status_code=500, detail={"error": f"Database error: {str(e)}"})
        

@app.put("/api/users/{id}", response_model=UserResponse)
def update_user(id: int, user_data: UserUpdate):
    with get_db() as db:
        # 1. Fetch current user data
        current_user = db.execute("SELECT * FROM usersinfo WHERE id = ?", (id,)).fetchone()
        if not current_user:
            raise HTTPException(status_code=404, detail={"error": "User not found"})
        
        # 2. Convert current row to a dict to easily update
        update_dict = dict(current_user)
        
        # 3. Overwrite only the fields provided in the request
        # .dict(exclude_unset=True) only gives us the fields actually sent by the frontend
        incoming_data = user_data.dict(exclude_unset=True)
        update_dict.update(incoming_data)
        
        # 4. Update the record
        try:
            db.execute(
                """UPDATE usersinfo 
                   SET first_name=?, last_name=?, email=?, tel=?, password=?, updated_at=CURRENT_TIMESTAMP
                   WHERE id=?""",
                (
                    update_dict["first_name"], 
                    update_dict["last_name"], 
                    update_dict["email"], 
                    update_dict["tel"], 
                    update_dict["password"], 
                    id
                )
            )
            db.commit()
        except sqlite3.IntegrityError:
            raise HTTPException(status_code=400, detail={"error": "Email already in use"})

        # 5. Return the updated user
        row = db.execute("SELECT * FROM usersinfo WHERE id = ?", (id,)).fetchone()
        return dict(row)

@app.delete("/api/users/{id}")
def delete_user(id: int):
    with get_db() as db:
        cursor = db.execute("DELETE FROM usersinfo WHERE id = ?", (id,))
        db.commit()
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail={"error": "User not found"})
        return {"message": "User deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=5000)