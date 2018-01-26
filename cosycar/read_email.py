# -*- coding: utf-8 -*-

import logging
import imaplib
import configparser
from email.parser import HeaderParser

from cosycar.constants import Constants
from cosycar.create_events import CreateEvent

log = logging.getLogger(__name__)


class ReadEmail():
    def __init__(self, config_file):
        config = configparser.ConfigParser()
        config.read(config_file)
        self._org_email = config.get('EMAIL', 'org_email')
        self._from_email = config.get('EMAIL', 'email_address')
        self._from_email += self._org_email
        self._from_pwd = config.get('EMAIL', 'password')
        self._smtp_server = config.get('EMAIL', 'smtp_server')
        self._smtp_port = config.getint('EMAIL', 'smtp_port')
        self._ok_senders = config.get('EMAIL', 'ok_senders')

    def fetch(self):
        mail = imaplib.IMAP4_SSL(self._smtp_server)
        log.debug("Email smtp: {}".format(self._smtp_server))
        log.debug("Email from: {}".format(self._from_email))
        mail.login(self._from_email, self._from_pwd)
        mail.select('inbox')

        type, data = mail.search(None, 'ALL')
        mail_ids = data[0]
        id_list = mail_ids.split()

        for email_id in id_list:
            email_subject = None
            sender = None
            data = mail.fetch(str(int(email_id)), '(BODY[HEADER])')
            header_data = data[1][0][1].decode()
            parser = HeaderParser()
            msg = parser.parsestr(header_data)
            email_subject = msg['Subject'].strip()
            sender = msg['From'].strip()
            if self._sender_is_nok(sender):
                log.warning("Non OK sender: {}".format(sender))
            elif self._subject_is_cancel(email_subject):
                log.info("Got Cancel")
                self._delete(mail, id_list)
                return
            elif self._subject_is_time(email_subject):
                self._create_will_leave_at(email_subject)
                self._delete(mail, id_list)
                return

        self._delete(mail, id_list)

    def _create_will_leave_at(self, leave_at):
        time_to_leave = "{}{}:{}{}".format(leave_at[0], leave_at[1],
                                           leave_at[2], leave_at[3])
        new_event = CreateEvent()
        log.info("New event from email, leave at: {}".format(time_to_leave))
        new_event.leave_at(time_to_leave)

    def _sender_is_nok(self, sender):
        ok_senders = self._ok_senders.split(',')
        ok_senders_cleaned = []
        for s in ok_senders:
            ok_senders_cleaned.append(s.strip())
        if sender in ok_senders_cleaned:
            return False
        else:
            return True

    def _subject_is_cancel(self, subject):
        found_cancel = False
        if subject.find('Cancel') is not -1:
            found_cancel = True
        if subject.find('cancel') is not -1:
            found_cancel = True
        delete_event = CreateEvent()
        delete_event.delete()
        return found_cancel

    def _subject_is_time(self, subject):
        if len(subject) == 4 and subject.isdigit():
            return True
        else:
            return False

    def _delete(self, mail, id_list):
        for email_id in id_list:
            mail.store(email_id, '+FLAGS', '\\Deleted')
        mail.expunge()
