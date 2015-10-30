import json
import unittest
import datetime

import requests

from base import SBT, SpsBaseTest


class SessionTest(SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(SessionTest, self).setUpClass()

        self.session_name = "Session1"
        self.session_location = "KitTable"
        self.session_theme = "RenFest"
        
        self.sessionid1 = 100
        self.sessionid2 = 101 #Sessison closed
        self.userid1 = 101    #Leader of session id 100
        self.user1_token = 'testtoken1'

        self.load_fixture("session")

    def test_session_get(self):
        url = self.rest_base_url + "/session/100?apptoken=%s&usertoken=%s" % (self.apptoken, self.default_usertoken)
        resp = requests.get(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        session = content['session']
        self.assertEquals(100, session['sessionid'])

    def test_create_and_read_session(self):
        url = self.rest_base_url + "/session?apptoken=%s&usertoken=%s" % (self.apptoken, self.default_usertoken)
        data = {
            "name": self.session_name,
            "location": self.session_location,
            "theme": self.session_theme,
        }
        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        session = content['session']

        self.assertEquals(session['name'], self.session_name)
        self.assertEquals(session['theme'], self.session_theme)
        self.assertEquals(session['location'], self.session_location)
        self.assertEquals(session['dateopen'], None)
        self.assertEquals(session['dateclosed'], None)
        dt = datetime.datetime.strptime(session['datecreated'], '%Y-%m-%d %H:%M:%S')
        self.assertEquals(dt.date(), datetime.date.today())

        url = self.rest_base_url + "/session?apptoken=%s&usertoken=%s" % (self.apptoken, self.default_usertoken)
        resp = requests.get(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        #Verify session name in sessions
        found_session = False
        for session in content['sessions']:
            if session['name'] == self.session_name:
                found_session = True
                break
        self.assertTrue(found_session)

    def test_get_session_w_nonloeader(self):
        #Validate sessionjoincd isnt show to
        #a non leader user
        raise NotImplementedError("NI")

    def test_edit_session(self):
        sessionid = self.sessionid1
        url = self.rest_base_url + "/session/%s?%s" % (sessionid, self.token_url_param(self.apptoken, self.user1_token))

        session_name = "NewSessionName"
        data = {
            "name": session_name,
        }
        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        session_profile = self.get_session(self.apptoken, self.default_usertoken, sessionid)
        self.assertEquals(session_profile['status'], "OK")
        session = session_profile['session']
        self.assertEquals(session['name'], session_name)
    def test_edit_session_join_code(self):
        raise NotImplementedError("NI")

    def test_nonleader_edit_session(self):
        #Default user is not in the session 1 created
        #by session.sql fixture
        url = self.rest_base_url + "/session/%s?%s" % (self.sessionid1, self.token_url_param(self.apptoken, self.default_usertoken))

        data = { "name": "New Session Name", }
        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "User is not a leader of this session")

    def test_edit_session_sessionstatustypcd_not_changed(self):
        #Try to change session status typ to
        #what the session is already set to
        url = self.rest_base_url + "/session/%s?%s" % (self.sessionid1, self.token_url_param(self.apptoken, self.user1_token))

        data = { "sessionstatustypcd": "new" }
        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session status is already set to new")
    def test_edit_closed_session(self):
        #Try editing session2, id 102
        url = self.rest_base_url + "/session/%s?%s" % (self.sessionid2, self.token_url_param(self.apptoken, self.user1_token))

        data = { "name": "NewName" }
        resp = requests.put(url, data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session is closed.")
        
class SessionUserTest(SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(SessionUserTest, self).setUpClass()
        self.load_fixture('session-user')

        self.sessionid1 = 200
        self.sessionjoincd = 'abcd'
        self.userid1 = 101 #leader of sessionid 200
        self.userid2 = 102
        self.userid3 = 103
        self.userid4 = 104 #prtcp of sessionid 200 
        self.userid5 = 105 #prtcp of sessionid 200 
        self.userid6 = 106 #leader of sessionid 201
        self.user1_token = 'testtoken1'
        self.user2_token = 'testtoken2'
        self.user3_token = 'testtoken3'
        self.user4_token = 'testtoken4'
        self.user5_token = 'testtoken5'
        self.user6_token = 'testtoken6'

    def test_get_user(self):
        url = self.rest_base_url + "/session/%s/user?%s" % (self.sessionid1, self.token_url_param(self.apptoken, self.default_usertoken))
        content = self.content_from_get(url)
        self.assertEquals(content['status'], "OK")

        users = content['users']
        self.assertEquals(len(users), 3) #Users: 101, 104, 105
        user = users[0]
        self.assertEquals(user['userid'], self.userid1)
        self.assertEquals(user['userroletypcd'], 'ldr')
    
    def test_valid_join_session(self):
        #Add user2 to the session
        url = self.rest_base_url + "/session/%s/user?%s" % (self.sessionid1, self.token_url_param(self.apptoken, self.user2_token))

        data = {
            "userid": self.userid2,
            "userroletypcd": "prtcp",
            "userjoincd": self.sessionjoincd,
        }
        resp = requests.post(url, data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        url = self.rest_base_url + "/session/%s/user?%s" % (self.sessionid1, self.token_url_param(self.apptoken, self.default_usertoken))
        content = self.content_from_get(url)
        self.assertEquals(content['status'], "OK")

        users = content['users']
        found_user = False
        for user in users:
            if user['userid'] == self.userid2:
                found_user = True
                break

        self.assertTrue(found_user)
        
    def test_invalid_join_session(self):

        #Try adding user is already in session
        url = self.rest_base_url + "/session/%s/user?%s" % (self.sessionid1, self.token_url_param(self.apptoken, self.user1_token))

        data = {
            "userid": self.userid1,
            "userroletypcd": "prtcp",
            "userjoincd": self.sessionjoincd,
        }
        resp = requests.post(url, data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals("User is already in the session",
                          content['errmsg'])

        #Invalid join code
        url = self.rest_base_url + "/session/%s/user?%s" % (self.sessionid1, self.token_url_param(self.apptoken, self.user3_token))

        data = {
            "userid": self.userid3,
            "userroletypcd": "prtcp",
            "userjoincd": "BadValue",
        }
        resp = requests.post(url, data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals("Invalid session join code",
                          content['errmsg'])

        #UserId/Uesrtoken mismatch
        url = self.rest_base_url + "/session/%s/user?%s" % (self.sessionid1, self.token_url_param(self.apptoken, self.user3_token))

        data = {
            "userid": self.userid1,
            "userroletypcd": "prtcp",
            "userjoincd": self.sessionjoincd,
        }
        resp = requests.post(url, data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals("User/UserToken mismatch",
                          content['errmsg'])

    def test_valid_remove_user(self):
        #User removes themself
        #Add user 3
        url = self.rest_base_url + "/session/%s/user?%s" % (self.sessionid1, self.token_url_param(self.apptoken, self.user3_token))

        data = {
            "userid": self.userid3,
            "userroletypcd": "prtcp",
            "userjoincd": self.sessionjoincd,
        }
        resp = requests.post(url, data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        #Then remove user 3
        url = self.rest_base_url + "/session/%s/user/%s?%s" % (self.sessionid1, self.userid3, self.token_url_param(self.apptoken, self.user3_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")


        #Leader of group removes user
        #Add user 3
        url = self.rest_base_url + "/session/%s/user?%s" % (self.sessionid1, self.token_url_param(self.apptoken, self.user3_token))

        data = {
            "userid": self.userid3,
            "userroletypcd": "prtcp",
            "userjoincd": self.sessionjoincd,
        }
        resp = requests.post(url, data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")
        
        #Have user 101 remove
        url = self.rest_base_url + "/session/%s/user/%s?%s" % (self.sessionid1, self.userid3, self.token_url_param(self.apptoken, self.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

    def test_invalid_remove_user(self):
        #User that isn't part of the session
        # - User 103 is not in session
        url = self.rest_base_url + "/session/%s/user/%s?%s" % (self.sessionid1, self.userid3, self.token_url_param(self.apptoken, self.user3_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'], "User is not in this session")

        #A regular user tryig to remove another user
        #Have user 4 try removing user 5
        url = self.rest_base_url + "/session/%s/user/%s?%s" % (self.sessionid1, self.userid5, self.token_url_param(self.apptoken, self.user4_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "User is not allowed to remove user.")
         
        #A leader from another session trying to
        #remove a user in a session
        #  Leader of sessoinid 201 remove user 5
        url = self.rest_base_url + "/session/%s/user/%s?%s" % (self.sessionid1, self.userid5, self.token_url_param(self.apptoken, self.user6_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "User is not in this session")

    def test_leader_leaves(self):
        #Try to remove user 101 from session 1         
        url = self.rest_base_url + "/session/%s/user/%s?%s" % (self.sessionid1, self.userid1, self.token_url_param(self.apptoken, self.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
            "Leader cannot remove themself. They must reassign leadership")

    def test_leader_reassigns_leader(self):
        #User 106 in session 202, assigns user 105
        #as leader
        user5id = 105
        user5token = 'testtoken5'
        user6id = 106
        user6token = 'testtoken6'
        url = self.rest_base_url + "/session/%s/user/%s?%s" % (202, user5id, self.token_url_param(self.apptoken, user6token))
        data = {
            "userroletypcd": "ldr",
        }
        resp = requests.put(url, data=data)
        content = resp.json()
        self.assertEquals(content['status'], "OK")

    def test_nonleaader_reassigns_leader(self):
        #Have user 104 try to reassign leader to 
        #user 105 in session 200
        url = self.rest_base_url + "/session/%s/user/%s?%s" % (200, 105, self.token_url_param(self.apptoken, "testtoken4"))
        data = { "userroletypcd": "ldr", }
        resp = requests.put(url, data=data)
        content = resp.json()
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "User is not leader of session")

    def test_leader_from_diff_session_reassigns_leader(self):
        #User 106 in session 201, trys to reassign
        #user 104 in session 200
        url = self.rest_base_url + "/session/%s/user/%s?%s" % (200, 104, self.token_url_param(self.apptoken, "testtoken6"))
        data = { "userroletypcd": "ldr", }
        resp = requests.put(url, data=data)
        content = resp.json()
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "User is not in this session")
        
class ReadSessionBeerTest(SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(ReadSessionBeerTest, self).setUpClass()
        self.load_fixture('session-beer-read')

        """
        Fixture Notes:
            tb1 and tb2 beers are in session 200
        """

    def test_get_session_beer(self):
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid1, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.get(url)
        content = json.loads(resp.content)

        self.assertEquals(content['status'], "OK")
        beers = content['beers']
        self.assertEquals(len(beers), 2)
        
        for beer in beers:
            self.assertEquals(beer['sessionid'],
                              SBT.sessionid1)

            self.assertIn(beer['beerid'], SBT.beers)

class CreateSessionBeerTest(SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(CreateSessionBeerTest, self).setUpClass()
        self.load_fixture('session-beer')
        """
        Fixture Notes:
            Session ID: 201 is closed
        """

    def test_valid_add_beer(self):
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid1, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "beerid": SBT.tb1,
        }
        resp = requests.post(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

    def test_add_nonexistant_beer(self):
        
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid1, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "beerid": "badbeerid",
        }
        resp = requests.post(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
            "Beer ID doesn't exist")

    def test_add_multiple_beers(self):
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid1, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "beerid": "%s,%s" % (SBT.tb1, SBT.tb2),
        }
        resp = requests.post(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

    def test_invalid_add_multiple_beers(self):
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid1, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "beerid": "%s'%s" % (SBT.tb1, SBT.tb2),
        }
        resp = requests.post(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")

    def test_add_beer_already_in_session(self):
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid1, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "beerid": SBT.tb1,
        }
        resp = requests.post(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        #Add it a second time
        resp = requests.post(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

    def test_add_beer_on_closed_session(self):
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid2, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "beerid": "%s,%s" % (SBT.tb1, SBT.tb2),
        }
        resp = requests.post(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session is closed.")

    def test_nonleader_add_beer(self):
        #User 2, prtcp, add beer to session id 200
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid1, self.token_url_param(self.apptoken, SBT.user2_token))
        data = {
            "beerid": "%s,%s" % (SBT.tb1, SBT.tb2),
        }
        resp = requests.post(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "User is not a leader of this session")

class DeleteSessionBeerTest(SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(DeleteSessionBeerTest, self).setUpClass()
        self.load_fixture('session-beer')
        """
        Fixture Notes:
            Beer ID: tb6 is closed
        """

    def test_valid_remove_beer(self):
        #Add a beer
        sessionbeers = self._add_beer(SBT.sessionid1,
                                      SBT.tb1,
                                      SBT.user1_token)
        self.assertEquals(len(sessionbeers), 1)
        sessionbeerid = sessionbeers[0]['sessionbeerid']

        #then remove beer
        url = self.rest_base_url + "/session/%s/beer/%s?%s" % (SBT.sessionid1, sessionbeerid, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

    def test_remove_beer_not_in_session(self):
        url = self.rest_base_url + "/session/%s/beer/%s?%s" % (SBT.sessionid1, 999, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session Beer id does not exist")

    def test_nonleader_remove_beer(self):
        #Add beer
        sessionbeers = self._add_beer(SBT.sessionid1,
                                      SBT.tb1,
                                      SBT.user1_token)
        self.assertEquals(len(sessionbeers), 1)
        sessionbeerid = sessionbeers[0]['sessionbeerid']

        #Have user 2 try to remove
        url = self.rest_base_url + "/session/%s/beer/%s?%s" % (SBT.sessionid1, sessionbeerid, self.token_url_param(self.apptoken, SBT.user2_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "User is not a leader of this session")

    def test_remove_beer_on_closed_session(self):
        url = self.rest_base_url + "/session/%s/beer/%s?%s" % (SBT.sessionid2, 999, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session is closed.")

    def test_remove_closed_beer(self):
        #Test expects a sesison where sessionbeerid 1
        #is closed
        url = self.rest_base_url + "/session/%s/beer/%s?%s" % (SBT.sessionid3, 1, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.delete(url)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session beer is closed")

class UpdateSessionBeerTest(SpsBaseTest):

    @classmethod
    def setUpClass(self):
        super(UpdateSessionBeerTest, self).setUpClass()
        self.load_fixture('session-beer')

    def _get_beers(self):
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid1, self.token_url_param(self.apptoken, SBT.user1_token))
        resp = requests.get(url)
        content = json.loads(resp.content)

        self.assertEquals(content['status'], "OK")
        return content['beers']

    def test_change_beer_sequence(self):
        #Add three beers with 1,2,3
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid1, self.token_url_param(self.apptoken, SBT.user1_token))
        data = {
            "beerid": "%s,%s,%s" % (SBT.tb1, SBT.tb2, SBT.tb3),
        }
        resp = requests.post(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")
        
        #Get Beers
        beers = self._get_beers()

        self.assertEquals(beers[0]['beerid'], SBT.tb1) 
        self.assertEquals(beers[0]['seqno'], 1) 
        self.assertEquals(beers[1]['beerid'], SBT.tb2) 
        self.assertEquals(beers[1]['seqno'], 2) 
        self.assertEquals(beers[2]['beerid'], SBT.tb3) 
        self.assertEquals(beers[2]['seqno'], 3) 

        #Reverse them
        url = self.rest_base_url + "/session/%s/beer?%s" % (SBT.sessionid1, self.token_url_param(self.apptoken, SBT.user1_token))

        beer1 = beers[0]['sessionbeerid']
        beer2 = beers[1]['sessionbeerid']
        beer3 = beers[2]['sessionbeerid']
        data = {
            "sequence": "%s,%s,%s" % (beer3, beer2, beer1)
        }
        resp = requests.put(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

        beers = self._get_beers()

        #Check order is reversed
        self.assertEquals(beers[0]['beerid'], SBT.tb1) 
        self.assertEquals(beers[0]['seqno'], 3) 
        self.assertEquals(beers[1]['beerid'], SBT.tb2) 
        self.assertEquals(beers[1]['seqno'], 2) 
        self.assertEquals(beers[2]['beerid'], SBT.tb3) 
        self.assertEquals(beers[2]['seqno'], 1) 

    def test_edit_beer(self):
        #Add beer, then change it
        sessionbeers = self._add_beer(SBT.sessionid1,
                                      SBT.tb1,
                                      SBT.user1_token)
        sessionbeer = None
        for beer in sessionbeers:
            if beer['beerid'] == SBT.tb1:
                sessionbeer = beer
                break
        assert sessionbeer is not None, "Didn't find sessionbeer"
        self.assertEquals(sessionbeer['beersessionstatustypcd'], "new")
        
        #Change beer status
        url = self.rest_base_url + "/session/%s/beer/%s?%s" % (SBT.sessionid1, sessionbeer['sessionbeerid'], self.token_url_param(self.apptoken, SBT.user1_token))
        #Change status to active, and change seqno
        data = {
            "beersessionstatustypcd": "actv",
            "seqno": sessionbeer['seqno'] + 1,
        }
        resp = requests.put(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")

    def test_edit_beer_on_closed_session(self):
        #Try editing sessionid 201
        #Even though there aren't any beers in session2,
        #The logic should still prevent you from trying
        #to edit
        url = self.rest_base_url + "/session/%s/beer/%s?%s" % (SBT.sessionid2, 999, self.token_url_param(self.apptoken, SBT.user1_token))
        #Change status to active, and change seqno
        data = { "beersessionstatustypcd": "actv" }
        resp = requests.put(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session is closed.")

    def test_edit_sessionjoincd(self):
        raise NotImplementedError("NI")

    def test_edit_closed_beer(self):
        """
        Try editing sessionbeerid 1 in session 3,
        this beer is closed
        """
        url = self.rest_base_url + "/session/%s/beer/%s?%s" % (SBT.sessionid3, 1, self.token_url_param(self.apptoken, SBT.user1_token))
        #Change status to active, and change seqno
        data = { "beersessionstatustypcd": "actv" }
        resp = requests.put(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session beer is closed")

    def test_edit_beer_not_in_session(self):
        url = self.rest_base_url + "/session/%s/beer/%s?%s" % (SBT.sessionid1, 999, self.token_url_param(self.apptoken, SBT.user1_token))
        #Change status to active, and change seqno
        data = { "beersessionstatustypcd": "actv" }
        resp = requests.put(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "ERR")
        self.assertEquals(content['errmsg'],
                "Session Beer id does not exist")

if __name__ == "__main__":
    unittest.main()
