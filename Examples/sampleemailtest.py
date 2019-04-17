"""Sample test suite for Email module."""
from prodigyqa.email import EmailKeywords

import socket
from time import sleep

pop_server = 'pop server'
pop_user = 'user'
pop_password = 'password'
smtp_server = 'smtp server'
sender = 'from@gmail.com'
recipient = 'to@gmail.com'


class TestClass(EmailKeywords):
    """Sample Test Suite."""

    def test_connect_to_smtp_server(self):
        """Test to connect bad server."""
        with self.assertRaises(socket.gaierror):
            self.connect_to_smtp_server('badserver')
        self.assertIsNotNone(self.connect_to_smtp_server(smtp_server))
        self.disconnect_from_smtp_server()

    def test_connect_to_pop_mail_server(self):
        """Test to connect server with wrong input."""
        with self.assertRaises(AssertionError):
            self.connect_to_pop_mail_server('badserver',
                                            'baduser', 'badpassword')
        with self.assertRaises(AssertionError):
            self.connect_to_pop_mail_server('webmail.hp.com',
                                            'baduser', 'badpassword')
        self.assertIsNotNone(self.connect_to_pop_mail_server(
            self.pop_server, self.pop_user, self.pop_password))
        self.assertTrue(self.disconnect_from_pop_mail_server())

    def test_send_mail(self):
        """Sample test to send mail."""
        num_messages = 10

        # get the count of messages
        self.assertIsNotNone(
            self.connect_to_pop_mail_server(self.pop_server,
                                            self.pop_user,
                                            self.pop_password,
                                            use_ssl=True))
        count = self.get_mail_message_count()

        # send the message
        self.assertTrue(self.connect_to_smtp_server(self.smtp_server))
        for i in range(count + 1, count + num_messages + 1):
            self.assertTrue(self.send_email(self.sender,
                                            self.recipient,
                                            "Test {0}".format(i),
                                            "This is test message "
                                            "{0}".format(i)))
            sleep(1)
        self.assertTrue(self.disconnect_from_smtp_server())
        self.__wait_for_mail_message_count(count + num_messages)

        for i in range(count + 1, count + num_messages + 1):
            self.mail_message_subject_should_match(i, "Test {0}".format(i))
            self.mail_message_subject_should_not_match(i, "Test xxx")
            self.mail_message_body_should_match(i, "This is test message "
                                                   "{0}".format(i))
            self.mail_message_body_should_not_match(i, "This is "
                                                       "test message xxx")

        for i in range(count + 1, count + num_messages + 1):
            self.delete_mail_message(1)
        self.mail_message_count_should_be(count)
        count = self.get_mail_message_count()
        self.assertTrue(self.disconnect_from_pop_mail_server())
