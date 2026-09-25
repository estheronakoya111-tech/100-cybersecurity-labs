
````text
LAB 03 — FASTAPI AUTHENTICATION & AUTHORIZATION TESTING

Repository:
100-cybersecurity-labs

Folder:
Lab-03-FastAPI-Auth-Authorization/

Files:
- app.py
- notes.md
- screenshots/

==================================================
1. OBJECTIVE
==================================================

Build a small FastAPI application with login, token-based authentication, and protected user resources.

Use Burp Suite Repeater to inspect and modify HTTP requests and test whether users can access resources they are not authorized to access.

Main concepts:
- Authentication
- Authorization
- HTTP methods
- HTTP headers
- Bearer tokens
- Access control
- HTTP status codes
- Burp Suite Repeater


==================================================
2. TOOLS
==================================================

- Python
- FastAPI
- Uvicorn
- Burp Suite
- Kali Linux
- Browser


==================================================
3. APPLICATION CODE
==================================================

File: app.py

```python
from fastapi import FastAPI, HTTPException, Header
from pydantic import BaseModel

class LoginRequest(BaseModel):
    username: str

app = FastAPI()

users = {
    1: {
        "name": "Esther",
        "email": "esther@example.com"
    },
    2: {
        "name": "Bob",
        "email": "bob@example.com"
    },
    3: {
        "name": "John",
        "email": "john@example.com"
    }
}

tokens = {}

@app.get("/")
def home():
    return {"message": "API is running"}

@app.post("/login")
def login(data: LoginRequest):
    for user_id, user in users.items():
        if user["name"] == data.username:
            token = f"token-{user_id}"
            tokens[token] = user_id

            return {
                "message": "Login successful",
                "user_id": user_id,
                "token": token
            }

    raise HTTPException(
        status_code=401,
        detail="Invalid username"
    )

@app.get("/users/{user_id}")
def get_user(
    user_id: int,
    authorization: str = Header(None)
):
    token = authorization.replace("Bearer ", "")
    logged_in_user = tokens.get(token)

    if logged_in_user != user_id:
        raise HTTPException(
            status_code=403,
            detail="Forbidden"
        )

    return users[user_id]
````

==================================================
4. RUNNING THE APPLICATION
==========================

Start the server with:

```bash
uvicorn app:app --reload
```

The application runs locally at:

[http://127.0.0.1:8000](http://127.0.0.1:8000)

The first `app` in `app:app` refers to `app.py`.

The second `app` refers to the FastAPI application object.

==================================================
5. BASIC ENDPOINTS
==================

GET /

Purpose:
Check that the API is running.

Response:

```json
{
    "message": "API is running"
}
```

POST /login

Purpose:
Authenticate a user and generate a token.

Example request:

```http
POST /login HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{"username":"Bob"}
```

Example response:

```json
{
    "message": "Login successful",
    "user_id": 2,
    "token": "token-2"
}
```

GET /users/{user_id}

Purpose:
Return information belonging to a specific user.

The request requires an Authorization header.

Example:

```http
GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

```

==================================================
6. AUTHENTICATION VS AUTHORIZATION
==================================

Authentication answers:

"Who are you?"

Example:
Logging in as Bob.

Authorization answers:

"What are you allowed to access?"

Example:
Bob's token should allow Bob to access Bob's resource but not Esther's resource.

==================================================
7. BURP SUITE TESTING
=====================

Burp Suite Repeater was used to inspect and modify HTTP requests.

A valid Bob request:

```http
GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

```

The server returned Bob's information.

The request was then modified:

```http
GET /users/1 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

```

Only the user ID was changed.

The token still belonged to Bob.

The server returned:

```http
HTTP/1.1 403 Forbidden
```

This showed that the authorization check was working.

==================================================
8. AUTHORIZATION LOGIC
======================

The server extracts the token:

```python
token = authorization.replace("Bearer ", "")
```

It then finds the user associated with that token:

```python
logged_in_user = tokens.get(token)
```

Finally, it compares the logged-in user's ID with the requested user ID:

```python
if logged_in_user != user_id:
    raise HTTPException(
        status_code=403,
        detail="Forbidden"
    )
```

If they do not match, access is denied.

==================================================
9. STATUS CODES
===============

401 Unauthorized

Used when authentication fails.

Example:

```json
{
    "detail": "Invalid username"
}
```

403 Forbidden

Used when the request is understood but the authenticated user is not allowed to access the requested resource.

==================================================
10. TOKEN TESTING
=================

The application generates tokens using:

```python
token = f"token-{user_id}"
```

Therefore:

User 1 → token-1

User 2 → token-2

User 3 → token-3

However, a token only becomes active after that user logs in because the token is stored in:

```python
tokens[token] = user_id
```

For example, after Bob logs in:

```text
token-2 → user ID 2
```

Testing `token-1` before Esther logs in does not authenticate Esther because that token has not yet been added to the server's in-memory token store.

==================================================
11. SECURITY OBSERVATION
========================

The token format is predictable:

```text
token-1
token-2
token-3
```

This is acceptable for a controlled learning lab but is not secure for a real application.

Production applications should use unpredictable tokens with proper expiration, validation, and revocation mechanisms.

==================================================
12. BURP SUITE LESSON
=====================

Burp Repeater made it possible to:

* Inspect HTTP requests
* Modify the requested user ID
* Modify Authorization headers
* Resend requests
* Observe server responses
* Test access-control behavior

A key lesson was that changing client-side request values does not matter if the server properly verifies authorization.

==================================================
13. PROBLEMS ENCOUNTERED
========================

Burp initially produced a request timeout.

The problem was caused by the HTTP request not having a blank line after the headers.

Correct structure:

```http
GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

```

The blank line tells the server that the HTTP headers have ended and the request is ready to be processed.

==================================================
14. KEY LEARNING
================

Authentication and authorization are different.

A user being logged in does not automatically mean they should be able to access every resource.

The server must verify:

1. Who the user is.
2. Which resource they requested.
3. Whether that user is allowed to access it.

Burp Suite can be used to test whether these checks are actually enforced by the server.

==================================================
15. RESULT
==========

Successfully:

* Built a FastAPI API.
* Created a login endpoint.
* Implemented simple token authentication.
* Protected user resources.
* Used Authorization headers.
* Tested requests with Burp Suite Repeater.
* Modified user IDs to test access control.
* Confirmed unauthorized access returned 403.
* Investigated how tokens were generated and stored.
* Identified predictable token generation as a security weakness.

LAB STATUS: COMPLETE

Environment: Local/controlled environment
Purpose: Cybersecurity education and authorized security testing

```
```
