---
title: "Stored Cross Site Scripting in Stimulsoft.Dashboards.JS - CVE-2024-24397"
date: 2024-02-05T09:17:50Z
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

**CVE-Number:** CVE-2024-24397

**Severity:** 7.6 (CVSS:3.1/AV:N/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:L)
<!-- Add your names. -->
*Discovered by Ing. Simon Schönegger, BSc, MSc, DI Lukas Hammer, BSc*

<!-- Brief introduction. -->
During security research, the researchers discovered that Stimulsoft Dashboards.JS is prone to multiple vulnerabilities including Stored Cross Site Scripting.

In order to exploit this vulnerability an attacker is only required to visit the Dashboards Application. This vulnerability is rated as unauthtenticated, since this product does not handle authentication on its own.
## Proof of Concept
<!-- In Depth discussion of the vulnerability. Whats it's impact, show enough proof but not too much. DO NOT INCLUDE EXPLOIT PAYLOADS! -->
A XSS payload can be injected in the field `ReportName`. When the report is loaded, the definition in the file does not get sanitized. Therefore, the payload remains persistent. This behaviour can be triggered by setting the `ReportName` to `<img src=\"#\" onerror=\"alert(1)\"/>`
![Injection of the XSS payload in the ReportName](../images/payload.png)
After the report is loaded into the designer, the user may click on `Properties` and expand the search bar. When such behaviour occurs the XSS payload is triggered and executed.
![Triggered XSS payload](../images/triggered.png)


## Vendor contact timeline 
<!-- Fill in your contact timeline!-->
| Date       | Action                                                                                                                                                                             |
|------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| 2024/01/10    | Discovery of the vulnerability |
| 2024/01/10    | Researchers inform vendor about the vulnerability |
| 2024/01/19    | Vendor informs the researchers, that the vulnerability will be fixed with 2024.1.3 |
| 2024/01/19    | Stimulsoft Dashboards.JS 2024.1.3 is released |
| 2024/01/19    | Disclosure of the vulnerability to MITRE  |
| 2024/02/02    | MITRE assigns CVE-2024-24397 |
