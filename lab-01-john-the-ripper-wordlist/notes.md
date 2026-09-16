# Lab 01 — John the Ripper Wordlist Attack

## Objective

Learn how a wordlist/dictionary attack works using John the Ripper against a test SHA-256 password hash.

> This lab was performed in a controlled environment using a password created specifically for practice.

---

## 1. Installing John the Ripper

John the Ripper was installed on Kali Linux.

```bash
sudo apt install john
```

### Verify the installation

```bash
which john
```

Output:

```text
/usr/sbin/john
```

This confirmed that the `john` executable was installed and available in the system PATH.

---

## 2. Exploring John

To see the hash formats supported by John:

```bash
john --list=formats
```

John showed many supported formats, including:

```text
Raw-SHA256
```

I also checked John's available command-line options:

```bash
john --help
```

---

## 3. Creating a Test Password

For this lab, I created a test password:

```text
sunshine123
```

This was only a practice password created for the lab.

---

## 4. Generating the SHA-256 Hash

The password was saved in a file and hashed using:

```bash
sha256sum password.txt
```

SHA-256 does not store the original password. It produces a fixed-length hash based on the input.

The resulting hash was placed in:

```text
hash.txt
```

---

## 5. Creating a Wordlist

A small wordlist was created containing several possible passwords:

```text
password
123456
sunshine123
letmein
qwerty
```

The file was named:

```text
wordlist.txt
```

### Why do we need a wordlist?

The hash itself does not contain the original password in a form that John can simply "turn back into words."

Instead, John takes candidate passwords from the wordlist, hashes each candidate, and compares the resulting hash with the target hash.

The process is:

```text
Candidate password
       ↓
     SHA-256
       ↓
Generated hash
       ↓
Compare with target hash
       ↓
Match?
```

For example:

```text
password       → hash → ❌
123456         → hash → ❌
sunshine123    → hash → ✅
```

---

## 6. Running the Wordlist Attack

The attack was performed with:

```bash
john --format=Raw-SHA256 --wordlist=wordlist.txt hash.txt
```

### Command breakdown

`john`

Starts John the Ripper.

`--format=Raw-SHA256`

Specifies that the target is a raw SHA-256 hash.

`--wordlist=wordlist.txt`

Tells John to use the passwords inside `wordlist.txt` as candidates.

`hash.txt`

Contains the target hash that John is trying to match.

---

## 7. Result

John successfully loaded the hash as:

```text
Raw-SHA256
```

It then tested the candidates in the wordlist.

The password recovered was:

```text
sunshine123
```

John reported:

```text
1g ... DONE
```

The `1g` indicates that one password was successfully cracked.

---

## 8. Showing the Cracked Password

The recovered password was displayed using:

```bash
john --show --format=Raw-SHA256 hash.txt
```

This shows passwords that John has already recovered instead of performing the attack again.

---

## What I Learned

* A hash is not the same thing as the original password.
* A wordlist contains possible password guesses.
* John can hash each candidate and compare it with a target hash.
* `Raw-SHA256` is the appropriate John format for the raw SHA-256 hash used in this lab.
* A dictionary attack depends heavily on the quality of the wordlist.
* If the correct password is not present among the candidates, a basic wordlist attack will not find it.
* Password cracking tools automate the guess → hash → compare process.

## Files

```text
notes.md       → documentation for this lab
wordlist.txt   → practice password candidates
```

The test password file and target hash file were not included in the repository.

