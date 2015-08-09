__author__ = 'ikurakin'

from unittest import TestCase
import socket


class POP3ServerTestCaise(TestCase):
    ERR = "-ERR\r\n"
    OK = "+OK\r\n"

    def setUp(self):
        HOST, PORT = "localhost", 9999
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((HOST, PORT))
        self.receive_data()

    def tearDown(self):
        self.quit_command()

    def receive_data(self):
        return self.sock.recv(1024)

    def user_command(self, user_name):
        self.sock.sendall("USER {}\n".format(user_name))
        return self.receive_data()

    def pass_command(self, pswd):
        self.sock.sendall("PASS {}\n".format(pswd))
        return self.receive_data()

    def list_command(self):
        self.sock.sendall("LIST\n")
        return self.receive_data()

    def recv_command(self, email_id):
        self.sock.sendall("RETR {}\n".format(email_id))
        return self.receive_data()

    def quit_command(self):
        self.sock.sendall("QUIT\n")
        return self.receive_data()

    def tranzaction_state(self, user_name, pswd):
        self.user_command(user_name)
        self.pass_command(pswd)

    def test_quit_cmd(self):
        self.assertEqual(self.quit_command(), "Bye!\r\n")

    def test_user_cmd(self):
        self.assertEqual(self.user_command("Khil"), self.OK)
        self.assertNotEqual(self.user_command("Hose"), self.OK)

    def test_pass_cmd(self):
        self.assertEqual(self.pass_command("qwerty"), self.ERR)
        self.user_command("Khil")
        self.assertEqual(self.pass_command("Trololo"), self.OK)
        self.assertEqual(self.pass_command("Trololo"), self.ERR)

    def test_list_cmd(self):
        self.tranzaction_state("Khil", "Trololo")
        expected_data = "+OK\r\nYou've got 1 letters in your mailbox\r\n1 Khil's email\r\n"\
                        "Feel free to fetch any with RETR command\r\n"
        self.assertEqual(self.list_command(), expected_data)

    def test_retr_cmd(self):
        self.tranzaction_state("Khil", "Trololo")
        expected_data = "Subject: Khil's email\r\nI'm riding the prairie on my stallion, so-and-so mustang, "\
                        "and my beloved Mary is thousand miles away knitting a stocking for me"
        self.assertEqual(self.recv_command(1), expected_data)
        self.assertNotEqual(self.recv_command(2), expected_data)

