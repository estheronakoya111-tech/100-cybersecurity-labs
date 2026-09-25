100 CYBERSECURITY LABS

A hands-on cybersecurity learning journey focused on building practical skills through labs, experimentation, and documentation.

This repository contains my progress through 100 cybersecurity labs, covering security tools, techniques, networking, analysis, and practical security concepts.

The goal is not just to follow commands, but to understand what each tool does, why it is used, how it works, and what the results mean.


🎯 GOALS

• Build practical cybersecurity skills through hands-on labs
• Learn and apply cybersecurity tools and techniques
• Improve Linux and command-line skills
• Develop security analysis and problem-solving skills
• Understand common cybersecurity concepts through practice
• Document what I learn throughout the journey
• Build a public record of my cybersecurity progress


🧪 LAB STRUCTURE

Each lab has its own folder:

100-cybersecurity-labs/

├── README.md
│
├── lab-01-john-the-ripper-wordlist/
│   ├── notes.md
│   ├── wordlist.txt
│   └── screenshots/
│
├── lab-02/
│   └── notes.md
│
├── lab-03-fastapi-auth-authorization/
│   ├── app.py
│   ├── notes.md
│   └── screenshots/
│
└── ...

Each lab may contain:

• notes.md — documentation of the lab, commands, results, and lessons learned
• Supporting files required for the lab
• Screenshots showing important results

Sensitive information, real credentials, and unnecessary password or hash files will not be uploaded.


🔐 LABS COMPLETED


LAB 01 — JOHN THE RIPPER: WORDLIST ATTACK

Tool: John the Ripper
Technique: Dictionary/Wordlist Attack
Hash: Raw SHA-256

Learned how a wordlist attack works by creating a test SHA-256 password hash and using John the Ripper to test password candidates against it.

Status: ✅ Completed


LAB 02 — KALI NETWORK RECON

Tools: Nmap, curl, ss, Python HTTP Server
Technique: Network Reconnaissance & Web Service Enumeration
Target: Localhost (127.0.0.1)

Used Nmap to discover hosts, scan ports, and identify a local Python web service. Used curl to inspect the web server and discovered unintended directory listing/file exposure.

Fixed the issue by creating a dedicated web directory and verified the fix.

Status: ✅ Completed


LAB 03 — FASTAPI AUTHENTICATION & AUTHORIZATION

Tools: Python, FastAPI, Uvicorn, Burp Suite Repeater
Technique: Authentication & Authorization Testing
Target: Local FastAPI application

Built a simple FastAPI API with a login endpoint, user resources, and token-based authentication.

Used Burp Suite Repeater to manually test HTTP requests, inspect authentication tokens, send Authorization headers, modify resource IDs, and observe access-control behavior.

Tested whether an authenticated user could access another user's resource by changing the requested user ID while keeping the same authentication token.

The API correctly returned 403 Forbidden after authorization was enforced server-side.

Also investigated predictable token generation and reinforced the distinction between authentication and authorization.

Status: ✅ Completed


🛠️ TOOLS & TECHNOLOGIES

Tools used throughout the labs may include:

• Kali Linux
• Python
• FastAPI
• Uvicorn
• Burp Suite
• John the Ripper
• Wireshark
• Nmap
• curl
• ss
• OWASP ZAP
• Linux command-line tools
• Other cybersecurity tools introduced throughout the journey

The tools used will vary depending on the lab.


📚 LEARNING APPROACH

For each lab, I aim to understand:

1. What the tool or technique is
2. Why it is used
3. How it works
4. How to use it in a controlled environment
5. What the results mean
6. What security lesson can be learned from it

This project focuses on hands-on learning and authorized security testing.


📈 PROGRESS

Labs completed: 3 / 100

[█░░░░░░░░░░░░░░░░░░] 3%

More labs coming.


⚠️ DISCLAIMER

All security testing documented in this repository is performed in controlled environments, against systems, accounts, files, and credentials that I own or have explicit permission to test.

This repository is for cybersecurity education, experimentation, and skill development.