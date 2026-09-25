Lab 03 — FastAPI Authentication & Authorization

Overview

This lab focused on understanding and testing authentication and authorization in a simple FastAPI API.

I built a small API that included:

- User data
- A login endpoint
- Token-based authentication
- A protected user endpoint
- Server-side authorization checks

I then used Burp Suite to inspect, modify, and resend HTTP requests to see how the API responded to different requests.

The goal of this lab was not to build production-ready authentication. The goal was to understand what happens behind a basic authentication flow and how authorization can be tested from the HTTP request level.

---

Objectives

By the end of the lab, I wanted to understand:

- The difference between authentication and authorization
- How FastAPI handles routes and requests
- How "POST" requests can be used for login
- How "GET" requests can be used to retrieve protected resources
- How authentication tokens are created and stored
- How tokens are sent through HTTP headers
- How the backend identifies the authenticated user
- How server-side authorization prevents unauthorized access
- How Burp Suite can be used to inspect and modify HTTP requests
- How predictable token generation creates a security weakness
- Why a working authentication system can still be insecure

---

Technologies Used

- Python
- FastAPI
- Pydantic
- Uvicorn
- Burp Suite
- Kali Linux

---

1. Creating the FastAPI Application

I created a small FastAPI application with a few users:

- Esther — user ID "1"
- Bob — user ID "2"
- John — user ID "3"

The application also contains a dictionary called "tokens".

tokens = {}

The dictionary is used to keep track of which authentication token belongs to which user.

For example:

token-1 → user 1
token-2 → user 2
token-3 → user 3

The application was started with:

uvicorn app:app --reload

The API was available locally at:

http://127.0.0.1:8000

The "--reload" option makes Uvicorn automatically restart the application when changes are made to the Python code. This is useful during development.

---

2. FastAPI and Python Concepts Learned

"FastAPI()"

The application starts with:

app = FastAPI()

"FastAPI()" creates the FastAPI application.

The variable "app" represents the application instance that Uvicorn runs.

---

Routes

A route connects an HTTP method and URL path to a Python function.

For example:

@app.get("/")
def home():
    return {"message": "API is running"}

This means that when the server receives:

GET /

FastAPI calls the "home()" function.

The decorator:

@app.get("/")

tells FastAPI which HTTP method and path should trigger the function.

---

3. HTTP Methods

I worked with both "GET" and "POST" requests during this lab.

GET

"GET" is generally used to request or retrieve information.

Example:

GET /users/2

This asks the server for the resource associated with user "2".

---

POST

"POST" is generally used to send data to the server or perform an operation.

Example:

POST /login

The login request sends information to the server so that the server can identify the user and create an authentication token.

---

Why the Method Matters

I initially noticed that visiting "/login" directly in a browser does not perform the same operation as sending a login request from the API.

A browser normally makes:

GET /login

But the API expects:

POST /login

Therefore:

GET /login

and:

POST /login

are two different requests.

The HTTP method is part of how the API determines what operation the client is trying to perform.

---

4. Pydantic Model

I created a Pydantic model for the login request:

class LoginRequest(BaseModel):
    username: str

This defines the structure of the data expected by the "/login" endpoint.

A request body can look like:

{
    "username": "Bob"
}

FastAPI uses the Pydantic model to validate and structure the incoming data.

One Python concept I learned here was that:

class LoginRequest(BaseModel):

creates a class/model.

It is not a function.

The model describes the type and structure of data that the endpoint expects.

---

5. Authentication vs Authorization

One of the main concepts I learned during this lab was the difference between authentication and authorization.

Authentication

Authentication answers:

«Who are you?»

In this lab, the "/login" endpoint is responsible for the initial authentication process.

The user provides a username and the server identifies the corresponding user.

After the user is identified, the server creates a token associated with that user.

---

Authorization

Authorization answers:

«What are you allowed to access?»

After authentication, the "/users/{user_id}" endpoint checks whether the authenticated user is allowed to access the requested resource.

For example:

Authenticated user → 2
Requested resource → /users/2

The request can be allowed.

But:

Authenticated user → 2
Requested resource → /users/1

should be denied when the API only allows users to access their own resource.

This showed me that being authenticated does not automatically mean that a user is authorized to access everything.

---

6. Testing "/login"

The login endpoint uses:

POST /login

The request body was:

{
    "username": "Bob"
}

The server returned a response similar to:

{
    "message": "Login successful",
    "user_id": 2,
    "token": "token-2"
}

The basic flow was:

POST /login
      ↓
Server identifies user
      ↓
Token is created
      ↓
Token is returned to the client

This was my first practical look at how a basic token-based authentication flow works.

---

7. Understanding the Token

The token in this lab was created using:

token = f"token-{user_id}"

The token was then associated with the user's ID:

tokens[token] = user_id

For example:

token-1 → 1
token-2 → 2
token-3 → 3

The "tokens" dictionary therefore acts as a simple in-memory mapping between authentication tokens and users.

This is only a learning implementation.

It is not a secure production authentication system.

---

8. Using the Token

After logging in as Bob, I used his token to access his user endpoint.

The request looked like:

GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2


The "Authorization" header carries the authentication credential.

The word:

Bearer

indicates that the token following it is being presented as the authentication credential.

The server extracts the token:

token = authorization.replace("Bearer ", "")

It then looks up the user associated with that token:

logged_in_user = tokens.get(token)

For Bob:

token-2 → 2

Therefore, the server can determine that the request is authenticated as user "2".

---

9. Understanding HTTP Headers

During the Burp testing, I also learned more about HTTP headers.

For example:

Host: 127.0.0.1:8000
Authorization: Bearer token-2

The "Host" header identifies the destination host and port.

The "Authorization" header contains the authentication information being sent with the request.

I also learned that HTTP requests have a separation between the headers and the request body.

A blank line marks the end of the headers.

For example:

GET /users/2 HTTP/1.1
Host: 127.0.0.1:8000
Authorization: Bearer token-2


While working with Burp, I accidentally created an incomplete HTTP request without the proper separation between the header section and the rest of the request.

Burp warned that the HTTP header block was incomplete, which helped me understand that the structure of the request itself matters.

---

10. Using Burp Suite

I used Burp Suite to inspect and manipulate the HTTP requests sent to my FastAPI application.

Burp Repeater was particularly useful because it allowed me to modify a request and send it again without having to repeat the original browser interaction.

I used Burp to:

- Inspect login requests
- Inspect authenticated requests
- Change HTTP methods
- Modify URL paths
- Modify the "Authorization" header
- Resend requests
- Observe HTTP status codes
- Test authorization behavior

This made it possible to test what the backend actually enforced instead of only looking at what the frontend displayed.

---

11. Testing GET vs POST

The login flow used:

POST /login

After receiving the token, the protected resource was accessed using:

GET /users/2

The overall flow was:

POST /login
      ↓
Receive token
      ↓
GET /users/2
      ↓
Send token with request
      ↓
Receive protected resource

This helped me understand that different endpoints can use different HTTP methods depending on the operation they perform.

---

12. Authorization Test

After successfully accessing Bob's information using:

GET /users/2
Authorization: Bearer token-2

I changed the requested resource from:

/users/2

to:

/users/1

I kept Bob's token:

Authorization: Bearer token-2

The server returned:

403 Forbidden

The important part of the test was:

Authenticated user = 2
Requested user     = 1

The server recognized the request as authenticated, but the authenticated user was not authorized to access that resource.

This demonstrated server-side authorization.

---

13. Why the "403" Happened

The authorization check in the API is:

if logged_in_user != user_id:
    raise HTTPException(
        status_code=403,
        detail="Forbidden"
    )

The logic is essentially:

If the authenticated user's ID
does not match the requested user's ID
        ↓
Deny access

So when Bob's token was used to request Esther's resource:

logged_in_user = 2
user_id = 1

The values were different, so the server returned:

403 Forbidden

This is important because authorization must be enforced by the backend.

A frontend should not be relied upon to simply hide another user's data.

If the backend does not enforce the permission check, an attacker can potentially bypass the frontend and send the request directly.

---

14. Testing "token-1"

I also tested whether I could simply change Bob's token:

token-2

to:

token-1

while requesting:

/users/1

The result was also:

403 Forbidden

At first, this needed some explanation.

The problem was not that "token-1" was inherently an invalid token.

At that point in the lab, I had only logged in as Bob.

Therefore, the server's "tokens" dictionary contained something similar to:

token-2 → 2

It did not yet contain:

token-1 → 1

because Esther had not logged in and caused that token to be added.

This helped me understand that the token lookup depends on the current state of the server.

The token only becomes recognized by this simple application after it has been created and stored.

---

15. Predictable Token Design

The lab also revealed a security weakness in the way the tokens were generated.

The application creates tokens using:

token = f"token-{user_id}"

This means that the token can be predicted from the user's ID.

For example:

User 1 → token-1
User 2 → token-2
User 3 → token-3

That is not secure authentication.

If authentication credentials can be easily guessed from publicly known or predictable information, an attacker may be able to impersonate users if the rest of the system does not provide additional protection.

Real authentication systems use securely generated, unpredictable credentials or tokens.

Depending on the authentication design, they may also include:

- Token expiration
- Token revocation
- Secure session management
- Strong credential handling
- HTTPS
- Additional validation and protections

The predictable token design was intentional in this lab because it made the authentication flow easier to understand.

---

16. Complete Authentication Flow

The complete authentication flow implemented in the lab was:

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
Token is returned to client
        ↓
Client sends token with protected request
        ↓
Server identifies authenticated user
        ↓
Server checks authorization
        ↓
Resource is returned
or access is denied

This helped connect the different concepts I had learned into one complete flow.

---

17. Security Testing Flow

My Burp Suite testing followed this process:

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
Server compares user IDs
      ↓
403 Forbidden

The important observation was that the backend did not simply trust the requested URL.

It checked whether the authenticated user was actually allowed to access that resource.

---

18. Important Security Concepts Learned

Authentication

The process of verifying or establishing the identity of a user.

In this lab, the login process identified the user and issued a token.

---

Authorization

The process of determining what an authenticated user is allowed to access.

In this lab, the server checked whether the authenticated user's ID matched the requested user ID.

---

HTTP Methods

Different HTTP methods represent different types of operations.

In this lab:

GET  → retrieve information
POST → send data / perform an operation

---

HTTP Headers

Headers contain additional information about an HTTP request or response.

The "Authorization" header was particularly important in this lab.

---

Authorization Header

The "Authorization" header was used to send the bearer token:

Authorization: Bearer token-2

---

Bearer Token

A bearer token is a credential that is presented with a request to prove that the requester has an authenticated token.

The important security idea is that whoever possesses a bearer token may be able to use it as the credential, which is why real tokens must be protected.

---

HTTP "401"

A "401 Unauthorized" response generally means that authentication is missing or invalid.

It is commonly associated with situations where the server cannot establish a valid authenticated identity.

---

HTTP "403"

A "403 Forbidden" response indicates that the server understood the request but is refusing to allow access to the requested resource.

In this lab, the "403" occurred because the authenticated user was not authorized to access another user's resource.

---

Server-Side Authorization

Permissions should be checked by the backend.

The frontend should not be treated as the security boundary.

A user can potentially bypass frontend restrictions by sending requests directly to the API.

---

Burp Repeater

Burp Repeater allows HTTP requests to be modified and resent repeatedly.

This makes it useful for testing how an application responds when parts of a request are changed.

---

Predictable Credentials

Authentication credentials should not be derived from easily predictable information such as user IDs.

The token design in this lab demonstrated why real authentication systems need unpredictable credentials.

---

19. Key Takeaways

This lab helped me understand that:

- Authentication and authorization are different security controls.
- Being authenticated does not automatically mean a user can access every resource.
- HTTP methods are part of how an API defines its operations.
- "POST" was used for the login operation.
- "GET" was used to retrieve a protected resource.
- Authentication information can be sent through HTTP headers.
- A bearer token can be used to identify an authenticated user.
- Burp Suite can be used to inspect and manipulate HTTP requests.
- Burp Repeater makes it easier to modify and resend requests.
- Authorization needs to be enforced on the server.
- A frontend restriction is not enough to protect backend resources.
- A "403 Forbidden" response can show that the backend rejected an authenticated user who was not authorized for the requested resource.
- A system can technically have authentication while still having a weak authentication implementation.
- Predictable tokens are insecure because they can be derived from predictable information.
- The state of the server matters when working with an in-memory token store.
- Simple lab authentication should not be confused with production-grade authentication.

---

20. Limitations

This application was intentionally simplified for learning.

It does not implement:

- Password authentication
- Secure random token generation
- Token expiration
- Refresh tokens
- Token revocation
- Persistent session storage
- Database-backed authentication
- Production-grade authentication
- HTTPS configuration
- Secure cookie-based sessions
- Full credential management

The purpose of this lab was to understand the underlying concepts and practice testing them with Burp Suite rather than to create a complete authentication system.

---

21. Evidence

Screenshots from Burp Suite were captured during the lab.

The screenshots show the HTTP requests and responses involved in the testing, including:

- Login requests
- Authentication tokens
- Authenticated requests
- Modified resource paths
- "403 Forbidden" responses

The screenshots serve as evidence of the practical testing performed during the lab.

---

22. Result

I successfully built and tested a small FastAPI API with a basic authentication flow and server-side authorization.

I used Burp Suite to inspect and manipulate authenticated requests.

The main authorization test involved logging in as Bob, using Bob's token to access his resource, and then changing the requested resource to another user's resource while keeping Bob's token.

The server returned:

403 Forbidden

because the authenticated user's ID did not match the requested user's ID.

The lab also exposed a predictable-token weakness in the simplified authentication design.

Overall, the lab gave me practical experience with:

FastAPI
   ↓
HTTP requests
   ↓
Authentication
   ↓
Bearer tokens
   ↓
Authorization
   ↓
Burp Suite testing
   ↓
Security weaknesses

This was my first practical exercise connecting API development with security testing at the HTTP request level.
