Create users info details form

Framework & library: flask, sqlite3, pydantic, fast api </br>
Unit Test: pytest </br>
Feature: get user api, add new user api, delete user api </br>
db table name: usersinfo </br>
Python version: 3.14 </br>
users details: first name, last name, email, tel password, created time, updated time </br>

Feature:
-view existing user information </br>
-add new user information </br>
-update existing user </br>
-delete user </br>

<img width="785" height="551" alt="Screenshot 2026-02-08 at 1 59 47 PM" src="https://github.com/user-attachments/assets/135e1f22-c9a1-4e3f-96a4-4a5202f20d99" />

frontend server: http://localhost:5173/
backend server: http://127.0.0.1:5000/

Api mapping table:
Frontend Function,Method,Endpoint,Backend Status </br>
fetchUsers(),GET,/api/users,Matched </br>
createUser(user),POST,/api/users,Matched </br>
"updateUser(id, patch)",PUT,/api/users/{id},Matched </br>
deleteUser(id),DELETE,/api/users/{id},Matched </br>

backend folder structure:
backend/
├── app/
│ ├── main.py # FastAPI routes and logic
│ ├── database.py # SQLite connection & table setup
│ ├── schemas.py # Pydantic models
│ └── models.py # Database helper functions
├── tests/
│ └── test_main.py # Pytest unit tests
└── requirements.txt
