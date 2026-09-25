# Lab 03 — FastAPI Authentication & Authorization

## Overview

This lab was focused on understanding how authentication and authorization work in a simple FastAPI application.

I built a small API that allows users to log in, receive a token, and then use that token when making requests to protected user resources.

I also used Burp Suite Repeater to inspect, modify, and resend HTTP requests. This helped me understand how authentication information is actually sent through HTTP headers and how authorization can be tested by changing the requested resource or token.

The application was intentionally simple. The goal was not to build production-ready authentication, but to understand the basic flow and see how authentication and authorization can be tested.

---

## Objectives

The main things I wanted to understand from this lab were:

- How FastAPI creates API routes.
- How `GET` and `POST` requests work.
- How request bodies are received using Pydantic models.
- The difference between authentication and authorization.
- How a login request can create a token.
- How a token can be stored and checked on later requests.
- How the `Authorization` HTTP header is used.
- How a server decides whether a user is allowed to access a resource.
- How `403 Forbidden` is returned when authorization fails.
- How Burp Suite Repeater can be used to inspect and modify requests.
- How predictable authentication tokens can create a security weakness.

---

## Technologies Used

- Python
- FastAPI
- Uvicorn
- Pydantic
- Burp Suite
- HTTP
- VS Code

---

## 1. Creating the FastAPI Application

The first step was creating the basic FastAPI application.

The application object is created using `FastAPI()`:

```python
from fastapi import FastAPI

app = FastAPI()
```

`app` is the main FastAPI application instance. I use it to create routes that the API can respond to.

For example:

```python
@app.get("/")
def home():
    return {"message": "API is running"}
```

The `@app.get("/")` part tells FastAPI that this function should run when a `GET` request is made to `/`.

I started the application with:

```bash
uvicorn app:app --reload
```

The first `app` refers to the Python file `app.py`.

The second `app` refers to the FastAPI application object created inside that file:

```python
app = FastAPI()
```

The `--reload` option makes Uvicorn restart the server automatically when I make changes to the code.

The API was available at:

```text
http://127.0.0.1:8000
```

---

## 2. Understanding API Routes

A route defines what the server should do when a particular HTTP request is received.

For example:

```python
@app.get("/")
def home():
    return {"message": "API is running"}
```

This means:

```text
GET /
```

calls the `home()` function.

Another route can be created for a specific user:

```python
@app.get("/users/{user_id}")
def get_user(user_id: int):
    ...
```

The `{user_id}` part is a path parameter.

For example:

```text
/users/1
/users/2
/users/3
```

would give the server different values for `user_id`.

The `: int` tells FastAPI that the value should be treated as an integer.

---

## 3. GET and POST Requests

During the lab I worked with both `GET` and `POST` requests.

### GET

A `GET` request is normally used when retrieving information.

For example:

```http
GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
```

This asks the server for information about user `2`.

### POST

A `POST` request is commonly used when sending information to the server.

The login endpoint used a `POST` request because the client needs to send a username to the server.

Example:

```http
POST /login HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
    "username": "Bob"
}
```

The blank line between the headers and the JSON body is important.

The HTTP request is separated into different sections:

```text
Request line
Headers

Body
```

The empty line tells the server that the headers have ended and the request body begins.

I noticed this while working with Burp Suite because an incomplete HTTP request could cause Burp to complain about an incomplete header block.

---

## 4. Creating the Login Request Model

I used Pydantic to define what the login request should look like.

The model was:

```python
class LoginRequest(BaseModel):
    username: str
```

This tells FastAPI that the request body should contain a `username` field and that the value should be a string.

For example:

```json
{
    "username": "Bob"
}
```

The request can then be sent to:

```text
POST /login
```

FastAPI uses the Pydantic model to read and validate the incoming request data.

This is useful because I don't have to manually extract the JSON value from the request.

---

## 5. Authentication vs Authorization

One of the main concepts in this lab was understanding the difference between authentication and authorization.

### Authentication

Authentication answers:

> Who are you?

For this simple lab, the username was used to identify the user.

For example:

```text
Bob
```

was identified as user ID:

```text
2
```

After a successful login, the server generated a token for that user.

### Authorization

Authorization answers:

> What are you allowed to access?

A user can be authenticated but still not be authorized to access another user's information.

For example, Bob can be logged in successfully, but that does not automatically mean Bob should be able to request:

```text
/users/1
```

if `/users/1` belongs to Esther.

The server therefore needs to check both things:

1. Is the request associated with a logged-in user?
2. Is that user allowed to access the requested resource?

---

## 6. Creating the Token Storage

For this lab, I used a simple Python dictionary to store tokens.

```python
tokens = {}
```

The dictionary stores the relationship between a token and the user ID.

The basic idea is:

```text
token → user ID
```

For example:

```text
token-2 → 2
```

This means that `token-2` belongs to user ID `2`.

This is only an in-memory demonstration. It is not a proper production authentication system.

If the application is restarted, the dictionary is cleared and the previously stored tokens disappear.

---

## 7. Logging In

The login process starts when the user sends a username.

For example:

```json
{
    "username": "Bob"
}
```

The server checks whether the username exists.

Bob's user ID was:

```text
2
```

The application then created a token using:

```python
token = f"token-{user_id}"
```

For Bob, this becomes:

```text
token-2
```

The token was then stored:

```python
tokens[token] = user_id
```

So the dictionary now contains something similar to:

```python
{
    "token-2": 2
}
```

The login response included information similar to:

```json
{
    "message": "Login successful",
    "user_id": 2,
    "token": "token-2"
}
```

The important part of this process is that the server remembers which user the token belongs to.

---

## 8. Using the Token

After logging in, the token can be included in another request.

The token was sent using the HTTP `Authorization` header.

The format used was:

```http
Authorization: Bearer token-2
```

A complete request looked like:

```http
GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

```

The word `Bearer` indicates that the client is presenting a token to the server as proof of authentication.

The server then needs to extract the actual token.

The code used:

```python
token = authorization.replace("Bearer ", "")
```

If the header contains:

```text
Bearer token-2
```

the extracted token becomes:

```text
token-2
```

The server can then check whether that token exists.

---

## 9. Checking the Token

The server looks up the token in the token dictionary:

```python
logged_in_user = tokens.get(token)
```

For example, if:

```text
token = token-2
```

and the dictionary contains:

```python
{
    "token-2": 2
}
```

then:

```text
logged_in_user = 2
```

This tells the server that the request is associated with user ID `2`.

If the token is not found, the server knows that it does not have a valid logged-in session for that token.

This is the basic authentication check used in the lab.

---

## 10. Authorization Check

After authentication, the server also needs to check authorization.

Suppose Bob is user ID `2`.

Bob can request:

```text
/users/2
```

because the requested resource belongs to user ID `2`.

But if Bob tries:

```text
/users/1
```

the server should not allow the request if user ID `1` belongs to another user.

The authorization check was:

```python
if logged_in_user != user_id:
    raise HTTPException(
        status_code=403,
        detail="Forbidden"
    )
```

The server compares:

```text
logged_in_user
```

with:

```text
user_id
```

If they are different, the request is rejected.

For example:

```text
Logged-in user: 2
Requested user: 1
```

Because:

```text
2 != 1
```

the server returns:

```text
403 Forbidden
```

This is an authorization failure.

---

## 11. Understanding 403 Forbidden

The response:

```text
403 Forbidden
```

means that the server understood the request but is refusing to allow access.

In this lab, a `403` was returned when Bob attempted to access another user's resource.

This helped demonstrate the difference between authentication and authorization.

Being logged in does not automatically mean a user can access everything.

---

## 12. Testing the API with Burp Suite

I used Burp Suite to inspect and manipulate the HTTP requests sent to the FastAPI application.

Burp Suite was useful because it allowed me to see the request in a form similar to what the server actually receives.

For example, I could inspect:

```http
GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

```

I could then modify parts of the request and resend it.

This is useful for security testing because I can test whether the server is relying on something that the client is allowed to change.

---

## 13. Using Burp Repeater

I used Burp Suite Repeater to resend modified requests.

The general process was:

1. Capture or obtain a request.
2. Send the request to Repeater.
3. Modify part of the request.
4. Send it again.
5. Observe the response.
6. Compare the result with the original request.

For example, I could change:

```http
GET /users/2 HTTP/1.1
```

to:

```http
GET /users/1 HTTP/1.1
```

while keeping Bob's token:

```http
Authorization: Bearer token-2
```

This allowed me to test whether the server would incorrectly trust the token without checking which resource Bob was requesting.

---

## 14. Authorization Test

The authorization test was successful.

I logged in as Bob and received:

```text
token-2
```

I then used that token to request Bob's resource:

```http
GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

```

The request was allowed because:

```text
logged_in_user = 2
user_id = 2
```

The values matched.

I then changed the requested resource:

```http
GET /users/1 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

```

Now the values were:

```text
logged_in_user = 2
user_id = 1
```

They did not match.

The server therefore returned:

```text
403 Forbidden
```

This showed that the authorization check was actually being enforced on the server.

---

## 15. Testing a Different Token

I also tested what would happen if I replaced Bob's token:

```text
token-2
```

with:

```text
token-1
```

while requesting:

```text
/users/1
```

At first, this still returned an authorization failure.

The reason was important.

I had not logged in as Esther during that test, so:

```text
token-1
```

had never been added to the `tokens` dictionary.

The server therefore had no record connecting:

```text
token-1
```

to user ID `1`.

This showed why the token dictionary matters. The server does not simply trust the format of the token. It checks whether the token actually exists in its stored authentication state.

---

## 16. Predictable Token Weakness

One security weakness I identified was the way the tokens were generated.

The token was created using:

```python
token = f"token-{user_id}"
```

This means the token is directly based on the user's ID.

For example:

```text
User 1 → token-1
User 2 → token-2
User 3 → token-3
```

This is predictable.

A real authentication token should not be something that an attacker can easily guess by knowing or changing a user ID.

For a real application, tokens should be generated using a secure random mechanism and should have proper session management.

This lab intentionally used a simple token format so that the authentication flow could be understood easily.

---

## 17. Why Predictable Tokens Are a Problem

If an application used predictable tokens in a real environment, an attacker might be able to guess another token.

The important problem is not simply that the token contains a user ID.

The larger issue is that the token does not contain enough randomness to make guessing difficult.

A production authentication system would normally need things such as:

- Securely generated session tokens.
- Token expiration.
- Token revocation.
- HTTPS.
- Proper credential handling.
- Secure session storage.
- Protection against token theft.
- Appropriate authorization checks.

The simple token used in this lab should therefore be treated as a learning example, not a secure authentication implementation.

---

## 18. Authentication Flow

The authentication flow I built can be summarized as:

```text
User sends username
        ↓
POST /login
        ↓
Server finds the user
        ↓
Server creates token
        ↓
Token is stored with the user ID
        ↓
Token is returned to the client
        ↓
Client sends token in Authorization header
        ↓
Server extracts token
        ↓
Server looks up token
        ↓
Server identifies logged-in user
```

After authentication, authorization is checked:

```text
User requests a resource
        ↓
Server checks logged-in user
        ↓
Server compares logged-in user with requested resource
        ↓
If they match → allow access
If they do not match → 403 Forbidden
```

This helped me understand that authentication and authorization are separate steps.

---

## 19. Important HTTP Concepts I Learned

One thing I became more comfortable with during this lab was the structure of an HTTP request.

A simplified request looks like:

```http
GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2

```

The first line contains:

```text
HTTP method + path + HTTP version
```

The next lines are headers.

For example:

```text
Host:
Authorization:
Content-Type:
```

Then there is a blank line.

If the request has a body, the body comes after the blank line.

For example:

```http
POST /login HTTP/1.1
Host: 127.0.0.1:8000
Content-Type: application/json

{
    "username": "Bob"
}
```

Understanding this made it easier to understand what Burp Suite was showing me.

---

## 20. What I Learned From Burp Suite

Before this lab, HTTP requests could look like something abstract happening behind the application.

Using Burp Repeater helped me see that the client is actually sending specific information to the server.

For example, I could manually change:

```text
HTTP method
URL path
Authorization header
Request body
```

and then observe how the server responded.

This is important for security testing because anything sent by the client should generally be treated as untrusted input.

The server must perform its own validation and authorization checks instead of assuming that the client will behave correctly.

---

## 21. Security Lesson From the Authorization Test

The authorization test demonstrated an important security principle:

> Authorization must be enforced on the server.

Changing:

```text
/users/2
```

to:

```text
/users/1
```

was easy because the client controls the request.

The important part was that the server did not simply return the requested user's data.

Instead, it compared the authenticated user's ID with the requested user ID.

```python
if logged_in_user != user_id:
    raise HTTPException(
        status_code=403,
        detail="Forbidden"
    )
```

This prevented Bob's token from being used to access Esther's resource.

---

## 22. Limitations of This Lab

This application was intentionally simplified, so it does not represent a complete production authentication system.

The lab did not implement:

- Password authentication.
- Password hashing.
- Secure random session tokens.
- Token expiration.
- Refresh tokens.
- Token revocation.
- Persistent session storage.
- Database-backed authentication.
- HTTPS configuration.
- Secure cookies.
- Rate limiting.
- Multi-factor authentication.
- Account lockout.
- Production-grade credential management.

The `tokens = {}` dictionary is also temporary because it exists only while the Python application is running.

If the server restarts, the stored tokens disappear.

---

## 23. What I Would Improve in a Real Application

If I were turning this into a real application, I would replace the simple authentication system with a more secure design.

Some improvements would include:

```text
Secure password storage
        ↓
Secure login process
        ↓
Cryptographically secure session/token generation
        ↓
Token expiration
        ↓
Token revocation
        ↓
HTTPS
        ↓
Server-side authorization checks
        ↓
Rate limiting and additional security controls
```

I would also store user and session information in a proper database instead of keeping everything in a Python dictionary.

The goal would be to make the system resistant to token guessing, token theft, unauthorized access, and other common authentication problems.

---

## 24. Evidence Collected

I used screenshots as evidence of the testing process.

The evidence included:

- FastAPI application running.
- Successful login request.
- Login response containing the generated token.
- Authenticated request using the `Authorization` header.
- Burp Repeater request.
- Modified user ID in the request.
- `403 Forbidden` response when Bob attempted to access another user's resource.
- Testing of a different token.

These screenshots help show that the API was not only written but actually tested.

---

## 25. Final Result

By the end of the lab, I had built and tested a simple FastAPI API with authentication and authorization.

The application could:

- Accept a login request.
- Identify a user.
- Generate a token.
- Store the token with the user's ID.
- Accept the token through the `Authorization` header.
- Identify the logged-in user from the token.
- Check whether the user was allowed to access a requested resource.
- Return `403 Forbidden` when authorization failed.

I also used Burp Suite Repeater to modify requests and verify that the authorization check was actually being enforced by the server.

The lab also helped me identify a weakness in the implementation: the authentication tokens were predictable because they were based directly on user IDs.

---

## 26. Main Takeaways

The most important things I took from this lab are:

- Authentication determines who the user is.
- Authorization determines what the authenticated user can access.
- HTTP headers can carry authentication information.
- The `Authorization` header can be used to send a bearer token.
- The server should never blindly trust values coming from the client.
- Authorization checks must happen on the server.
- Burp Suite can be used to inspect and modify HTTP requests.
- A successful login does not mean the user should have access to every resource.
- Predictable tokens are not suitable for real authentication systems.
- A simple working authentication demo is different from production-ready authentication.

This lab gave me a better understanding of what happens behind an API request and how authentication and authorization can be tested from a security perspective.
