

# Lab 03 — FastAPI Authentication & Authorization

## Overview

This lab focused on understanding and testing authentication and authorization in a simple FastAPI API.

I built a small API with:

- User data
- A login endpoint
- Token-based authentication
- A protected user endpoint
- Server-side authorization checks

I then used Burp Suite to inspect and modify HTTP requests and observe how the API responded.

The purpose was not to build production-ready authentication, but to understand how authentication, tokens, authorization, and HTTP requests work together.

---

# Objectives

- Understand the difference between authentication and authorization.
- Build a basic authentication flow with FastAPI.
- Understand how POST requests are used for login.
- Understand how GET requests are used to retrieve protected resources.
- Understand how authentication tokens are issued and used.
- Use Burp Suite to inspect and modify HTTP requests.
- Test whether a user's token can access another user's data.
- Understand how server-side authorization prevents unauthorized access.
- Identify weaknesses in a simplified token implementation.

---

# Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Burp Suite
- Kali Linux

---

# 1. Creating the FastAPI Application

I created a simple FastAPI application and defined a few users:

- Esther — user ID 1
- Bob — user ID 2
- John — user ID 3

The application also contains a dictionary called `tokens` which stores the relationship between issued tokens and user IDs.

Example:

```python
tokens = {}

The application was started with:

uvicorn app:app --reload

The API was available locally at:

http://127.0.0.1:8000


---

2. FastAPI and Python Concepts Learned

FastAPI()

app = FastAPI()

This creates the FastAPI application.

The variable app represents the application that Uvicorn runs.


---

Routes

A route connects an HTTP method and URL path to a Python function.

For example:

@app.get("/")
def home():
    return {"message": "API is running"}

This means a GET request to / calls the home() function.


---

HTTP Methods

I worked with both GET and POST requests.

GET

GET is used to request or retrieve information.

Example:

GET /users/2

This asks the server for user 2.

POST

POST is used to send data to the server, often to create something or perform an action.

Example:

POST /login

The login request sends the username to the server.


---

3. Pydantic Model

I created a Pydantic model for the login request:

class LoginRequest(BaseModel):
    username: str

This defines the structure of the data expected by /login.

The request body looks like:

{
    "username": "Bob"
}

FastAPI/Pydantic uses the model to validate and structure the incoming data.

I learned that LoginRequest is a class/model rather than a function.


---

4. Authentication vs Authorization

One of the main concepts learned during this lab was the difference between authentication and authorization.

Authentication

Authentication answers:

> Who are you?



In this lab, /login is responsible for authentication.

The user provides a username and the server identifies the corresponding user.


---

Authorization

Authorization answers:

> What are you allowed to access?



The /users/{user_id} endpoint checks whether the authenticated user is allowed to access the requested user resource.

Authentication and authorization are therefore separate concepts.

A user being logged in does not automatically mean they should be allowed to access every resource.


---

5. Testing /login

The login endpoint uses POST:

POST /login

The request body was:

{
    "username": "Bob"
}

The server returned a response containing:

{
    "message": "Login successful",
    "user_id": 2,
    "token": "token-2"
}

This demonstrated the basic flow:

POST /login
      ↓
Server identifies user
      ↓
Token is created
      ↓
Token is returned to the client


---

6. Understanding the Token

The token in this lab was created with:

token = f"token-{user_id}"

The token was then associated with the user's ID:

tokens[token] = user_id

For example:

token-1 → user 1
token-2 → user 2
token-3 → user 3

The tokens dictionary acts as a simple in-memory representation of active authentication tokens.

This is only a learning implementation and is not suitable for production authentication.


---

7. Using the Token

After logging in as Bob, I used his token to access his user endpoint.

The request was:

GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

The Authorization header carries the token.

Bearer indicates that the token is being presented as the authentication credential.

The server extracts the token:

token = authorization.replace("Bearer ", "")

It then looks up the user associated with that token:

logged_in_user = tokens.get(token)

For Bob:

token-2 → 2

So the server knows that the request is authenticated as user 2.


---

8. Understanding HTTP Headers

I learned that HTTP headers contain additional information about a request.

For example:

Host: 127.0.0.1:8000
Authorization: Bearer token-2

The Host header identifies the destination host and port.

The Authorization header carries authentication information.

I also learned that HTTP headers need to be separated from the request body by a blank line.

For example:

GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

The blank line tells the server that the headers have ended.

A missing blank line caused Burp to warn that the HTTP header block was incomplete and could result in a request timeout.


---

9. Using Burp Suite

I used Burp Suite to inspect and manipulate the HTTP requests sent to the FastAPI application.

Burp Repeater was particularly useful because it allowed me to modify a request and send it again without having to repeat the entire browser interaction.

I used it to:

Inspect login requests

Change HTTP methods

Modify URL paths

Modify the Authorization header

Send requests repeatedly

Observe HTTP status codes

Test authorization behavior



---

10. GET vs POST in the Lab

I initially worked with /login using POST.

The login flow was:

POST /login
      ↓
Receive token
      ↓
GET /users/2
      ↓
Use token to access protected data

I also learned that simply visiting /login in a browser normally produces a GET request, but the /login endpoint in this application expects POST.

Therefore:

GET /login

is not the same as:

POST /login

The method is part of the API operation.


---

11. Authorization Test

After successfully accessing Bob's information using:

GET /users/2
Authorization: Bearer token-2

I changed the requested resource from:

/users/2

to:

/users/1

while keeping Bob's token:

Authorization: Bearer token-2

The server returned:

403 Forbidden

The server was effectively checking:

Authenticated user = 2
Requested user = 1

Because they did not match, access was denied.

This demonstrated server-side authorization.


---

12. Why the 403 Happened

The authorization check in the API is:

if logged_in_user != user_id:
    raise HTTPException(
        status_code=403,
        detail="Forbidden"
    )

This means:

> If the authenticated user's ID does not match the requested user's ID, deny access.



This is important because authorization must be enforced by the backend.

Simply hiding another user's profile from the frontend would not be enough.


---

13. Testing token-1

I also tested whether I could simply change Bob's token:

token-2

to:

token-1

while requesting:

/users/1

The result was also:

403 Forbidden

The reason was not that token-1 was inherently invalid.

At that point, I had only logged in as Bob.

The tokens dictionary therefore contained something equivalent to:

token-2 → 2

but did not yet contain:

token-1 → 1

until Esther actually logged in.

This helped me understand that the token lookup is based on the current server state.


---

14. Predictable Token Design

The lab also revealed a security weakness in the token implementation.

Tokens are generated using:

token = f"token-{user_id}"

This means the token can be predicted from the user's ID.

For example:

user 1 → token-1
user 2 → token-2
user 3 → token-3

This is obviously not secure authentication.

A real application should not create authentication tokens from predictable user information.

Real systems use securely generated, unpredictable credentials/tokens and normally include additional protections such as expiration and proper token/session management.

This predictable token design was intentionally used because the purpose of the lab was learning how authentication and authorization work.


---

15. Authentication Flow

The complete authentication flow I implemented was:

User sends username
        ↓
POST /login
        ↓
Server identifies user
        ↓
Server generates token
        ↓
Token is stored with user ID
        ↓
Token returned to client
        ↓
Client sends token with protected request
        ↓
Server identifies authenticated user
        ↓
Server checks authorization
        ↓
Resource is returned or access is denied


---

16. Security Testing Flow

Using Burp Suite, the testing process was:

Login as Bob
      ↓
Receive token-2
      ↓
Request /users/2 with token-2
      ↓
Bob's data returned
      ↓
Change request to /users/1
      ↓
Keep token-2
      ↓
403 Forbidden

This demonstrated that the backend was checking authorization instead of simply trusting the requested user ID.


---

17. Important Security Concepts Learned

Authentication

Verifying the identity of a user.

Authorization

Determining what an authenticated user is allowed to access.

HTTP methods

GET retrieves information while POST sends data or performs an operation.

HTTP headers

Headers carry additional information about HTTP requests and responses.

Authorization header

Used to send authentication credentials such as a bearer token.

Bearer token

A token presented as proof of authentication.

HTTP 401

Generally indicates that authentication is missing or invalid.

HTTP 403

Indicates that the server understood the request but refuses to allow access.

Server-side authorization

Permissions must be checked by the backend rather than trusted from the frontend.

Burp Repeater

Allows HTTP requests to be modified and resent for testing.

Predictable credentials

Authentication credentials should not be derived from predictable values such as user IDs.


---

18. Key Takeaways

This lab helped me understand that:

Being logged in does not automatically mean a user can access everything.

Authentication and authorization are different security controls.

HTTP methods matter.

Tokens can be used to identify an authenticated session/user.

Authentication information can be sent through HTTP headers.

Burp Suite can be used to manipulate requests and test backend behavior.

Authorization must be enforced on the server.

A 403 Forbidden response can indicate that the server correctly rejected an unauthorized resource request.

A token implementation can technically work while still being insecure because of predictable token generation.

A simple lab implementation should not be confused with production authentication.



---

Limitations

This application was intentionally simplified for learning.

It does not implement:

Password authentication

Secure random token generation

Token expiration

Refresh tokens

Token revocation

Persistent sessions/database storage

Production-grade authentication

HTTPS configuration


The purpose of this lab was to understand the underlying concepts and practice testing them with Burp Suite.


---

Evidence

Screenshots from Burp Suite were captured during the lab as evidence of the HTTP requests and responses tested.

The screenshots support the practical testing performed in this lab.


---

Result

I successfully built and tested a small FastAPI API with authentication and server-side authorization.

I used Burp Suite to manipulate authenticated requests and confirmed that a user's token could not access another user's resource when the authorization check was enforced.

The lab also exposed a predictable-token weakness in the simplified authentication design, giving me a practical understanding of why real authentication systems require stronger token generation and session management.
