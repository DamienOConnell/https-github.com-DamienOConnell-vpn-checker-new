#!/usr/bin/env python3

# DAO 6/4/2018

from datetime import datetime
from netmiko import ConnectHandler
from devices import router1
import sys
import os

import email_notify

contacts_file = "contacts.txt"
success_template = "msg_success.txt"
failure_template = "msg_failure.txt"

# avoid absolute path to files - contacts, templates, esp. when using cron
os.chdir(os.path.dirname(sys.argv[0]))

start_time = datetime.now()
device_list = [router1]
number_of_polls = str(20)
successes = 0
poll_commands = [
    "ping 192.168.1.1 source loopback 0 repeat " + str(number_of_polls),
    "ping 192.168.1.1 source loopback 0 repeat " + str(number_of_polls),
]

for device in device_list:
    output = False
    try:
        net_connect = ConnectHandler(**device)
        print(net_connect.enable())
        print(net_connect.send_command("terminal length 0"))
        for command in poll_commands:
            output = net_connect.send_command(command)
        for char in output:
            if char == "!":
                successes += 1
    except Exception:
        print("error in establishing connection")
        sys.exit(0)

if successes == 0:
    print("Could not poll over VPN command was ", command)
    email_notify.send_mail_message(
        contacts_file,
        failure_template,
        "Poller detects - link Down",
        successes,
        number_of_polls,
    )
else:
    print(
        "Success ",
        successes,
        " successful polls from ",
        number_of_polls,
        " poll attempts",
    )
    email_notify.send_mail_message(
        contacts_file,
        success_template,
        "Poller detects - link Healthy",
        successes,
        number_of_polls,
    )

print("Time elapsed: {}\n".format(datetime.now() - start_time))
