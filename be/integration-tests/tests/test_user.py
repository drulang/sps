import unittest
import json
import datetime

import requests

from base import SpsBaseTest

class UserTest(SpsBaseTest):

    test_email = 'testuser@test.com'
    test_username = 'testuser1'
    test_password = 'testpassword1'
    test_firstname = 'testfn'
    test_lastname = 'testln'

    @classmethod
    def setUpClass(self):
        super(UserTest, self).setUpClass()
        self.load_fixture("user")

    def test_valid_get_user(self):
        url = self.rest_base_url + "/user/%s?apptoken=%s&usertoken=%s" % (self.default_userid, self.apptoken, self.default_usertoken)

        resp = requests.get(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'],"OK")

        user = content['user']
        self.assertEquals(user['email'], self.default_email)
        self.assertEquals(user['username'], self.default_username)
        self.assertEquals(user['lastname'], self.default_lastname)
        self.assertEquals(user['firstname'], self.default_firstname)

    def test_get_nonexistant_user(self):
        url = self.rest_base_url + "/user/%s?apptoken=%s&usertoken=%s" % (9999, self.apptoken, self.default_usertoken)
        resp = requests.get(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'],"ERR")
        self.assertGreater(len(content['errmsg']), 0)

    def test_create_valid_user(self):
        url = self.rest_base_url + "/user?apptoken=%s" % self.apptoken
        data = {
            "email": self.test_email,
            "username": self.test_username,
            "password": self.test_password,
            "firstname": self.test_firstname,
            "lastname": self.test_lastname
        }
        resp = requests.post(url, data=data)

        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        user = content['user']
        usertoken = content['usertoken']

        self.assertEquals(user['email'], self.test_email)
        self.assertEquals(user['username'], self.test_username)
        self.assertEquals(user['lastname'], self.test_lastname)
        self.assertEquals(user['firstname'], self.test_firstname)

        self.assertEquals(usertoken['username'], self.test_username)
        self.assertNotEquals(usertoken['token'], "null")
        self.assertNotEquals(usertoken['token'], None)
        self.assertGreater(len(usertoken['token']), 5)

        dt = datetime.datetime.strptime(usertoken['datecreated'], '%Y-%m-%d %H:%M:%S.%f')
        self.assertEquals(dt.date(), datetime.date.today())

    def test_create_user_w_invalid_fields(self):
        url = self.rest_base_url + "/user?apptoken=%s" % self.apptoken
        data = {
            "email": self.test_email,
            "username": self.test_username,
            "password": self.test_password,
            "firstname": self.test_firstname,
            "lastname": self.test_lastname
        }

        def validate_error_response(data, field):
            resp = requests.post(url, data=data)
            content = json.loads(resp.content)

            self.assertEquals(content['status'], 'ERR')
            self.assertEquals(content['field'], field)
            self.assertGreater(len(content['errmsg']), 0)

        ##
        # Email
        ##

        #Empty
        data['email'] = ""
        validate_error_response(data, "email")
        data['email'] = self.test_email

        #TODO: Implement invalid format
        #TODO: Implement existing

        ##
        # Username
        ##

        #Empty
        data['username'] = ""
        validate_error_response(data, "username")
        data['username'] = self.test_username

        #TODO: Implement invalid format
        #TODO: Test existing
        #TODO: Test with word in black listed words

        ##
        # Password
        ##

        #Empty
        data['password'] = ""
        validate_error_response(data, "password")
        data['password'] = self.test_password

        #TODO: Implement invalid format
        #TODO: Implement existing
        #TODO: Test too short
        #TODO: Test too long
        #TODO: Test No number

        ##
        # Firstname
        ##
        #TODO: Test with word in black listed words

        ##
        # Lastname
        ##
        #TODO: Test with word in black listed words

    def test_update_user_w_valid_fields(self):
        new_email = "newemail@test.com"
        new_firstname = "newfirstname"
        new_lastname = "newlname"

        update_url = self.rest_base_url + "/user/%s?apptoken=%s&usertoken=%s" %\
                    (self.default_userid, self.apptoken, self.default_usertoken)
        data = {
            "email": new_email,
            "firstname": new_firstname,
            "lastname": new_lastname,
        }

        resp = requests.put(update_url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")
        
        #Get user profile to verify changes
        profile_url = self.rest_base_url + "/user/%s?apptoken=%s&usertoken=%s" % (self.default_userid, self.apptoken, self.default_usertoken)

        resp = requests.get(profile_url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'],"OK")

        user = content['user']
        self.assertEquals(user['email'], new_email)
        self.assertEquals(user['firstname'], new_firstname)
        self.assertEquals(user['lastname'], new_lastname)

        #Change back to default values
        data = {
            "email": self.default_email,
            "firstname": self.default_firstname,
            "lastname":  self.default_lastname,
        }

        resp = requests.put(update_url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")
        
    def test_update_user_w_invalid_fields(self):
        raise NotImplementedError("NI")

    def test_delete_user(self):
        raise NotImplementedError("NI")

    def test_change_user_password(self):
        #Change user5's password
        username5 = "testuser5"
        userid5 = 5
        usertoken5 = "testtoken5"
        newpassword = "newpassword"
        
        update_url = self.rest_base_url + "/user/%s?apptoken=%s&usertoken=%s" %\
                    (userid5, self.apptoken, usertoken5)

        data = { "password": newpassword }
        resp = requests.put(update_url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        #Try logging in with new password
        url = self.rest_base_url + "/user/login?apptoken=%s" % self.apptoken

        data = {
            "username": username5,
            "password": newpassword,
        }

        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

if __name__ == "__main__":
    unittest.main()
