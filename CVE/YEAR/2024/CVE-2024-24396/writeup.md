---
title: "Reflected Cross Site Scripting in Stimulsoft.Dashboards.JS - CVE-2024-24396"
date: 2024-02-05T09:16:50Z
draft: false
toc: false
images:
tags:
  - stimulsoft
---
<!-- These are required fields for the disclosure process -->
**Affected Product:** Stimulsoft Dashboards.JS

**Affected Versions:** <2024.1.2 

**Fixed Version:** 2024.1.3

**CVE-Number:** CVE-2024-24396

**Severity:** 4.8 (CVSS:3.1/AV:N/AC:H/PR:N/UI:N/S:U/C:L/I:L/A:N)
<!-- Add your names. -->
*Discovered by Ing. Simon Schönegger, BSc, MSc, DI Lukas Hammer, BSc*

<!-- Brief introduction. -->
During security research, the researchers discovered that Stimulsoft Dashboards.JS is prone to multiple vulnerabilities including Reflected Cross Site Scripting.

In order to exploit this vulnerability an attacker is only required to visit the Dashboards Application. This vulnerability is rated as unauthtenticated, since this product does not handle authentication on its own.
## Proof of Concept
<!-- In Depth discussion of the vulnerability. Whats it's impact, show enough proof but not too much. DO NOT INCLUDE EXPLOIT PAYLOADS! -->
It is possible to inject arbitrary JavaScript-Code into the search bar. This code is executed as soon as the search function is triggered. The following code can be used to trigger this behaviour: `<img src="#" onerror="alert(1)" />`
![Injecting JavaScript-Code into the search bar](../images/reflected_xss.png)
## Vendor contact timeline 
<!-- Fill in your contact timeline!-->
| Date       | Action                                                                                                                                                                             |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2024/01/10    | Discovery of the vulnerability |
| 2024/01/10    | Researchers inform vendor about the vulnerability |
| 2024/01/19    | Vendor informs the researchers, that the vulnerability will be fixed with 2024.1.3 |
| 2024/01/19    | Stimulsoft Dashboards.JS 2024.1.3 is released |
| 2024/01/19    | Disclosure of the vulnerability to MITRE  |
| 2024/02/02    | MITRE assigns CVE-2024-24396 |


