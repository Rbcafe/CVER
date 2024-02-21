# CVE-2024-25466
Description for CVE-2024-25466

> [Suggested description]</br>
> Directory Traversal vulnerability in React Native Document Picker
> before v.9.1.1 and fixed in v.9.1.1 allows a local attacker to execute
> arbitrary code via a crafted script to the Android library component.
>
> ------------------------------------------
>
> [Vulnerability Type]</br>
> Directory Traversal
>
> ------------------------------------------
>
> [Vendor of Product]</br>
> https://github.com/rnmods/react-native-document-picker/
>
> ------------------------------------------
>
> [Affected Product Code Base]</br>
> react-native-document-picker android library - react-native-document-picker library for android:<9.1.1 version, fixed in 9.1.1
>
> ------------------------------------------
>
> [Affected Component]</br>
> Android library (exact file: https://github.com/rnmods/react-native-document-picker/blob/0be5a70c3b456e35c2454aaf4dc8c2d40eb2ab47/android/src/main/java/com/reactnativedocumentpicker/RNDocumentPickerModule.java)
>
> ------------------------------------------
>
> [Attack Type]</br>
> Local
>
> ------------------------------------------
>
> [Impact Code execution]</br>
> true
>
> ------------------------------------------
>
> [Impact Escalation of Privileges]</br>
> true
>
> ------------------------------------------
>
> [Attack Vectors]</br>
> To exploit this vulnerability, user must choose malicious configured application while picking a file
>
> ------------------------------------------
>
> [Has vendor confirmed or acknowledged the vulnerability?]</br>
> true
>
> ------------------------------------------
>
> [Reference]</br>
> http://react-native-document-picker.com</br>
> https://github.com/rnmods/react-native-document-picker/</br>
> https://github.com/rnmods/react-native-document-picker/blob/0be5a70c3b456e35c2454aaf4dc8c2d40eb2ab47/android/src/main/java/com/reactnativedocumentpicker/RNDocumentPickerModule.java
>
> ------------------------------------------
>
> [CVSSv3]</br>
> CVSS v3: (AV:L/AC:L/PR:N/UI:R/S:U/C:L/I:H/A:H): 7.3
