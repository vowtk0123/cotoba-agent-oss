"""
Copyright (c) 2020 COTOBA DESIGN, Inc.

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated
documentation files (the "Software"), to deal in the Software without restriction, including without limitation
the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software,
and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO
THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT,
TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""
import unittest.mock

from twilio.rest import Client

from programy.clients.restful.flask.twilio.client import TwilioBotClient
from programy.clients.restful.flask.twilio.config import TwilioConfiguration

from programytest.clients.arguments import MockArgumentParser


class MockArgs():

    def __init__(self):
        self._args = {}

    def get(self, name):
        return self._args[name]


class MockTwilioClient(Client):

    def __init__(self, account_sid, auth_token):
        pass


class MockTwilioBotClient(TwilioBotClient):

    def __init__(self, argument_parser=None, twilio_client=None):
        self.test_twilio_client = twilio_client
        self.test_question = None
        TwilioBotClient.__init__(self, argument_parser)

    def set_question(self, question):
        self.test_question = question

    def get_license_keys(self):
        self._account_sid = "TWILIO_ACCOUNT_SID"
        self._auth_token = "TWILIO_AUTH_TOKEN"
        self._from_number = "+447777777777"

    def ask_question(self, sessionid, question):
        if self.test_question is not None:
            return self.test_question
        return super(MockTwilioBotClient, self).ask_question(sessionid, question)

    def create_twilio_client(self):
        if self.test_twilio_client is not None:
            return self.test_twilio_client
        return super(MockTwilioBotClient, self).create_twilio_client()


class TwilioBotClientTests(unittest.TestCase):

    def test_twilio_client_init(self):
        arguments = MockArgumentParser()
        client = MockTwilioBotClient(arguments)
        self.assertIsNotNone(client)

        self.assertEqual("TWILIO_ACCOUNT_SID", client._account_sid)
        self.assertEqual("TWILIO_AUTH_TOKEN", client._auth_token)
        self.assertEqual("+447777777777", client._from_number)

        self.assertIsInstance(client.get_client_configuration(), TwilioConfiguration)

        self.assertIsInstance(client._twilio_client, Client)

    def test_create_response(self):
        arguments = MockArgumentParser()
        client = MockTwilioBotClient(arguments)
        self.assertIsNotNone(client)

        response = client.create_response("+447777777777", "Hi There")
        self.assertIsNotNone(response)
        self.assertEqual('<?xml version="1.0" encoding="UTF-8"?><Response><Message to="+447777777777">Hi There</Message></Response>', response)

    def test_receive_message_post(self):
        arguments = MockArgumentParser()
        client = MockTwilioBotClient(arguments, twilio_client=MockTwilioClient("SID", "TOKEN"))
        self.assertIsNotNone(client)

        client.test_question = "Hi there"

        request = unittest.mock.Mock()
        request.method = 'POST'
        request.form = {"From": "+447777777888", "Body": "Hello"}

        response = client.receive_message(request)
        self.assertIsNotNone(response)
        self.assertEqual('<?xml version="1.0" encoding="UTF-8"?><Response><Message to="+447777777888">Hi there</Message></Response>', response)

    def test_receive_message_get(self):
        arguments = MockArgumentParser()
        client = MockTwilioBotClient(arguments, twilio_client=MockTwilioClient("SID", "TOKEN"))
        self.assertIsNotNone(client)

        client.test_question = "Hi there"

        request = unittest.mock.Mock()
        request.method = 'GET'
        request.args = MockArgs()
        request.args._args["From"] = "+447777777888"
        request.args._args["Body"] = "Hello"

        response = client.receive_message(request)
        self.assertIsNotNone(response)
        self.assertEqual('<?xml version="1.0" encoding="UTF-8"?><Response><Message to="+447777777888">Hi there</Message></Response>', response)
