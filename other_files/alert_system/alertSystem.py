import smtplib

from string import Template

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = 'uzmar.gomez@softtek.com'
PASSWORD = 'Poirot25092015@'

# MY_ADDRESS = 'ds.academy.crypto@outlook.com'
# PASSWORD = 'Btc_Eth_'

user_info = "contacts.txt"
email_message = "template_email.txt"

host_address = "smtp.office365.com"
port = 587

def get_contacts(filename):
    names = []
    emails = []
    with open(filename, mode='r', encoding='utf-8') as contacts_file:
        for a_contact in contacts_file:
            names.append(a_contact.split()[0])
            emails.append(a_contact.split()[1])
    return names, emails

def read_template(filename):
    with open(filename, 'r', encoding='utf-8') as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)

def main():
    names, emails = get_contacts(user_info) # read contacts
    message_template = read_template(email_message)

    # set up the SMTP server
    server = smtplib.SMTP(host=host_address, port=port)
    server.starttls()
    server.login(MY_ADDRESS, PASSWORD)

    # For each contact, send the email:
    for name, email in zip(names, emails):
        msg = MIMEMultipart()       # create a message

        # add in the actual person name to the message template
        message = message_template.substitute(person_name=name.title())

        # Prints out the message body for our sake
        print(message)

        # setup the parameters of the message
        msg['From']=MY_ADDRESS
        msg['To']=email
        if name == "Miguel":
            msg['Subject']="Urgent"
            msg['X-Priority']='1'
        elif name == "Luis":
            msg['Subject']="Not that urgent"
            msg['X-Priority']='3'
        elif name == "Esteban":
            msg['Subject']="Not urgent at all"
            msg['X-Priority']='5'

        # add in the message body
        msg.attach(MIMEText(message, 'plain'))

        # send the message via the server set up earlier.
        server.send_message(msg)
        del msg

    # Terminate the SMTP session and close the connection
    server.quit()

if __name__ == '__main__':
    main()
