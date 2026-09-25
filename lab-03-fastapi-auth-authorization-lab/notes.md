# LAB 03 — FastAPI Authentication & Authorization Testing

## Overview

This lab focused on understanding how authentication and authorization work in an API and how to test access-control behavior using Burp Suite.

The API was built locally with FastAPI and tested through HTTP requests using Burp Suite Repeater.

The main goal was not to build a production-ready authentication system, but to understand how an API identifies users, issues tokens, checks those tokens, and prevents users from accessing resources they are not authorized to access.

---

# 1. Objectives

The objectives of this lab were to:

- Build a simple API using FastAPI.
- Understand FastAPI routes and HTTP methods.
- Understand how POST requests differ from GET requests.
- Understand Pydantic models and request validation.
- Understand authentication.
- Understand authorization.
- Create and use simple authentication tokens.
- Send tokens through the HTTP Authorization header.
- Test API requests using Burp Suite Repeater.
- Modify HTTP requests and observe how the server responds.
- Identify an authorization/access-control weakness.
- Fix the authorization problem by enforcing authorization server-side.
- Understand HTTP status codes such as 401 and 403.
- Understand why predictable tokens are insecure.
- Understand the difference between client requests and server-side security decisions.

---

# 2. Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Burp Suite
- HTTP
- VS Code
- Kali Linux / local testing environment

The API was intentionally kept simple so that the focus remained on authentication, authorization, HTTP requests, and security testing.

---

# 3. FastAPI Setup

FastAPI was used to create the API.

The application was started with:

    uvicorn app:app --reload

The command contains two important `app` references.

The first `app` refers to the Python file:

    app.py

The second `app` refers to the FastAPI application object created inside that file:

    app = FastAPI()

Therefore:

    app:app

means:

    Python file : FastAPI application object

The `--reload` option allows Uvicorn to automatically reload the application when changes are made to the source code during development.

The API was available locally at:

    http://127.0.0.1:8000

---

# 4. Creating the FastAPI Application

The basic FastAPI application was created with:

    from fastapi import FastAPI

    app = FastAPI()

The line:

    app = FastAPI()

creates the FastAPI application object.

Routes are then attached to this application using decorators such as:

    @app.get("/")
    @app.post("/login")

A decorator tells FastAPI which HTTP method and URL should trigger a particular function.

For example:

    @app.get("/")
    def home():
        return {"message": "API is running"}

This means that when a GET request is sent to `/`, FastAPI runs the `home()` function.

---

# 5. HTTP Methods

A major part of the lab was understanding HTTP requests.

Two methods were especially important:

## GET

GET is normally used to retrieve information from a server.

For example:

    GET /users/2

can mean:

"Give me the information belonging to user 2."

## POST

POST is commonly used when sending data to the server or asking the server to perform an operation that includes submitted data.

The login endpoint used POST:

    POST /login

The username was sent in the request body.

This is why opening `/login` directly in a browser was not the same as sending a POST request.

Typing a URL into the browser normally results in a GET request.

The login endpoint expected POST.

---

# 6. Pydantic Request Model

The application used a Pydantic model to define the expected structure of login data.

The model was:

    class LoginRequest(BaseModel):
        username: str

This introduced another important Python concept: classes.

`LoginRequest` is a class that represents the structure of the data expected by the endpoint.

The field:

    username: str

means that the request is expected to contain a `username` value represented as a string.

The model was then used by the login endpoint:

    @app.post("/login")
    def login(data: LoginRequest):

FastAPI uses the Pydantic model to parse and validate the incoming request data.

For example, the expected JSON body was:

    {
        "username": "Bob"
    }

The important lesson was that `LoginRequest` is not a normal function. It is a class/model describing the expected structure of incoming data.

---

# 7. User Data

The application used a simple in-memory dictionary to represent users:

    users = {
        1: {
            "name": "Esther", "email": "esther@example.com"
        },
        2: {
            "name": "Bob", "email": "bob@example.com"
        },
        3: {
            "name": "John", "email": "john@example.com"
        }
    }

Each user had:

- A numeric user ID.
- A name.
- An email address.

This was intentionally simple.

The users were not stored in a real database for this lab.

---

# 8. Authentication vs Authorization

One of the most important concepts in this lab was the difference between authentication and authorization.

## Authentication

Authentication answers:

"Who are you?"

For this lab, authentication happened when a username was submitted to the `/login` endpoint.

If the username existed, the API treated the request as a successful login.

## Authorization

Authorization answers:

"What are you allowed to access?"

After authentication, the API needed to make sure that the logged-in user could only access the resource they were allowed to access.

For example:

If Bob is logged in as user 2, he should not automatically be able to access Esther's user information at `/users/1`.

Authentication identifies the user.

Authorization controls what that user is allowed to access.

---

# 9. Login Endpoint

The login endpoint was:

    @app.post("/login")
    def login(data: LoginRequest):

The endpoint loops through the users:

    for user_id, user in users.items():
        if user["name"] == data.username:

If the submitted username matches an existing user, a token is created.

The token is generated using:

    token = f"token-{user_id}"

The token is then stored:

    tokens[token] = user_id

The API returns:

    return {
        "message": "Login successful",
        "user_id": user_id,
        "token": token
    }

If the username does not exist, the API returns:

    raise HTTPException(status_code=401, detail="Invalid username")

---

# 10. Authentication Token Storage

The application used:

    tokens = {}

This dictionary acted as a very simple in-memory token store.

For example, if Bob logged in, the server could store:

    token-2 -> 2

This means:

- `token-2` belongs to user ID 2.
- User ID 2 is Bob.

The token could then be used in later requests.

This is only a simplified learning implementation.

A real authentication system would need much stronger token generation, expiration, revocation, secure storage, and other protections.

---

# 11. Testing Login with Burp Suite

Burp Suite Repeater was used to manually construct and modify HTTP requests.

A login request could look like:

    POST /login HTTP/1.1
    Host: 127.0.0.1:8000
    Content-Type: application/json
    Content-Length: 17

    {"username":"Bob"}

The important parts are:

- HTTP method: POST
- Endpoint: `/login`
- Host: `127.0.0.1:8000`
- Content-Type: `application/json`
- JSON request body

The blank line between the headers and body is important.

---

# 12. HTTP Header Blank-Line Issue

While using Burp Repeater, a problem was encountered where the request did not have a proper blank line after the HTTP headers.

Burp warned:

    HTTP header block does not have a blank line at the end

This caused the request to potentially wait or time out because the HTTP request was not formatted correctly.

The correct structure is:

    GET / HTTP/1.1
    Host: 127.0.0.1:8000

    <request body if needed>

There must be a blank line separating the HTTP headers from the request body.

This was an important practical HTTP lesson because manually editing requests in Burp means that small formatting mistakes can affect the request.

---

# 13. Successful Bob Login

A login request was sent with:

    {
        "username": "Bob"
    }

The API returned:

    {
        "message": "Login successful",
        "user_id": 2,
        "token": "token-2"
    }

This showed that the API had:

1. Received the login request.
2. Identified Bob.
3. Assigned Bob's user ID.
4. Created a token.
5. Stored the relationship between the token and user ID.
6. Returned the token to the client.

---

# 14. Authorization Header

After logging in, the token had to be sent with later requests.

The API expected the token in the HTTP Authorization header.

The request looked like:

    GET /users/2 HTTP/1.1
    Host: 127.0.0.1:8000
    Authorization: Bearer token-2

The important part is:

    Authorization: Bearer token-2

`Authorization` is the HTTP header.

`Bearer` indicates that the value following it is being presented as a bearer credential.

The API then extracts the token.

The code used:

    token = authorization.replace("Bearer ", "")

This removes the `Bearer ` prefix.

For:

    Bearer token-2

the resulting token becomes:

    token-2

The server then checks:

    logged_in_user = tokens.get(token)

If `token-2` belongs to user 2, the server obtains:

    logged_in_user = 2

---

# 15. Accessing Bob's Resource

After Bob logged in, the following request was tested:

    GET /users/2 HTTP/1.1
    Host: 127.0.0.1:8000
    Authorization: Bearer token-2

The API returned Bob's information.

This demonstrated the normal authenticated flow:

    Login
       ↓
    Receive token
       ↓
    Send token in Authorization header
       ↓
    Server identifies logged-in user
       ↓
    Server checks requested resource
       ↓
    Access granted

---

# 16. The Authorization Check

The user endpoint was:

    @app.get("/users/{user_id}")
    def get_user(user_id: int, authorization: str = Header(None)):

The server extracts the token:

    token = authorization.replace("Bearer ", "")

Then finds the logged-in user:

    logged_in_user = tokens.get(token)

The authorization decision is made with:

    if logged_in_user != user_id:
        raise HTTPException(status_code=403, detail="Forbidden")

Otherwise:

    return users[user_id]

The important security decision is:

    logged_in_user != user_id

If the logged-in user is not the same user as the requested resource, access is denied.

---

# 17. Initial Authorization Problem

Before the authorization check was properly enforced, changing the user ID in the URL could allow access to another user's information.

For example, a request intended for one user could be changed from:

    /users/1

to:

    /users/2

If the server simply trusted the user ID supplied in the URL without checking whether the requester was allowed to access it, the API could return another user's information.

This demonstrated an access-control weakness.

The important lesson was that a server must never rely on the client to decide what the client is allowed to access.

The client can modify:

- URLs
- parameters
- request bodies
- headers
- tokens
- other request data

The server must make the final authorization decision.

---

# 18. Testing the Authorization Control

After authorization was implemented, Bob's token was used:

    Authorization: Bearer token-2

The original request was:

    GET /users/2 HTTP/1.1

This correctly returned Bob's information.

The request was then modified to:

    GET /users/1 HTTP/1.1

while keeping:

    Authorization: Bearer token-2

This was an important Burp Suite test.

The request effectively asked:

"Bob's token is being used, but can Bob access user 1?"

The server returned:

    403 Forbidden

This demonstrated that the authorization check was working.

The server saw:

    logged_in_user = 2
    requested_user = 1

Since:

    2 != 1

the request was rejected.

---

# 19. Why 403 Was Returned

The application used HTTP status code 403 for this situation.

403 means that the server understood the request but is refusing to authorize access to the requested resource.

In this case, the user was authenticated with Bob's token, but the requested resource belonged to another user.

Therefore:

    Authentication: successful

but:

    Authorization: failed

This is why the application returned:

    403 Forbidden

---

# 20. Testing token-1

The token generation code was:

    token = f"token-{user_id}"

Therefore, based on the code:

    user 1 -> token-1
    user 2 -> token-2
    user 3 -> token-3

It was tempting to assume that simply sending:

    Authorization: Bearer token-1

would authenticate as Esther.

However, the server only stores tokens when the corresponding user actually logs in.

When Bob logged in, the token store contained something equivalent to:

    token-2 -> 2

There was no:

    token-1 -> 1

because Esther had not logged in during that server session.

Therefore, sending `token-1` without first logging Esther in did not automatically authenticate as Esther.

This demonstrated an important distinction between:

- the format of a token
- an active token stored by the server

A token-looking string is not automatically valid.

---

# 21. Predictable Token Weakness

Although the token system worked for this learning lab, the token generation method is insecure.

The application generates:

    token-{user_id}

This means the token is directly related to the user's ID.

For example:

    token-1
    token-2
    token-3

are predictable.

A production authentication system should not use predictable credentials like this.

Real authentication systems should use securely generated, unpredictable credentials and should normally include protections such as:

- expiration
- revocation
- secure storage
- appropriate token validation
- protection against token theft
- secure transport through HTTPS

The predictable token design was intentionally kept simple for this lab so the authentication and authorization concepts could be understood without introducing unnecessary complexity.

---

# 22. HTTPException

The application used:

    HTTPException

from FastAPI:

    from fastapi import FastAPI, HTTPException, Header

`HTTPException` allows the server to return an HTTP error response.

For example:

    raise HTTPException(status_code=401, detail="Invalid username")

returns a 401 response.

Another example:

    raise HTTPException(status_code=403, detail="Forbidden")

returns a 403 response.

This is different from:

    print()

`print()` only writes information to the server's console.

It does not create an HTTP error response for the client.

`HTTPException` tells FastAPI to send an actual HTTP error response.

---

# 23. Status Codes Used

Two important status codes were used in this lab.

## 401 Unauthorized

The application used 401 when the username supplied during login did not match a user.

Example:

    Invalid username

The idea was that authentication had failed.

## 403 Forbidden

The application used 403 when the authenticated user attempted to access another user's resource.

Example:

    Bob's token -> /users/1

The user had been identified, but the requested resource was not authorized for that user.

---

# 24. GET vs POST in Burp

Burp Repeater made the difference between HTTP methods more obvious.

For example:

    GET /users/2 HTTP/1.1

was used to retrieve user information.

The login endpoint required:

    POST /login HTTP/1.1

because the username was submitted in the request body.

A browser address bar normally performs a GET request, so simply navigating to:

    http://127.0.0.1:8000/login

does not perform the same operation as sending:

    POST /login

with JSON data.

This was an important practical lesson when manually testing APIs.

---

# 25. Burp Suite Repeater

Burp Suite Repeater was one of the main tools used during the lab.

Repeater allows an HTTP request to be:

- inspected
- edited
- resent
- compared
- tested with different values

This made it possible to manually test authorization behavior.

For example, the same request could be changed from:

    /users/2

to:

    /users/1

while keeping the same token.

This is useful when testing whether an API properly validates authorization instead of blindly trusting values supplied by the client.

---

# 26. Security Testing Process

The general testing process used in the lab was:

    1. Build the API
       ↓
    2. Start the server
       ↓
    3. Send a login request
       ↓
    4. Receive an authentication token
       ↓
    5. Send the token in the Authorization header
       ↓
    6. Request the authenticated user's resource
       ↓
    7. Modify the resource ID
       ↓
    8. Resend the request
       ↓
    9. Observe the server response
       ↓
    10. Verify whether authorization is enforced

This is a basic example of hands-on API security testing.

---

# 27. What This Lab Demonstrated

The lab demonstrated that API security cannot rely on the frontend or the client behaving correctly.

A client can change a request.

For example, a client can change:

    /users/2

to:

    /users/1

Therefore, the server must independently determine whether the requester is allowed to access user 1.

The security decision belongs on the server.

---

# 28. Python Concepts Reinforced

This lab also reinforced several Python concepts.

## Classes

The Pydantic request model used:

    class LoginRequest(BaseModel):

This reinforced the idea that a class defines a structure/type.

## Dictionaries

The application used dictionaries for:

- users
- tokens

For example:

    tokens[token] = user_id

stores a relationship between a token and a user ID.

## Functions

FastAPI endpoints are Python functions.

For example:

    def login(data: LoginRequest):

and:

    def get_user(user_id: int, authorization: str = Header(None)):

## Loops

The login endpoint used:

    for user_id, user in users.items():

to search through the stored users.

## Conditions

The application used conditions such as:

    if user["name"] == data.username:

and:

    if logged_in_user != user_id:

These conditions determine whether the request should continue or be rejected.

## f-strings

The token was generated with:

    f"token-{user_id}"

This is an f-string, allowing the value of `user_id` to be inserted into the string.

---

# 29. FastAPI Concepts Reinforced

The lab reinforced:

- FastAPI application creation
- Route decorators
- GET routes
- POST routes
- Path parameters
- Headers
- Request bodies
- Pydantic models
- HTTP exceptions
- HTTP status codes
- Uvicorn
- Local API testing

An example of a path parameter was:

    @app.get("/users/{user_id}")

The `{user_id}` portion is taken from the URL and passed into the function.

---

# 30. HTTP Concepts Reinforced

The lab provided practical experience with:

- HTTP methods
- HTTP headers
- HTTP request bodies
- HTTP status codes
- Authorization headers
- Bearer tokens
- GET requests
- POST requests
- Request formatting
- Blank lines separating headers and body

The lab also showed that manually constructing HTTP requests requires attention to syntax and formatting.

---

# 31. Problems Encountered

Several problems were encountered during the lab.

## Burp Request Timeout

One request timed out because the HTTP request did not contain the required blank line after the headers.

This was solved by correctly formatting the HTTP request.

## HTTP Method Confusion

There was also attention around whether the request was actually being sent as GET or another method.

This reinforced the importance of checking the exact HTTP method in Burp Repeater.

## token-1 Returning 403

`token-1` was tested before Esther had logged in.

The request was rejected because the in-memory token store only contained tokens that had actually been generated during the current application session.

This reinforced the difference between a predictable token format and a valid active token.

---

# 32. Burp Evidence

Screenshots were captured as evidence that Burp Suite was used during the lab.

The screenshots serve as supporting evidence for the practical testing process.

The screenshots do not represent every individual step.

The important evidence is that Burp Repeater was used to:

- send API requests
- include Authorization headers
- modify resource IDs
- resend requests
- observe HTTP responses
- verify authorization behavior

---

# 33. Final Application Code

The final application was saved as:

    app.py

The final code was:

    from fastapi import FastAPI, HTTPException, Header
    from pydantic import BaseModel

    class LoginRequest(BaseModel):
        username: str

    app = FastAPI()

    users = {
        1: {
            "name": "Esther", "email": "esther@example.com"
        },
        2: {
            "name": "Bob", "email": "bob@example.com"
        },
        3: {
            "name": "John", "email": "john@example.com"
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

        raise HTTPException(status_code=401, detail="Invalid username")

    @app.get("/users/{user_id}")
    def get_user(user_id: int, authorization: str = Header(None)):
        token = authorization.replace("Bearer ", "")
        logged_in_user = tokens.get(token)

        if logged_in_user != user_id:
            raise HTTPException(status_code=403, detail="Forbidden")
        else:
            return users[user_id]

---

# 34. Lab Folder Structure

The lab was stored as the third lab inside the existing cybersecurity labs repository.

The structure is:

    100-cybersecurity-labs/
    │
    ├── Lab-01-John-the-Ripper/
    │
    ├── Lab-02-Nmap-SimpleHTTPServer/
    │
    └── Lab-03-FastAPI-Auth-Authorization/
        │
        ├── app.py
        ├── notes.md
        │
        └── screenshots/

The `notes.md` file contains the documentation for the lab.

The screenshots folder contains evidence from the Burp Suite testing.

---

# 35. Limitations of the Lab

This application is intentionally a learning application.

It is not production-ready authentication.

Some limitations include:

- No password authentication.
- No database.
- Tokens are predictable.
- Tokens are stored only in memory.
- Tokens do not expire.
- There is no token revocation system.
- There is no refresh-token system.
- There is no HTTPS configuration in the local lab.
- There is no real user-management system.
- Error handling is intentionally simple.
- The authentication model is simplified.

These limitations were intentional because the objective was to understand authentication and authorization fundamentals and practice testing them with Burp Suite.

The lab should not be treated as a secure authentication implementation for a real application.

---

# 36. What Was Actually Tested

The practical testing performed in this lab included:

1. Starting the FastAPI server.
2. Accessing the local API.
3. Creating and testing the `/login` endpoint.
4. Sending JSON login data.
5. Receiving a token.
6. Understanding how the token was stored.
7. Sending the token using the Authorization header.
8. Accessing the authenticated user's resource.
9. Modifying the requested user ID.
10. Sending the modified request through Burp Repeater.
11. Observing the 403 Forbidden response.
12. Testing the behavior of another predictable token.
13. Investigating why an inactive token was rejected.
14. Observing how HTTP request formatting affects Burp requests.

---

# 37. Main Security Lessons

The most important security lessons from this lab were:

## 1. Authentication is not authorization

Knowing who a user is does not automatically mean they are allowed to access every resource.

## 2. The server must enforce authorization

The client should never be trusted to decide what it is allowed to access.

## 3. URLs can be modified

A user can change values such as:

    /users/2

to:

    /users/1

The server must validate whether the requester is allowed to access the new resource.

## 4. Tokens should not be predictable

A token such as:

    token-2

is easy to guess.

Real authentication systems need unpredictable credentials.

## 5. Burp Repeater is useful for testing authorization

Repeater makes it easy to modify HTTP requests and see whether the server properly validates them.

## 6. HTTP details matter

Incorrect headers, missing blank lines, or incorrect methods can cause requests to fail even when the application itself is working.

## 7. HTTP status codes communicate security decisions

401 and 403 are not just numbers.

They communicate different types of failures.

## 8. A token-looking value is not automatically valid

A token must be recognized and accepted by the server.

---

# 38. Final Takeaway

This lab provided hands-on experience with a basic authentication and authorization flow rather than only learning the concepts theoretically.

The process was:

    User logs in
          ↓
    Server identifies user
          ↓
    Server creates token
          ↓
    Token is returned
          ↓
    Client sends token with request
          ↓
    Server identifies logged-in user
          ↓
    Server checks requested resource
          ↓
    Authorization decision
          ↓
    Access granted or denied

The most important lesson was that authentication and authorization are separate security controls.

A user can be successfully authenticated and still be denied access to a resource.

Burp Suite made this distinction practical by allowing the request to be modified while keeping the same authentication token.

Changing the requested resource while keeping Bob's token demonstrated why server-side authorization checks are necessary.

The lab also introduced practical API security testing: rather than assuming that an endpoint is secure because it works normally, requests were deliberately modified to see how the server responded.

This was the main purpose of the lab: to understand how authentication, authorization, HTTP requests, tokens, and access-control decisions work together and to verify those controls through hands-on testing.