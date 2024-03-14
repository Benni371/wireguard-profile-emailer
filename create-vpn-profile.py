import sys
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from dotenv import load_dotenv
import subprocess

load_dotenv()
SENDER_EMAIL_PASSWORD = os.getenv("SENDER_EMAIL_PASSWORD")
SENDER_EMAIL = os.getenv("SENDER_EMAIL")

if SENDER_EMAIL_PASSWORD is None or SENDER_EMAIL is None:
    print("Email Password or Email not found in .env file.")
    sys.exit(1)

def send_email(to_email, qr_path, profile_path, profile_name):
    # Email details
    from_email = SENDER_EMAIL  # Update with your email
    subject = f'VPN Profile for {profile_name}'
    message = 'VPN Profile and QR attached for importing into wireguard'

    # Check if email argument is supplied
    if not to_email:
        print("Please provide an email address.")
        return

    # Construct the email
    msg = MIMEMultipart()
    msg['From'] = f"VPN Bot {from_email}"
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.attach(MIMEText(message, 'plain'))

    # Attach file if provided
    if qr_path:
        attachment = open(qr_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(qr_path))
        msg.attach(part)
    
    if profile_path:
        attachment = open(profile_path, "rb")
        part = MIMEBase('application', 'octet-stream')
        part.set_payload((attachment).read())
        encoders.encode_base64(part)
        part.add_header('Content-Disposition', "attachment; filename= %s" % os.path.basename(profile_path))
        msg.attach(part)

    # Connect to SMTP server and send email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(from_email, SENDER_EMAIL_PASSWORD)
        text = msg.as_string()
        server.sendmail(from_email, to_email, text)
        server.quit()
        print("Email sent successfully!")
    except Exception as e:
        print("An error occurred:", e)

def run_system_command(command):
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print("Error while executing command:", e)

if __name__ == "__main__":
    if len(sys.argv) < 1:
        print("Usage: python script.py <to_email>")
        sys.exit(1)

    to_email = sys.argv[1]

    profile_name = to_email.split("@")[0] # grab the email prefix if its john.johnson@gmail.com then the vpn profile name will be john.johnson.conf
    file_path = "path/to/config/" # usually for wireguard its /home/<user>/configs/
    
    #adds pivpn profile to /home/<user/configs/{profile_name}.conf
    run_system_command(f"pivpn -a -n {profile_name}") 

    # uses qrencode to encode the conf for wireguard so you can import the profile that way
    # main use case is to receive it on a computer then scan it with your phone
    run_system_command(f"qrencode -t png -o {file_path}/{profile_name}-qr.png -r {file_path}/{profile_name}.conf") 

    qr_path = f"{file_path}/{profile_name}-qr.png"
    profile_path = f"{file_path}/{profile_name}.conf"
    send_email(to_email, qr_path, profile_path, profile_name)
