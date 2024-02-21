# CVE-2024-23200
CVE-2024-23200

The My Porsche application 9.23.50 for Android allows attackers
to obtain sensitive information because AndroidManifest.xml lacks
the hasFragileUserData attribute, and thus sensitive information about
a vehicle and its owner persists after uninstallation.

android:hasFragileUserData is an attribute in Android that allows
developers to specify whether their app contains fragile user data
that needs to be protected.

Fragile user data refers to any data that could potentially cause harm
or damage to a user if it's lost, stolen, or misused.

This can include sensitive personal information such as social
security numbers, credit card numbers, medical records, and other
sensitive data.

This value should be set explicitly in the application to indicate
whether the application is handling important user data or not.

If its value is true, then when the user uninstalls the app, a prompt
will be shown to the user asking him whether to keep the app's data.

The hasFragileUserData flag can be added to the application
AndroidManifest.xml file.



Lukasz Studniarz
