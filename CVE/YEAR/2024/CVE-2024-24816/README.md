# CVE-2024-24816
CKEditor 4 < 4.24.0-lts - XSS vulnerability in samples that use the "preview" feature. 

## Timeline
- Vulnerability reported to vendor: 18.07.2024
- New fixed 5.2.8 version released: 07.02.2024
- Public disclosure: 06.01.2024

## Description

Cross-Site-Scripting (XSS) vulnerability in CkEditor 4 sample files. This vulnerability allows an attacker to execute untrusted JavaScript code in the context of the currently logged-in user.

The vulnerability exists in sample files that use the "preview" feature:
```
samples/old/**/*.html
plugins/[plugin name]/samples/**/*.html
```

The following code can be used to achieve XSS using the "preview" feature:
```
<p>&gt;</p>

<p><a href="javascript:alert(document.domain)">XSS</a></p>

<p>&nbsp;</p>
```

This issue was caused by a lack of sanitization of the data passed to "preview" feature. This problem has been fixed in CKEditor 4 at version 4.24.0-lts.

## Affected versions
< 4.24.0-lts

## Advisory
Update CKEditor 4 to version 4.24.0-lts or newer.

### References
* https://ckeditor.com/cke4/release-notes
* https://github.com/ckeditor/ckeditor4/security/advisories/GHSA-mw2c-vx6j-mg76
* https://nvd.nist.gov/vuln/detail/CVE-2024-24816
