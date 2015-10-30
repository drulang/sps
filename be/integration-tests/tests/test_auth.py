import unittest
import json

import requests

import base


class AuthTest(base.SpsBaseTest):

    def test_valid_api_token(self):
        url = self.rest_base_url + "/ratingval?apptoken=%s" % self.apptoken
        req = requests.get(url)
        msg = json.loads(req.content)
        
        assert req.status_code == 200
        assert msg['status'] == "OK"

    def test_invalid_api_token(self):
        url = self.rest_base_url + "/ratingval?apptoken=badtoken"
        req = requests.get(url)
        msg = json.loads(req.content)

        assert req.status_code == 403
        assert msg['status'] == "ERR"
        assert 'errmsg' in msg.keys()
        assert msg['errmsg'] == "Invalid/missing app token"

    def test_no_api_token(self):
        #TODO: Change this to a list or urls,
        #then validate each url
        url = self.rest_base_url + "/ratingval"
        req = requests.get(url)
        msg = json.loads(req.content)

        assert req.status_code == 403
        assert msg['status'] == "ERR"
        assert 'errmsg' in msg.keys()
        assert 'missing app token' in msg['errmsg']

    def test_usertoken_mismatch(self):
        #Validate when one user token is used to retrieve another user's
        #profile an error is thrown
        url = self.rest_base_url + "/user?apptoken=%s" % self.apptoken
        data = {
            "email": "testemail",
            "username": "testun",
            "password": "testpassword1",
            "firstname": "fn",
            "lastname": "ln",
        }

        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        usertoken = content['usertoken']

        #Use new user's token to access the default user profile
        content = self.get_user_profile(self.apptoken, self.default_userid, usertoken['token'])

        self.assertEquals(content['status'],"ERR")
        self.assertGreater(len(content['errmsg']), 0)

    def test_valid_user_login(self):
        url = self.rest_base_url + "/user/login?apptoken=%s" % self.apptoken
        data = {
            "username": self.default_username,
            "password": self.default_password,
        }

        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'],"OK")

        usertoken = content['usertoken']
        self.assertEquals(usertoken['username'], self.default_username)
        self.assertGreater(len(usertoken['token']), 0)

    def test_invalid_user_login(self):
        url = self.rest_base_url + "/user/login?apptoken=%s" % self.apptoken
        data = {
            "username": self.default_username,
            "password": "badpassword",
        }

        resp = requests.post(url, data=data)
        content = json.loads(resp.content)

        self.assertEquals(content['status'],"ERR")
        self.assertGreater(len(content['errmsg']), 0)

    def test_user_logout(self):
        #Verify we can access user profile
        content = self.get_user_profile(self.apptoken, self.default_userid, self.default_usertoken)
        self.assertEquals(content['status'], "OK")

        #Log user out
        del_url = self.rest_base_url + "/user/token?apptoken=%s&usertoken=%s" % (self.apptoken, self.default_usertoken)
        resp = requests.delete(del_url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        #Verify we can't access user profile
        content = self.get_user_profile(self.apptoken, self.default_userid, self.default_usertoken)
        self.assertEquals(content['status'], "ERR")
        self.assertGreater(len(content['errmsg']), 0)

        #Login again to get new token
        login_url = self.rest_base_url + "/user/login?apptoken=%s" % self.apptoken
        data = {
            "username": self.default_username,
            "password": self.default_password,
        }

        resp = requests.post(login_url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'],"OK")

        self.default_usertoken = content['usertoken']['token']

if __name__ == "__main__":
    unittest.main()
