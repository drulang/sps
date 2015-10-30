import unittest
import json

import requests

from base import SpsBaseTest, SBT


class SessionEventTest(SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(SessionEventTest, self).setUpClass()
        self.load_fixture("session-event")

    def test_events_generated(self):
        #Assert no events, change sessionstatustypcd
        #for session 100, there should be one event
        event_url = self.rest_base_url + "/session/%s/event?%s" % (100, self.token_url_param(self.apptoken, SBT.user1_token))

        content = self.content_from_get(event_url)
        self.assertEquals(content['status'], "OK")
        self.assertEquals(len(content['events']), 0)

        #Change sessionstatustypcd
        url = self.rest_base_url + "/session/%s?%s" % (100, self.token_url_param(self.apptoken, SBT.user1_token))

        data = { "sessionstatustypcd": "clsd", }

        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        #Verify 1 event
        content = self.content_from_get(event_url)
        self.assertEquals(content['status'], "OK")
        self.assertEquals(len(content['events']), 1)
        
if __name__ == "__main__":
    unittest.main()
