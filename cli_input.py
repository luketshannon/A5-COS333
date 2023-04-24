import argparse

class Input:

    def __init__(self):
        self.parser = None
        self.parsed_args = None

    def parse_cli(self, args):
        self.parser = argparse.ArgumentParser(description=
        'Client for the registrar application',
         allow_abbrev=False) #still the same??
        self.parser.add_argument('host', metavar='host', help=
        'the host on which the server is running')
        self.parser.add_argument('port', metavar='port', type = int,
        help='the port at which the server is listening')

        self.parsed_args = self.parser.parse_args(args)
        return self.parsed_args

    def parse_cli_server(self, args):
        self.parser = argparse.ArgumentParser(description=
        'Server for the registrar application',
        allow_abbrev=False)
        # self.parser.add_argument('host', metavar='host', help=
        # 'the host on which the server is running')
        self.parser.add_argument('port', metavar='port', type = int,
        help='the port at which the server is listening')

        self.parsed_args = self.parser.parse_args(args)
        return self.parsed_args
