

<details>

<summary><strong>Learn AWS hacking from zero to hero with</strong> <a href="https://training.hacktricks.xyz/courses/arte"><strong>htARTE (HackTricks AWS Red Team Expert)</strong></a><strong>!</strong></summary>

Other ways to support HackTricks:

* If you want to see your **company advertised in HackTricks** or **download HackTricks in PDF** Check the [**SUBSCRIPTION PLANS**](https://github.com/sponsors/carlospolop)!
* Get the [**official PEASS & HackTricks swag**](https://peass.creator-spring.com)
* Discover [**The PEASS Family**](https://opensea.io/collection/the-peass-family), our collection of exclusive [**NFTs**](https://opensea.io/collection/the-peass-family)
* **Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f) or the [**telegram group**](https://t.me/peass) or **follow** us on **Twitter** 🐦 [**@carlospolopm**](https://twitter.com/hacktricks_live)**.**
* **Share your hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.

</details>

## Firmware Integrity

The **custom firmware and/or compiled binaries can be uploaded to exploit integrity or signature verification flaws**. The following steps can be followed for backdoor bind shell compilation:

1. The firmware can be extracted using firmware-mod-kit (FMK).
2. The target firmware architecture and endianness should be identified.
3. A cross compiler can be built using Buildroot or other suitable methods for the environment.
4. The backdoor can be built using the cross compiler.
5. The backdoor can be copied to the extracted firmware /usr/bin directory.
6. The appropriate QEMU binary can be copied to the extracted firmware rootfs.
7. The backdoor can be emulated using chroot and QEMU.
8. The backdoor can be accessed via netcat.
9. The QEMU binary should be removed from the extracted firmware rootfs.
10. The modified firmware can be repackaged using FMK.
11. The backdoored firmware can be tested by emulating it with firmware analysis toolkit (FAT) and connecting to the target backdoor IP and port using netcat.

If a root shell has already been obtained through dynamic analysis, bootloader manipulation, or hardware security testing, precompiled malicious binaries such as implants or reverse shells can be executed. Automated payload/implant tools like the Metasploit framework and 'msfvenom' can be leveraged using the following steps:

1. The target firmware architecture and endianness should be identified.
2. Msfvenom can be used to specify the target payload, attacker host IP, listening port number, filetype, architecture, platform, and the output file.
3. The payload can be transferred to the compromised device and ensured that it has execution permissions.
4. Metasploit can be prepared to handle incoming requests by starting msfconsole and configuring the settings according to the payload.
5. The meterpreter reverse shell can be executed on the compromised device.
6. Meterpreter sessions can be monitored as they open.
7. Post-exploitation activities can be performed.

If possible, vulnerabilities within startup scripts can be exploited to gain persistent access to a device across reboots. These vulnerabilities arise when startup scripts reference, [symbolically link](https://www.chromium.org/chromium-os/chromiumos-design-docs/hardening-against-malicious-stateful-data), or depend on code located in untrusted mounted locations such as SD cards and flash volumes used for storing data outside of root filesystems.

## References
* For further information check [https://scriptingxss.gitbook.io/firmware-security-testing-methodology/](https://scriptingxss.gitbook.io/firmware-security-testing-methodology/)

<details>

<summary><strong>Learn AWS hacking from zero to hero with</strong> <a href="https://training.hacktricks.xyz/courses/arte"><strong>htARTE (HackTricks AWS Red Team Expert)</strong></a><strong>!</strong></summary>

Other ways to support HackTricks:

* If you want to see your **company advertised in HackTricks** or **download HackTricks in PDF** Check the [**SUBSCRIPTION PLANS**](https://github.com/sponsors/carlospolop)!
* Get the [**official PEASS & HackTricks swag**](https://peass.creator-spring.com)
* Discover [**The PEASS Family**](https://opensea.io/collection/the-peass-family), our collection of exclusive [**NFTs**](https://opensea.io/collection/the-peass-family)
* **Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f) or the [**telegram group**](https://t.me/peass) or **follow** us on **Twitter** 🐦 [**@carlospolopm**](https://twitter.com/hacktricks_live)**.**
* **Share your hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.

</details>


