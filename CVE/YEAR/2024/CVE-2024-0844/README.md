# Popup-more  < 2.2.0 CVE-2024-0844
Path traversal in the popup-more WordPress plugin.

### Description
Vulnerable file location : /popup-more/classes/Ajax.php <br>
Link : https://wordpress.org/plugins/popup-more/#description <br>
Version : - < **2.2.0** <br>
Parameter: formKey <br>
Status: unpatched <br>

https://github.com/advisories/GHSA-wxfh-8hrr-vfjw

### Code snippet: 

```php
require_once YPM_POPUP_CLASSES.'form/'.esc_attr($key).'Form.php';
```

### Proof of concept:
![lfi_poc (1)](https://github.com/0x9567b/popup-more/assets/72038577/eddd0850-0fb8-4672-893f-5fed5f540193)
