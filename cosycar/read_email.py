# -*- coding: utf-8 -*-

import logging
import imaplib
import email

ORG_EMAIL = "@gmail.com"
FROM_EMAIL = "what email address to use" + ORG_EMAIL
FROM_PWD = "store this somewhere else"
SMTP_SERVER = "imap.gmail.com"
SMTP_PORT = 993

log = logging.getLogger(__name__)


class ReadEmail():
    def fetch(self):
        mail = imaplib.IMAP4_SSL(SMTP_SERVER)
        mail.login(FROM_EMAIL, FROM_PWD)
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
