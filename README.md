# VPN Profile Emailer
## Setup/How-To
- Install PiVPN on raspberry pi or linux OS
- Create a gmail account or use one you already own and setup an app password
- Change line 80 in the file to the path where your wireguard files are
- Create an .env file in the same directory as the python file and add:
  - EMAIL_SENDER_PASSWORD=`<gmail app password>`
  - EMAIL_SENDER = `<email address of the same gmail associated with the app>`
- run script with python3 `<the email of the recipient>`
- Script will create the profile on the raspberry pi with pivpn, encode the wireguard conf file, and then send both the conf file and qr code to the recipient
