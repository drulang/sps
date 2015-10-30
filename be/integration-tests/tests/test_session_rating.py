import json
import unittest
import datetime

import requests

import base
from base import SBT


class ReadSessionBeerRatingTest(base.SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(ReadSessionBeerRatingTest, self).setUpClass()
        self.load_fixture('session-beer-rating')
        """
        Fixture Notes:
            - Session Id 200
                -has tb1, tb2, tb3 in beers
                -tb1,beersessionid 2, has 2x ratings
                    -By userid: 201
                -tb1,beersessionid 3, has a rating
                    -By userid: 202
        """

    def test_get_all_session_beer_ratings(self):
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s" % (SBT.sessionid1, 2, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.get(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")
        
        self.assertEquals(len(content['beerratings']), 3)
        beerratings = content['beerratings']
        self.assertEquals(beerratings[0]['sessionbeerid'], 2)
        self.assertEquals(beerratings[1]['sessionbeerid'], 2)
    def test_filter_session_ratings_by_userid(self):
        #Filter for user 2, should be no ratings
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s&userid=%s" % (SBT.sessionid1, 2, self.token_url_param(self.apptoken, SBT.user1_token), SBT.userid2)
        resp = requests.get(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")
        self.assertEquals(len(content['beerratings']), 1)

    def test_filter_session_ratings_by_ratingtyp(self):
        #Filter by malty
        ratingtypcd = "mlt"

        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s&ratingtypcd=%s" % (SBT.sessionid1, 2, self.token_url_param(self.apptoken, SBT.user1_token), ratingtypcd)
        resp = requests.get(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")
        self.assertEquals(len(content['beerratings']), 2)

        beerrating = content['beerratings'][0]
        self.assertEquals(beerrating['ratingtypcd'],
                          ratingtypcd)
        beerrating = content['beerratings'][1]
        self.assertEquals(beerrating['ratingtypcd'],
                          ratingtypcd)

    def test_get_session_beer_rating(self):
        #Get beer rating 1
        ratingid = 1
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid1, 2, ratingid, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.get(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        beerrating = content['beerrating']
        self.assertEquals(beerrating['ratingid'], ratingid)
class CreateSessionBeerRatingTest(base.SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(CreateSessionBeerRatingTest, self).setUpClass()
        self.load_fixture('session-beer-rating')

    def test_create_rating(self):
        #Rate sessionbeerid 3
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s" % (SBT.sessionid1, 3, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "userid": SBT.userid1,
            "ratingval": 3,
            "ratingtypcd": "hpy",
        }
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        beerrating = content['beerrating']
        self.assertEquals(beerrating['userid'], SBT.userid1)
    def test_create_rating_on_closed_session(self):
        #Try on sessionnid2
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s" % (SBT.sessionid2, 999, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "userid": SBT.userid1,
            "ratingval": 3,
            "ratingtypcd": "hpy",
        }
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                SBT.SESSION_CLOSED_ERRMSG)

    def test_create_rating_on_closed_beer(self):
        #Rate sessionbeerid 1, in session3
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s" % (SBT.sessionid3, 1, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "userid": SBT.userid1,
            "ratingval": 3,
            "ratingtypcd": "hpy",
        }
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session beer is closed")

    def test_create_invalid_rating(self):
        #Test ratingval
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s" % (SBT.sessionid1, 3, self.token_url_param(self.apptoken, SBT.user1_token))
        data = { 
            "userid": SBT.userid1,
            "ratingtypcd": "hpy",
        }
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'], "Missing required field ratingval")

        #Test ratingtypcd not passwed
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s" % (SBT.sessionid1, 3, self.token_url_param(self.apptoken, SBT.user1_token))
        data = { 
            "userid": SBT.userid1,
            "ratingval": 3,
        }
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'], "Missing required field ratingtypcd")

    def test_create_rating_userid_ne_to_usertoken(self):
        #Rate sessionbeerid 3
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s" % (SBT.sessionid1, 3, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "userid": SBT.userid2,
            "ratingval": 3,
            "ratingtypcd": "hpy",
        }
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "User/UserToken mismatch")

    def test_create_rating_on_rated_beer(self):
        #Try ratng sessionbeerid 4 twice
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s" % (SBT.sessionid1, 4, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "userid": SBT.userid1,
            "ratingval": 3,
            "ratingtypcd": "hpy",
        }
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        #Second rating
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "User has already rated this beer")

    def test_create_rating_on_nonexistant_beer(self):
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s" % (SBT.sessionid1, 999, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "userid": SBT.userid1,
            "ratingval": 3,
            "ratingtypcd": "hpy",
        }
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session Beer id does not exist")

class DeleteSessionBeerRatingTest(base.SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(DeleteSessionBeerRatingTest, self).setUpClass()
        self.load_fixture('session-beer-rating')

    def test_delete_rating(self):
        #Rate sessionbeerid 4
        url = self.rest_base_url + "/session/%s/beer/%s/rating?%s" % (SBT.sessionid1, 4, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "userid": SBT.userid1,
            "ratingval": 3,
            "ratingtypcd": "hpy",
        }
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")
        
        #Now delete
        ratingid = content['beerrating']['ratingid']

        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid1, 4, ratingid, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

    def test_delete_another_user_rating(self):
        #Try deleting user 101 ratingid 1 in session 101
        ratingid = 1
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid1, 4, ratingid, self.token_url_param(self.apptoken, SBT.user2_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
          "This user is not allowed to edit this rating")

    def test_delete_rating_on_closed_beer(self):
        #Try deleting user 101 beerratingid 3,
        #in session 202
        ratingid = 3
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid3, 1, ratingid, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
          "Session beer is closed")

    def test_delete_rating_on_closed_session(self):
        #Try deleting on session id 2
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid2, 1, 999, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                          SBT.SESSION_CLOSED_ERRMSG)

    def test_delete_nonexistant_rating(self):
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid1, 2, 999, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Beer rating does not exist")
                         
    def test_delete_on_nonexistant_session(self):
        #TODO: Need to add this to all other classes
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (999, 2, 1, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session id does not exist")


class UpdateSessionBeerRatingTest(base.SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(UpdateSessionBeerRatingTest, self).setUpClass()
        self.load_fixture('session-beer-rating')

    def test_edit_rating(self):
        #Session1, beerratingid 5, sessionbeerid 2
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid1, 2, 5, self.token_url_param(self.apptoken, SBT.user1_token))

        comment = "New Comment"
        data = {
            "ratingval": 1,
            "comment": comment,
        }
        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        beerrating = content['beerrating']
        self.assertEquals(beerrating['ratingval'], 1)
        self.assertEquals(beerrating['comment'], comment)

    def test_edit_another_user_rating(self):
        #Try editing user 102's session1 beerratingid 2
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid1, 2, 2, self.token_url_param(self.apptoken, SBT.user1_token))

        data = { "ratingval": 1, }
        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
          "This user is not allowed to edit this rating")

    def test_edit_nonexistant_rating(self):
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid1, 2, 999, self.token_url_param(self.apptoken, SBT.user1_token))

        data = { "ratingval": 1, }
        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Beer rating does not exist")
        
    def test_edit_rating_on_closed_beer(self):
        #Try editing sessiion 3, beerrating id 3
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid3, 1, 3, self.token_url_param(self.apptoken, SBT.user1_token))

        data = { "ratingval": 1, }
        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session beer is closed")

    def test_edit_rating_on_closed_session(self):
        #try session 2
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (SBT.sessionid2, 1, 3, self.token_url_param(self.apptoken, SBT.user1_token))

        data = { "ratingval": 1, }
        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                SBT.SESSION_CLOSED_ERRMSG)

    def test_edit_rating_on_nonexistant_session(self):
        url = self.rest_base_url + "/session/%s/beer/%s/rating/%s?%s" % (999, 2, 1, self.token_url_param(self.apptoken, SBT.user1_token))
        data = { "ratingval": 1, }
        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session id does not exist")

if __name__ == "__main__":
    unittest.main()
