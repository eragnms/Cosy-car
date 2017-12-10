# -*- coding: utf-8 -*-

import logging
import imaplib
import email
import configparser
import datetime
from email.parser import HeaderParser

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
        
        minutes_to_next_event = None
        
        for email_id in id_list:
            email_subject = None
            sender = None
            data = mail.fetch(str(int(email_id)), '(BODY[HEADER])')
            header_data = data[1][0][1].decode()
            parser = HeaderParser()
            msg = parser.parsestr(header_data)
            email_subject = msg['Subject'].strip()
            sender = msg['From']).strip()
            minutes_to_next_event = self._check_subject(email_subject)
            
        return minutes_to_next_event
        
    def fetch_old(self):
        mail = imaplib.IMAP4_SSL(self._smtp_server)
        mail.login(self._from_email, self._from_pwd)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]

        id_list = mail_ids.split()
        minutes_to_next_event = None
        
        for email_id in id_list:
            curr_sub = None
            typ, data = mail.fetch(str(int(email_id)),
                                   'BODY[HEADER.FIELDS (SUBJECT)]')
            for response_part in data:
                if isinstance(response_part, tuple):
                    for item in response_part:
                        text = item.decode()
                        ix = text.find('Subject:')
                        if ix is not -1:
                            curr_sub = text.split('Subject:')[1].split('\r')[0]
                            curr_sub = curr_sub.strip()
            found_cancel = False
            found_time = False
            if curr_sub is not None:
                if curr_sub.find('Cancel') is not -1:
                    found_cancel = True
                if curr_sub.find('found_cancel') is not -1:
                    found_cancel = True
                if len(curr_sub) == 4 and curr_sub.isdigit():
                   found_time = True
            if found_cancel:
                self._delete(mail, id_list)
            if found_time:
                now = datetime.datetime.now()
                now_date = now.strftime('%Y:%m:%d')
                date_to_leave = "{}:{}{}:{}{}".format(now_date,
                                                      curr_sub[0],
                                                      curr_sub[1],
                                                      curr_sub[2],
                                                      curr_sub[3])
                date_to_leave = datetime.datetime.strptime(date_to_leave,
                                                           '%Y:%m:%d:%H:%M')
                if (date_to_leave <= now):
                    date_to_leave = date_to_leave + datetime.timedelta(days=1)
                delta = date_to_leave - now
                minutes_to_next_event = delta.total_seconds() / 60
        return minutes_to_next_event

    def _delete(self, mail, id_list):
        for email_id in id_list:
            mail.store(email_id, '+FLAGS', '\\Deleted')
        mail.expunge()
