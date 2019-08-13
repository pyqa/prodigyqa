"""Email library."""
import poplib
import smtplib
import email
from re import match
import socket       # used for unit tests
from datetime import datetime
from time import sleep


class TimeoutError(RuntimeError):
    """Raise this exception for timeout error."""

    EXIT_ON_FAILURE = True


class EmailKeywords(object):
    """Library for SMTP and POP Email keywords.

    This library provides the keywords for communicating with SMTP
    and POP servers and processing emails.
    """

    def __init__(self):
        """Variable Stack Declaration."""
        self.pop_connected = False
        self.pop_server = None
        self.pop_user = None
        self.pop_password = None
        self.smtp_connected = False
        self.pop_obj = None
        self.smtp_obj = None

    def __del__(self):
        """finalizer."""
        self.disconnect_from_pop_mail_server()
        self.disconnect_from_smtp_server()

    # POP Mail Keywords
    # ===================
    def _connect_pop(self, retry: int = 5):
        """Private method to connect to the POP server.

        Since POP sessions are locked, we must reconnect to get any message.
        updates.  This method is used by the keywords that poll the POP server.

        :param retry: integer.
        :type retry: int
        :return: True or raise exception.
        """
        # Occasionally, connections fail.
        # We retry [retry] times before raising an assertion.
        l_retry = retry
        while l_retry > 0:
            try:
                if self.pop_use_ssl:
                    self.pop_obj = poplib.POP3_SSL(self.pop_server, port=995)
                else:
                    self.pop_obj = poplib.POP3(self.pop_server, port=110)
                self.pop_obj.user(self.pop_user)
                self.pop_obj.pass_(self.pop_password)
                self.pop_connected = True
                return True
            except poplib.error_proto:  # indicates a login issue
                sleep(1)
                l_retry -= 1
            except socket.gaierror:     # this exception is for bad server name
                raise AssertionError("Failed to connect to POP server"
                                     "due to bad server name'"
                                     "{0}'".format(self.pop_server))
        raise AssertionError("Failed to connect to POP server"
                             " after {0} retries".format(retry))

    def connect_to_pop_mail_server(self, server, user, password, use_ssl: bool= True) -> bool:
        """Connect to the POP mail server.

        :param server: pop server
        :param user: user name
        :param password: password
        :param use_ssl: boolean
        :type use_ssl: bool
        :return: True on successful connection
        :rtype: bool
        """
        self.pop_server = server
        self.pop_user = user
        self.pop_password = password
        self.pop_use_ssl = use_ssl
        self._connect_pop()
        # To establish the initial connection and to save credentials for
        # future connections.  We can disconnect for now.
        self.disconnect_from_pop_mail_server()
        return True

    def reconnect_to_pop_mail_server(self):
        """Re-connect in order to determine updates."""
        # if we are already connected, disconnect
        if self.pop_connected and self.pop_obj is not None:
            self.disconnect_from_pop_mail_server()
        self._connect_pop()

    def disconnect_from_pop_mail_server(self) -> bool:
        """Disconnect from the POP mail server.
        :rtype: bool
        """
        if self.pop_obj is not None:
            self.pop_obj.quit()
            self.pop_connected = False
            self.pop_obj = None
        return True

    def get_mail_message_count(self):
        """Return the message count of POP mailbox."""
        self.reconnect_to_pop_mail_server()
        count = self.pop_obj.stat()[0]
        self.disconnect_from_pop_mail_server()
        return count

    def mail_message_count_should_be(self, count, timeout: int= 60):
        """Verify that the POP message count is as expected.

        :param count: expected mail count
        :param timeout:
        :type timeout: int
        """
        msg_count = self._wait_for_mail_message_count(count, timeout)
        if msg_count != count:
            raise AssertionError("POP message count should have "
                                 "been {0} when it was "
                                 "{1}".format(count, msg_count))

    def _wait_for_mail_message_count(self, count, timeout: int= 60):
        """Wait for a new message to appear on the POP server.

        :param count: expected mail count
        :param timeout:
        :type timeout: int
        :return: actual mail count
        """
        start = datetime.now()
        while (datetime.now() - start).seconds < timeout:
            cur_count = self.get_mail_message_count()
            if cur_count == count:
                return cur_count
            sleep(5)  # sleep 5 seconds to hammer the server with requests
        raise TimeoutError(
            "Failed to wait for message count in {0}s".format(timeout))

    def mail_message_count_should_not_be(self, count, timeout: int= 20):
        """Verify that the POP message count is not a certain value.

        :param count: expected mail count
        :param timeout:
        :type timeout: int
        """
        start = datetime.now()
        # wait for the message(s) to arrive, so a loop is necessary here
        while (datetime.now() - start).seconds < timeout:
            msg_count = self.get_mail_message_count()

        if msg_count == count:
            raise AssertionError(
                "POP message count should have been {0}".count)

    def delete_mail_message(self, index):
        """Delete a mail message from the POP server.

        NOTE: message index starts at 1.
        :param index: mail index.
        """
        self.reconnect_to_pop_mail_server()
        self.pop_obj.dele(index)
        self.disconnect_from_pop_mail_server()

    def get_mail_message_subject(self, index):
        """Retrieve the subject for the supplied message number.

        :param index: mail index
        :return: mail subject
        """
        self.reconnect_to_pop_mail_server()
        mail = self.pop_obj.retr(index)[1]
        self.disconnect_from_pop_mail_server()
        msg = email.message_from_string("\n".join(mail))
        return msg['subject']

    def get_mail_message_body(self, index):
        """Retrieve the body for the supplied message number.

        :param index:
        :return: mail body
        """
        self.reconnect_to_pop_mail_server()
        mail = self.pop_obj.retr(index)[1]
        self.disconnect_from_pop_mail_server()
        msg = email.message_from_string("\n".join(mail))
        return msg.get_payload()

    def mail_message_subject_should_match(self, index, reg_exp):
        """Email subject contains the required regular expression match.

        :param index: mail index.
        :param reg_exp: regular expression of mail subject.
        """
        self.reconnect_to_pop_mail_server()
        mail = self.pop_obj.retr(index)[1]
        self.disconnect_from_pop_mail_server()
        msg = email.message_from_string("\n".join(mail))
        if match(reg_exp, msg['subject']) is None:
            raise AssertionError("Message {0} subject did not match '{1}'."
                                 "Body:{2}".format(index,
                                                   reg_exp, msg['subject']))

    def mail_message_subject_should_not_match(self, index, reg_exp):
        """Email subject should not contain the regular expression match.

        :param index: mail index
        :param reg_exp: regular expression for mail subject.
        """
        self.reconnect_to_pop_mail_server()
        mail = self.pop_obj.retr(index)[1]
        self.disconnect_from_pop_mail_server()
        msg = email.message_from_string("\n".join(mail))
        if match(reg_exp, msg['subject']) is not None:
            raise AssertionError("Message {0} subject matched '{1}' "
                                 "but should not have. "
                                 "Subject:{2}".format(index,
                                                      reg_exp, msg['Subject']))

    def mail_message_body_should_match(self, index, reg_exp):
        """Email message body contains the required regular expression match.

        :param index: mail index
        :param reg_exp: regular expression for mail message body
        """
        self.reconnect_to_pop_mail_server()
        mail = self.pop_obj.retr(index)[1]
        self.disconnect_from_pop_mail_server()
        msg = email.message_from_string("\n".join(mail))
        body = msg.get_payload()
        if match(reg_exp, body) is None:
            raise AssertionError("Message {0} did not match '{1}'."
                                 "Body:{2}".format(index, reg_exp, body))

    def mail_message_body_should_not_match(self, index, reg_exp):
        """Email message body does not contain the regular expression match.

        :param index: mail index
        :param reg_exp: regular expression for mail message body
        """
        self.reconnect_to_pop_mail_server()
        mail = self.pop_obj.retr(index)[1]
        self.disconnect_from_pop_mail_server()
        msg = email.message_from_string("\n".join(mail))
        body = msg.get_payload()
        if match(reg_exp, body) is not None:
            raise AssertionError("Message {0} matched '{1}' "
                                 "but should not have."
                                 "Body:{2}".format(index, reg_exp, body))

    # SMTP Mail Keywords
    # ==============================
    def smtp_server_should_be_connected(self):
        """Verify that the SMTP server is connected."""
        if self.smtp_obj is None or self.smtp_connected is False:
            raise AssertionError("SMTP server should be connected but is not.")

    def smtp_server_should_not_be_connected(self):
        """Verify that the SMTP server is not connected."""
        if self.smtp_obj is not None or self.smtp_connected is True:
            raise AssertionError("SMTP server should not be connected but is.")

    def connect_to_smtp_server(self, server, port) -> bool:
        """Connect to the SMTP server.

        :param server: smtp server
        :param port: port no
        :return: boolean
        :rtype: bool
        """
        self.smtp_obj = smtplib.SMTP(server, port)
        self.smtp_connected = True
        return True

    def disconnect_from_smtp_server(self) -> bool:
        """Disconnect from the SMTP server.
        :rtype : bool
        """
        if self.smtp_obj is not None:
            self.smtp_obj.quit()
            self.smtp_connected = False
            self.smtp_obj = None
        return True

    def send_email(self, from_addr, to_addrs, subject, message) -> bool:
        """Send an email to a recipient.

        :param from_addr: from address
        :param to_addrs: to address
        :param subject: mail subject
        :param message: message to send
        :return: boolean
        :rtype : bool
        """
        msg = email.mime.Text.MIMEText(message)
        msg['To'] = ", ".join(to_addrs).strip(
            ", ") if isinstance(to_addrs, list) else to_addrs
        msg['From'] = from_addr
        msg['Subject'] = subject
        self.smtp_obj.sendmail(from_addr, to_addrs, msg.as_string())
        return True
