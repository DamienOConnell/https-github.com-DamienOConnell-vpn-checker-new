#!/usr/bin/env python3
# DAO 6/4/2018

import smtplib
from string import Template
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

MY_ADDRESS = "username@mybox.mydomain.com.au"
PASSWORD = "nopassword"


def get_contacts(filename):
    """
    Return a comma-separated email address string
    read from file argument
    """
    first = True
    emails = ""
    with open(filename, mode="r", encoding="utf-8") as contacts_file:
        for a_contact in contacts_file:
            if first:
                emails = emails + a_contact.strip()
                first = False
            else:
                emails = emails + "," + a_contact.strip()

    emails = str(emails)
    return emails


def read_template(filename):
    """
    Returns a Template object comprising the contents of the
    file specified by filename.
    """

    with open(filename, "r", encoding="utf-8") as template_file:
        template_file_content = template_file.read()
    return Template(template_file_content)


def send_mail_message(
    address_file, msg_template_file, subject_string, successes, polls
):

    emails = get_contacts(address_file)
    message_template = read_template(msg_template_file)  # read the message

    s = smtplib.SMTP(host="localhost", port=25)
    # s.starttls()
    # s.login(MY_ADDRESS, PASSWORD)

    print(emails)
    print(str(emails))

    msg = MIMEMultipart()

    # template substitution
    message = message_template.substitute(SUCCESSES=successes, POLLS=polls)

    print(message)

    msg["From"] = MY_ADDRESS
    msg["To"] = emails
    msg["Subject"] = subject_string

    msg.attach(MIMEText(message, "plain"))

    s.send_message(msg)
    del msg

    s.quit()


def main():
    #
    send_mail_message(
        "contacts.txt", "msg_success.txt", "Network link – Healthy", 20, 20
    )
    send_mail_message(
        "contacts.txt", "msg_failure.txt", "Network link – Down", 0, 20
    )


if __name__ == "__main__":
    main()
