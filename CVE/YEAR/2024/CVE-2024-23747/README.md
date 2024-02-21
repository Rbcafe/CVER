# CVE-2024-23747
The Moderna Sistemas ModernaNet Hospital Management System 2024 is susceptible to an Insecure Direct Object Reference (IDOR) vulnerability. 

## PoC

This vulnerability resides in the system's handling of user data access through a /Modernanet/LAUDO/LAU0000100/Laudo?id= URL. Bymanipulating this id parameter, an attacker can gain access to sensitive medical information.

http://IP/Modernanet/LAUDO/LAU0000100/Laudo?id=NUMBER

![Captura de tela 2024-01-26 061042](https://github.com/louiselalanne/CVE-2024-23747/assets/100588945/7f4cbd62-3ba9-453b-88a2-b7c2f1deb2fd)

You don't need to be logged in to see the results.

## Bonus
It was possible to access this hospital's user account because of weak credentials that can be obtained through this IDOR.

![image](https://github.com/louiselalanne/CVE-2024-23747/assets/100588945/b33d8140-8ae3-4a4f-b2db-546b5e22aea1)

## Reference
https://modernasistemas.com.br/sitems/
