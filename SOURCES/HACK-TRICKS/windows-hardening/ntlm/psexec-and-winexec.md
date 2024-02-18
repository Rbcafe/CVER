# PsExec/Winexec/ScExec

<details>

<summary><strong>Learn AWS hacking from zero to hero with</strong> <a href="https://training.hacktricks.xyz/courses/arte"><strong>htARTE (HackTricks AWS Red Team Expert)</strong></a><strong>!</strong></summary>

Other ways to support HackTricks:

* If you want to see your **company advertised in HackTricks** or **download HackTricks in PDF** Check the [**SUBSCRIPTION PLANS**](https://github.com/sponsors/carlospolop)!
* Get the [**official PEASS & HackTricks swag**](https://peass.creator-spring.com)
* Discover [**The PEASS Family**](https://opensea.io/collection/the-peass-family), our collection of exclusive [**NFTs**](https://opensea.io/collection/the-peass-family)
* **Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f) or the [**telegram group**](https://t.me/peass) or **follow** us on **Twitter** 🐦 [**@carlospolopm**](https://twitter.com/hacktricks_live)**.**
* **Share your hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.

</details>

## How do they work

The process is outlined in the steps below, illustrating how service binaries are manipulated to achieve remote execution on a target machine via SMB:

1. **Copying of a service binary to the ADMIN$ share over SMB** is performed.
2. **Creation of a service on the remote machine** is done by pointing to the binary.
3. The service is **started remotely**.
4. Upon exit, the service is **stopped, and the binary is deleted**.

### **Process of Manually Executing PsExec**

Assuming there is an executable payload (created with msfvenom and obfuscated using Veil to evade antivirus detection), named 'met8888.exe', representing a meterpreter reverse_http payload, the following steps are taken:

- **Copying the binary**: The executable is copied to the ADMIN$ share from a command prompt, though it may be placed anywhere on the filesystem to remain concealed.

- **Creating a service**: Utilizing the Windows `sc` command, which allows for querying, creating, and deleting Windows services remotely, a service named "meterpreter" is created to point to the uploaded binary.

- **Starting the service**: The final step involves starting the service, which will likely result in a "time-out" error due to the binary not being a genuine service binary and failing to return the expected response code. This error is inconsequential as the primary goal is the binary's execution.

Observation of the Metasploit listener will reveal that the session has been initiated successfully.

[Learn more about the `sc` command](https://technet.microsoft.com/en-us/library/bb490995.aspx).


Find moe detailed steps in: [https://blog.ropnop.com/using-credentials-to-own-windows-boxes-part-2-psexec-and-services/](https://blog.ropnop.com/using-credentials-to-own-windows-boxes-part-2-psexec-and-services/)

**You could also use the Windows Sysinternals binary PsExec.exe:**

![](<../../.gitbook/assets/image (165).png>)

You could also use [**SharpLateral**](https://github.com/mertdas/SharpLateral):

{% code overflow="wrap" %}
```
SharpLateral.exe redexec HOSTNAME C:\\Users\\Administrator\\Desktop\\malware.exe.exe malware.exe ServiceName
```
{% endcode %}

<details>

<summary><strong>Learn AWS hacking from zero to hero with</strong> <a href="https://training.hacktricks.xyz/courses/arte"><strong>htARTE (HackTricks AWS Red Team Expert)</strong></a><strong>!</strong></summary>

Other ways to support HackTricks:

* If you want to see your **company advertised in HackTricks** or **download HackTricks in PDF** Check the [**SUBSCRIPTION PLANS**](https://github.com/sponsors/carlospolop)!
* Get the [**official PEASS & HackTricks swag**](https://peass.creator-spring.com)
* Discover [**The PEASS Family**](https://opensea.io/collection/the-peass-family), our collection of exclusive [**NFTs**](https://opensea.io/collection/the-peass-family)
* **Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f) or the [**telegram group**](https://t.me/peass) or **follow** us on **Twitter** 🐦 [**@carlospolopm**](https://twitter.com/hacktricks_live)**.**
* **Share your hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.

</details>
