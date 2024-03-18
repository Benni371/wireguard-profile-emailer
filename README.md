# VPN Profile Emailer
## Setup/How-To
- Install PiVPN on raspberry pi or linux OS; Choose the Wireguard option when prompted
- Create a Gmail account or use one you already own and set up an app password
- Change line 80 in the file to the path where your Wireguard files are on your raspberry pi or linux OS
- Create an .env file in the same directory as the python file and add:
  - EMAIL_SENDER = `<email address of the Gmail associated with the app password>`
  - EMAIL_SENDER_PASSWORD=`<gmail app password>`
- run script on the raspberry pi with `python3 create-vpn-profile.py <the email of the recipient>`
- Script will create the profile on the raspberry pi with PiVPN, encode the Wireguard conf file into a QR code, and then send both the conf file and QR code to the recipient
