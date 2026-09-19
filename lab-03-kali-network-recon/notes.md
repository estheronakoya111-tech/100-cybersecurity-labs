# Lab 02 — Kali Network Recon

## Lab Goal

Practice:

* Checking my Kali network
* Discovering hosts
* Scanning ports
* Identifying services
* Inspecting a web server
* Finding unintended file exposure
* Fixing the issue
* Verifying the fix

**Lab target:** My own Kali Linux VM / localhost

**Main tools:** `ip`, `Nmap`, `ss`, `curl`, Python HTTP server

---

# Part 1 — Check the Kali Network

## Step 1 — Check my IP address

Command:

```bash
ip addr
```

I looked for the `inet` address under my active network interface.

My Kali IP was:

```text
10.0.2.15/24
```

This means my Kali VM was using the `10.0.2.0/24` network.

### Important

`10.0.2.15` = my Kali VM's IP address.

`127.0.0.1` = my own Kali machine through localhost.

These are not the same address, but both refer to my own Kali environment.

---

# Part 2 — Discover Hosts on the Network

## Step 2 — Discover devices/hosts

Command:

```bash
nmap -sn 10.0.2.0/24
```

The scan found:

```text
10.0.2.2
10.0.2.3
10.0.2.15
```

`10.0.2.15` was my Kali VM.

The `.2` and `.3` addresses were related to the VirtualBox NAT network.

### Network Mode

My VirtualBox network adapter was set to:

```text
NAT
```

NAT allows the Kali VM to access the internet through the host computer and creates the `10.0.2.x` virtual network.

---

# Part 3 — Scan My Kali IP

## Step 3 — Try a normal Nmap scan

Command:

```bash
nmap 10.0.2.15
```

The scan was taking too long, so I stopped it using:

```text
Ctrl + C
```

I did not wait for the full scan.

---

## Step 4 — Scan only ports 1–100

Command:

```bash
nmap -p 1-100 10.0.2.15
```

Result:

```text
100 filtered tcp ports (no-response)
```

### Meaning

`filtered` means Nmap could not determine whether the ports were open or closed because it did not receive a useful response.

At this point, there was no useful service to enumerate on the Kali IP.

---

# Part 4 — Check for Listening Services

## Step 5 — Check what is listening

Command:

```bash
sudo ss -tulpn
```

Result:

```text
Netid State Recv-Q Send-Q Local Address:Port Peer Address:Port Process
```

No listening service was shown.

### Why we checked this

We needed something running locally that we could safely scan and investigate.

Since I only had one Kali VM and did not have a second vulnerable machine, we created a small local web-server lab instead of downloading another VM.

---

# Part 5 — Create a Local Web Server

## Step 6 — Start Python's web server

Command:

```bash
python3 -m http.server 8080
```

This started a simple HTTP web server on:

```text
127.0.0.1:8080
```

The server was started while I was in:

```text
/home/kali
```

This became important later.

I opened a second terminal so that I could scan and test the server while it was running.

---

# Part 6 — Scan the Web Server

## Step 7 — Check port 8080

Command:

```bash
nmap -p 8080 127.0.0.1
```

Result:

```text
8080/tcp open http-proxy
```

### Meaning

* `8080` = port number
* `open` = something was accepting connections
* `http-proxy` = Nmap's service-name guess

The `http-proxy` label did **not** mean that the server was actually a proxy.

---

# Part 7 — Identify the Service

## Step 8 — Detect the service and version

Command:

```bash
nmap -sV -p 8080 127.0.0.1
```

Nmap identified:

```text
SimpleHTTPServer 0.6 (Python 3.13.12)
```

### What `-sV` means

`-sV` tells Nmap to try to identify the service and its version.

---

# Part 8 — Inspect the HTTP Server

## Step 9 — Check HTTP headers

Command:

```bash
curl -I http://127.0.0.1:8080
```

The response included information such as:

```text
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.13.12
Content-type: text/html
```

### Observation

The server was revealing its software and Python version.

This is useful information for reconnaissance, although version disclosure by itself does not prove that the server is vulnerable.

---

## Step 10 — View the web page

Command:

```bash
curl http://127.0.0.1:8080
```

Instead of showing only a normal page, the response showed a directory listing.

The listing was for:

```text
/home/kali
```

Some visible filenames included:

```text
.ssh/
.zsh_history
password.txt
hash.txt
wordlist.txt
Downloads/
Projects/
Documents/
```

I did **not** open the contents of those files.

---

# Part 9 — Find Out Why the Files Were Exposed

## Step 11 — Check the current directory

Command:

```bash
pwd
```

Result:

```text
/home/kali
```

### Explanation

Python's simple HTTP server serves the directory from which it was started.

Because the server was started from:

```text
/home/kali
```

it was serving the contents of my entire home directory.

---

# Part 10 — Fix the Problem

## Step 12 — Create a dedicated web directory

Command:

```bash
mkdir ~/web-lab
```

### Meaning

* `mkdir` = create a directory
* `~` = my home directory
* `~/web-lab` = `/home/kali/web-lab`

---

## Step 13 — Create a simple web page

Command:

```bash
echo "Kali Security Lab" > ~/web-lab/index.html
```

### Meaning

This created:

```text
/home/kali/web-lab/index.html
```

containing:

```text
Kali Security Lab
```

The `>` sends the output into the file.

---

## Step 14 — Move into the new directory

Command:

```bash
cd ~/web-lab
```

### Meaning

`cd` = change directory.

I moved from:

```text
/home/kali
```

to:

```text
/home/kali/web-lab
```

---

## Step 15 — Start the server from the new directory

Command:

```bash
python3 -m http.server 8080
```

The server was now serving:

```text
/home/kali/web-lab
```

instead of:

```text
/home/kali
```

---

# Part 11 — Verify the Fix

## Step 16 — Check the page

Command:

```bash
curl http://127.0.0.1:8080
```

Result:

```text
Kali Security Lab
```

The previous directory listing was no longer displayed.

---

## Step 17 — Check the service again

Command:

```bash
nmap -sV -p 8080 127.0.0.1
```

The service was still detected as:

```text
8080/tcp open http SimpleHTTPServer 0.6 (Python 3.13.12)
```

The web server was still working after the fix.

---

# Part 12 — Further HTTP Checks

## Step 18 — Check HTTP title and headers

Command:

```bash
nmap -sV --script http-title,http-headers -p 8080 127.0.0.1
```

The headers showed information including:

```text
Server: SimpleHTTP/0.6 Python/3.13.12
Content-type: text/html
Content-Length: 18
```

This confirmed the server information was still being disclosed.

---

## Step 19 — Test the OPTIONS method

Command:

```bash
curl -i -X OPTIONS http://127.0.0.1:8080
```

Result:

```text
HTTP/1.0 501 Unsupported method ('OPTIONS')
```

### Observation

The server did not support the OPTIONS method.

This was **not treated as a vulnerability**.

---

# Part 13 — Final Verification

## Step 20 — Check the complete HTTP response

Command:

```bash
curl -i http://127.0.0.1:8080/
```

The response included:

```text
HTTP/1.0 200 OK
Server: SimpleHTTP/0.6 Python/3.13.12
Content-type: text/html
Content-Length: 18
```

And the page content was:

```text
Kali Security Lab
```

The web server was working and the unwanted directory listing was gone.

---

# Main Finding

## Directory Listing / Unintended File Exposure

The web server was initially started from:

```text
/home/kali
```

This caused the contents of the home directory to be accessible through the web server.

### Fix

I created a dedicated web directory:

```text
/home/kali/web-lab
```

and started the web server from that directory.

### Result

The server now displayed only the intended page:

```text
Kali Security Lab
```

instead of the contents of `/home/kali`.

---

# Secondary Observation

## Server Version Disclosure

The HTTP response revealed:

```text
SimpleHTTP/0.6 Python/3.13.12
```

This gives information about the software being used.

It was recorded as an observation, not as a confirmed vulnerability.

---

# Full Command List

Commands in the order they were used:

```bash
ip addr

nmap -sn 10.0.2.0/24

nmap 10.0.2.15

nmap -p 1-100 10.0.2.15

sudo ss -tulpn

python3 -m http.server 8080

nmap -p 8080 127.0.0.1

nmap -sV -p 8080 127.0.0.1

curl -I http://127.0.0.1:8080

curl http://127.0.0.1:8080

pwd

mkdir ~/web-lab

echo "Kali Security Lab" > ~/web-lab/index.html

cd ~/web-lab

python3 -m http.server 8080

curl http://127.0.0.1:8080

nmap -sV -p 8080 127.0.0.1

nmap -sV --script http-title,http-headers -p 8080 127.0.0.1

curl -i -X OPTIONS http://127.0.0.1:8080

curl -i http://127.0.0.1:8080/
```

The long-running first Nmap scan was stopped with:

```text
Ctrl + C
```

---

# Quick Reference

### My Kali IP

```text
10.0.2.15
```

### Kali network

```text
10.0.2.0/24
```

### Localhost

```text
127.0.0.1
```

### Web server port

```text
8080
```

### Original web directory

```text
/home/kali
```

### Fixed web directory

```text
/home/kali/web-lab
```

### Web server command

```bash
python3 -m http.server 8080
```

### Main issue

```text
Directory listing / unintended file exposure
```

### Fix

```text
Use a dedicated web directory
```

---

# Lab Flow

**Check Network → Discover → Scan → Check Services → Start Local Server → Enumerate → Inspect → Find → Fix → Verify**
