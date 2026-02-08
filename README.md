Create users info details form

Framework & library: flask, sqlite3, pydantic, fast api
Unit Test: pytest
Feature: get user api, add new user api, delete user api
db table name: usersinfo
Python version: 3.14
users details: first name, last name, email, tel password, created time, updated time

Feature:
-view existing user information
-add new user information
-update existing user 
-delete user

<img width="785" height="551" alt="Screenshot 2026-02-08 at 1 59 47 PM" src="https://github.com/user-attachments/assets/135e1f22-c9a1-4e3f-96a4-4a5202f20d99" />

frontend server: http://localhost:5173/
backend server: http://127.0.0.1:5000/

Api mapping table:
Frontend Function,Method,Endpoint,Backend Status
fetchUsers(),GET,/api/users,Matched
createUser(user),POST,/api/users,Matched
"updateUser(id, patch)",PUT,/api/users/{id},Matched
deleteUser(id),DELETE,/api/users/{id},Matched

backend folder structure:
backend/
├── app/
│   ├── main.py          # FastAPI routes and logic
│   ├── database.py      # SQLite connection & table setup
│   ├── schemas.py       # Pydantic models
│   └── models.py        # Database helper functions
├── tests/
│   └── test_main.py     # Pytest unit tests
└── requirements.txt
