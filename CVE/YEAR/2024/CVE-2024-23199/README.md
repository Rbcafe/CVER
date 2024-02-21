# CVE-2024-23199
CVE-2024-23199


The My Porsche application 9.23.50 for Android allows remote attackers
to obtain sensitive information because of Insecure Object
Serialization in
com.tencent.mm.opensdk.modelbiz.WXOpenBusinessWebview$Req.fromBundle.

------------------------------------------


In Android, Insecure Object Serialization (IOS) poses a security risk
when developers fail to implement proper safeguards during the
serialization and deserialization of objects. This vulnerability can be
exploited by attackers to inject malicious data, potentially leading to
severe consequences such as remote code execution or unauthorized
access to sensitive information. To mitigate IOS risks, developers
should adopt secure coding practices, validate input data, use secure
serialization libraries, and employ encryption methods. Regular
security assessments and testing are crucial to identifying and
addressing any insecure object serialization vulnerabilities in Android
applications.

Method android.os.Bundle.getSerializable call trace:

at com.tencent.mm.opensdk.modelbiz.WXOpenBusinessWebview$Req.fromBundle() at android.os.Bundle.getSerializable()



Lukasz Studniarz
