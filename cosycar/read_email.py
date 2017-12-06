# -*- coding: utf-8 -*-

import logging
import imaplib
import email
import configparser

from cosycar.constants import Constants

log = logging.getLogger(__name__)


class ReadEmail():
    def __init__(self):
        config = configparser.ConfigParser()
        config.read(Constants.cfg_file)
        self._org_email = config.get('EMAIL', 'org_email')
        self._from_email = config.get('EMAIL', 'email_address')
        self._from_email += self._org_email
        self._from_pwd = config.get('EMAIL', 'password')
        self._smtp_server = config.get('EMAIL', 'smtp_server')
        self._smtp_port = config.getint('EMAIL', 'smtp_port')
    
    def fetch(self):
        mail = imaplib.IMAP4_SSL(self._smtp_server)
        mail.login(self._from_email, self._from_pwd)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        print(id_list)
        # first_email_id = int(id_list[0])
        latest_email_id = int(id_list[-1])
        print(latest_email_id)

        subject = None
        typ, data = mail.fetch(str(latest_email_id), 'BODY[HEADER.FIELDS (SUBJECT)]')
        for response_part in data:
            if isinstance(response_part, tuple):
                for item in response_part:
                    print("*********************")
                    print("A tuple {}".format(item))
                    print("*********************")
                    print("")
                    print("")
                #print(response_part)
                msg = email.message_from_string(str(response_part[1]))
                #print('Message %s\n%s\n' % (1, data[0][1]))
                #print("*********************")
                #print(msg)
                #print("*********************")
                subject = msg['Subject']
                print("subject: {}".format(subject))
                # email_from = msg['from']
        return subject

    def delete(self):
        # delete all emails in the inbox
        pass
