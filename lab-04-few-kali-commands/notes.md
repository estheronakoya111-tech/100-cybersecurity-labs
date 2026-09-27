

````markdown
# Linux Security Lab

## Goal

This lab is focused on learning Linux fundamentals that are useful for
cybersecurity, system administration, troubleshooting, and security analysis.

The goal is not just to memorize commands, but to understand what the
operating system is doing.

---

# 1. Linux Filesystem

Linux organizes everything under one main directory called `/`.

Unlike Windows, Linux does not normally use drive letters such as `C:` and
`D:` for its filesystem structure.

Some important directories are:

| Directory | Purpose |
|---|---|
| `/` | Root of the entire filesystem |
| `/home` | Personal directories for normal users |
| `/etc` | System and application configuration files |
| `/var` | Data that changes frequently |
| `/var/log` | System and application logs |
| `/tmp` | Temporary files |
| `/usr` | Installed programs and other resources |
| `/root` | Home directory of the root user |
| `/proc` | Information about running processes and the kernel |
| `/dev` | Device files |
| `/boot` | Files needed during system boot |

## Navigation Commands

### `pwd`

`pwd` means **Print Working Directory**.

It shows the directory I am currently inside.

```bash
pwd
````

### `ls`

`ls` lists the contents of the current directory.

```bash
ls
```

### `ls -la`

The `-l` option displays information in a detailed format.

The `-a` option includes hidden files.

```bash
ls -la
```

Linux considers files whose names begin with `.` to be hidden.

Examples:

```text
.config
.bashrc
.gitignore
```

Hidden does not necessarily mean protected.

### `cd`

`cd` means **Change Directory**.

```bash
cd /etc
```

moves into `/etc`.

```bash
cd ..
```

moves to the parent directory.

```bash
cd /
```

moves to the root directory.

---

# 2. Linux File Permissions

Linux uses permissions to control who can read, modify, or execute files.

The three basic permissions are:

* `r` = read
* `w` = write
* `x` = execute

Permissions are applied to three categories:

* `u` = user/owner
* `g` = group
* `o` = others

For example:

```text
-rwxr-xr--
```

can be separated into:

```text
owner   group   others
rwx     r-x     r--
```

The owner has read, write, and execute permission.

The group has read and execute permission.

Others have only read permission.

## `chmod`

`chmod` means **change mode**.

It changes file permissions.

```bash
chmod u+x script.py
```

adds execute permission for the owner.

```bash
chmod u-x script.py
```

removes execute permission from the owner.

Numeric permissions can also be used.

The values are:

```text
read     = 4
write    = 2
execute  = 1
```

Therefore:

```text
7 = rwx
6 = rw-
5 = r-x
4 = r--
```

For example:

```bash
chmod 755 script.py
```

gives:

```text
owner   = rwx
group   = r-x
others  = r-x
```

Another example:

```bash
chmod 600 secret.txt
```

gives the owner read/write permission while removing permissions from the
group and others.

---

# 3. File Ownership

Linux files have an owner and a group.

## `chown`

`chown` means **change owner**.

It changes who owns a file.

```bash
chown esther file.txt
```

Ownership can also include a group:

```bash
chown esther:developers file.txt
```

Changing ownership usually requires elevated privileges.

---

# 4. Inspecting Files

## `stat`

`stat` displays detailed information about a file.

```bash
stat file.txt
```

It can show information such as:

* file size
* permissions
* owner
* group
* timestamps

This is useful when investigating files because metadata can provide
information about how and when a file was modified.

---

# 5. Searching for Files

## `find`

`find` searches for files and directories.

```bash
find /home -type f
```

finds regular files under `/home`.

```bash
find /home -type d
```

finds directories.

```bash
find /home -name "*.py"
```

finds Python files.

An important distinction:

```text
find → searches for files/directories
grep → searches inside files
```

---

# 6. Searching Inside Files

## `grep`

`grep` searches text inside files.

For example:

```bash
grep "failed" login.log
```

This searches `login.log` for lines containing the word `failed`.

This is particularly useful in cybersecurity because logs can contain
large amounts of information.

For example, I could search authentication logs for:

```text
failed
login
error
unauthorized
```

---

# 7. Reading Logs

## `tail`

`tail` displays the end of a file.

```bash
tail login.log
```

This is useful for logs because the newest entries are often near the end
of the file.

### `tail -f`

```bash
tail -f login.log
```

The `-f` option means **follow**.

Instead of showing the file once and stopping, it continues displaying new
lines as they are added.

This is useful for monitoring a log while something is happening.

---

# 8. Processes

A **process** is a program that is currently running.

Every process has a **PID (Process ID)**.

## `ps`

`ps` means **Process Status**.

```bash
ps aux
```

This displays running processes.

We also used:

```bash
ps aux --sort=-%cpu | head
```

This helped us identify processes using the most **CPU (Central Processing
Unit)**.

We investigated a Chromium process using:

```bash
ps -p 3122 -f
```

This displayed detailed information about that particular process.

We learned about:

* PID = Process ID
* PPID = Parent Process ID
* CPU usage
* memory usage
* process start time
* command being executed

## `kill`

`kill` sends a signal to a process.

For example:

```bash
kill 3122
```

was used during the lab to terminate a specific Chromium process.

A process can be part of a larger application, so killing one process does
not necessarily close the entire application.

---

# 9. Networking

## `ping`

`ping` tests whether a host can be reached and measures how long responses
take.

For example:

```bash
ping google.com
```

We also tested:

```bash
ping 8.8.8.8
```

`8.8.8.8` is a public **DNS (Domain Name System)** server operated by
Google.

`ping` uses **ICMP (Internet Control Message Protocol)**.

Some information shown in the output includes:

* `icmp_seq` = ICMP sequence number
* `ttl` = Time To Live
* `time` = round-trip response time
* packet loss

We also learned that `ping` does not necessarily mean "is the internet
working?"

For example:

```bash
ping 127.0.0.1
```

can work without an internet connection because `127.0.0.1` is the local
loopback address.

---

# 10. Traceroute

```bash
traceroute google.com
```

`traceroute` attempts to show the network hops between my machine and a
destination.

A hop is normally a router or other network device involved in forwarding
traffic.

We saw:

```text
1  10.0.2.2
2  * * *
3  * * *
```

The first hop was the virtual network gateway used by my Kali virtual
machine.

The `* * *` entries mean that the probes did not receive a response.

This does not automatically mean that the network device is down.
Devices or firewalls can simply refuse to respond to traceroute probes.

---

# 11. Network Interfaces

On Linux, I used:

```bash
ip addr
```

to inspect network interfaces and addresses.

My Kali virtual machine had:

```text
lo
eth0
```

`lo` is the loopback interface.

Its address:

```text
127.0.0.1
```

refers back to the same machine.

`eth0` is the network interface used by my Kali virtual machine.

The machine had an address similar to:

```text
10.0.2.15/24
```

This is a private **IPv4 (Internet Protocol version 4)** address.

The `/24` represents the network prefix.

The interface also had a **MAC (Media Access Control)** address.

Because Kali was running inside VirtualBox, the network interface and
address were part of the virtual machine's network environment.

---

# 12. Network Sockets

## `ss`

`ss` means **Socket Statistics**.

It can show network sockets and listening services.

We used:

```bash
ss -ltnp
```

The options mean:

```text
-l = listening
-t = TCP (Transmission Control Protocol)
-n = numeric addresses and ports
-p = show the process using the socket
```

We specifically used:

```bash
ss -ltnp | grep 9999
```

because Autopsy reported that it was using port `9999`.

The command returned no output.

That meant there was no TCP service listening on port `9999` at that
moment, which helped us investigate why the Autopsy web interface was
refusing the connection.

---

# 13. Shell Scripts

A file ending in `.sh` is commonly used for a **shell script**.

A shell is a program that allows a user to interact with the operating
system by entering commands.

On Kali Linux, a commonly used shell is **Bash (Bourne Again SHell)**.

For example:

```bash
#!/bin/bash

pwd
ls -la
echo "Linux practice"
```

The purpose of `commands.sh` in this lab is to keep a record of the Linux
commands I practiced.

---

# What I Learned

The main concepts covered in this lab were:

* Linux filesystem structure
* Navigating directories
* Hidden files
* File permissions
* File ownership
* File metadata
* Searching for files
* Searching inside files
* Reading and monitoring logs
* Processes and PIDs
* Terminating processes
* Basic network troubleshooting
* Internet Protocol addresses
* Network interfaces
* Network hops
* Listening ports and sockets
* Shell scripts

These concepts form a foundation for later cybersecurity work involving
Linux systems, network analysis, logs, services, and security
investigations.

```
```
