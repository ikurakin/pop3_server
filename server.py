__author__ = 'ikurakin'

import SocketServer
from controllers import DBQueries

class POP3Handler(SocketServer.BaseRequestHandler):
    """
    The RequestHandler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    ERR = "-ERR\r\n"
    OK = "+OK\r\n"
    def setup(self):
        self.request.sendall("Welcome to POP server, 127.0.0.1!\r\n")
        self.AUTHORIZATION = True
        self.user = None
        self.TRANSACTION = False
        self.queries = DBQueries()
        self.accepted_methods = dict((("USER", self.user_method), ("PASS", self.pass_method),
                                      ("LIST", self.list_method), ("RETR", self.retr_method),
                                      ("QUIT", self.quit_method)))

    def handle(self):
        while self.AUTHORIZATION:
            self.process_request_data()

    def process_request_data(self):
        data = self.request.recv(1024).strip()
        self.data = data.split()
        if self.data:
            POP3_method = self.data[0]
            if POP3_method in self.accepted_methods:
                self.accepted_methods[POP3_method]()
            else:
                self.request.sendall("Method is not accepted!\r\n")

    # implements QUIT POP3 method behavior
    def quit_method(self):
        self.AUTHORIZATION = False
        self.request.sendall("Bye!\r\n")

    # implements USER POP3 method behavior
    def user_method(self):
        if self.TRANSACTION:
            self.request.sendall(self.ERR)
            return
        if len(self.data) > 1:
            self.user = self.data[1]
            if self.queries.user_exists(self.user):
                self.request.sendall(self.OK)
                return
        self.request.sendall(self.ERR)

    # implements PASS POP3 method behavior
    def pass_method(self):
        if len(self.data) > 1:
            passw = self.data[1]
            if self.TRANSACTION:
                self.request.sendall(self.ERR)
                return
            if self.user:
                if self.queries.authenticate_user(self.user, passw):
                    self.TRANSACTION = True
                    self.request.sendall(self.OK)
                    return
        self.request.sendall(self.ERR)

    # implements LIST POP3 method behavior
    def list_method(self):
        if self.TRANSACTION:
            emails = self.queries.get_user_emails(self.user)
            if emails:
                string = self.OK
                string += "You've got {} letters in your mailbox\r\n".format(len(emails))
                string += "\r\n".join(emails)
                string += "\r\nFeel free to fetch any with RETR command\r\n"
                self.request.sendall(string)
                return
        self.request.sendall(self.ERR)

    # implements RETR POP3 method behavior
    def retr_method(self):
        if len(self.data) > 1:
            id = self.data[1]
            subject, body = self.queries.get_email(id)
            self.request.sendall("Subject: {subject}\r\n{body}".format(subject=subject, body=body))
            return
        self.request.sendall(self.ERR)


class ThreadingPOP3Server(SocketServer.ThreadingMixIn, SocketServer.TCPServer):
    pass

if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = ThreadingPOP3Server((HOST, PORT), POP3Handler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
