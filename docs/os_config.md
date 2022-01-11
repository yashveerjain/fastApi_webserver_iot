# this file is for extra configuration add on to linux os, for security

## Firewall
Uncomplicated Firewall (UFW) is a program for managing a netfilter
firewall designed to be easy to use. It uses a command-line interface
consisting of a small number of simple commands and uses iptables for
configuration. UFW is available by default in all Ubuntu installations after
8.04 LTS. 
* Applications can register their profiles with UFW after installation.
UFW manages these applications by name. We can see which
applications are registered by using UFW with the following command:
> ufw app list

* To make sure that the firewall allows SSH connections after enabling
it, we will allow these connections, and then enable the firewall with the
following two commands:
- > ufw allow OpenSSH
- > ufw enable


## SSL Certificate

* In this process, we will use Let’s Encrypt, which is a certificate authority 
(CA) that provides an easy and automated way to obtain, install, and
maintain free TLS/SSL certificates. This process is simplified and
automated with the help of a software client called Certbot. Certbot
attempts to automate almost all the required steps and needs only minor
manual effort.
* [reference](https://certbot.eff.org/instructions?ws=other&os=ubuntufocal)
* commands to run:
* > apt install snapd
* > 