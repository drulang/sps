import unittest
import os
from subprocess import call, Popen
import json
import time

import requests
import redis

import conf

MYSQL_DB_FILE="sps-test-db.sql"
SPSHOME=os.environ['SPSHOME']
SPSHOME = SPSHOME if SPSHOME[-1] == "/" else SPSHOME + "/"
TESTAPPHOME = SPSHOME + "integration-tests/tmp/"

class SpsBaseTest(unittest.TestCase):

    @staticmethod
    def main():
        unittest.main()

    @classmethod
    def setUpClass(self):
        self.test_conf = conf.SpsConf()
        self.server = self.test_conf.rest_server
        self.port = self.test_conf.rest_port
        self.rest_base_url = "http://%s:%s" % (self.server, self.port)
        self.apptoken = "testtoken"

        #0. Cleanup incase of previous failure
        print "Cleaning up any leftovers"
        try:
            pass
            #self._drop_test_db()
        except:
            pass
        self._delete_testapp()
        print "  Complete."

        #1. Initialize DB
        #TODO: Fix this so call is used properly with a list of args
        self.mysql_cmd = "mysql -u %s -p%s -h %s -P %s" %\
                    (self.test_conf.db_user,
                     self.test_conf.db_password,
                     self.test_conf.db_host,
                     self.test_conf.db_port)

        db_file = SPSHOME + "integration-tests/" +  MYSQL_DB_FILE
        load_mysql_cmd = self.mysql_cmd + " < %s" % db_file
        print "Creating database"
        rc = call([load_mysql_cmd],shell=True)
        if rc != 0:
            raise Exception("Unable to create database")
        else:
            print "  Complete."

        #2. Load fixture
        print "Loading base fixture"
        self.load_fixture("base")
        print "  Complete."

        #3. Setup and run rest server
        print "Setting up application"
        cpy_cmd = SPSHOME + "integration-tests/" + "copy-app.sh"
        rc = call([cpy_cmd],shell=True)
        if rc != 0:
            raise Exception("Unable to copy app")
        else:
            print "  Complete."

        app_cmd = SPSHOME + "venv/bin/python "
        app_cmd += TESTAPPHOME + "sps-be.py"
        self.spsbe_proc = Popen(app_cmd,
                                shell=True,
                                env=dict(os.environ, PYTHONPATH=TESTAPPHOME+"lib"))
        #Wait for server to come up
        start_time = time.time()
        while True:
            if (time.time() - start_time) > 5:
                raise Exception("Unable to verify if app server is up")

            try:
                resp = requests.get(self.rest_base_url + "/system")
                respj = json.loads(resp.content)
                assert respj['apistatus'] == "UP"
                break
            except:
                pass

        #4. Create default user
        self.default_userid = 1
        self.default_username = "defaultuser"
        self.default_password = "temp"
        self.default_email = "defaultuser@test.com"
        self.default_firstname = "defaultfn"
        self.default_lastname = "defaultln"

        url = self.rest_base_url + "/user?apptoken=%s" % self.apptoken
        data = {
            "email": self.default_email,
            "username": self.default_username,
            "password": self.default_password,
            "firstname": self.default_firstname,
            "lastname": self.default_lastname,
        }

        resp = requests.post(url, data=data)
        content = json.loads(resp.content)
        assert content['status'] == "OK", "Content: %s" % content
        self.default_usertoken = content['usertoken']['token']

    @classmethod
    def tearDownClass(self):
        #1. Stop rest server via POST request
        resp = requests.post(self.rest_base_url + "/shutdown")
        if resp.status_code == 200:
            resp_json = json.loads(resp.content) 
            assert resp_json['status'] == "OK", "Received error when shutting down server: %s" % resp_json['message']
        else:
            raise Exception("Unable to shutdown app server")
        #2. Drop database
        print "Dropping test database"
        self._drop_test_db()
        print "  Complete."

        #3. Delete app
        self._delete_testapp()

    @classmethod
    def _drop_test_db(self):
        mysql_cmd = "mysql -u %s -p%s -h %s -P %s" % (self.test_conf.db_user,
                                                      self.test_conf.db_password,
                                                      self.test_conf.db_host,
                                                      self.test_conf.db_port)
        drop_db_cmd = mysql_cmd + ' -e "drop database %s"' % self.test_conf.db_name
        rc = call([drop_db_cmd],shell=True)
        if rc != 0:
            raise Exception("Unable to delete database")

        #Clear Redis db
        conn = redis.StrictRedis(host=self.test_conf.redis_host, port=self.test_conf.redis_port, db=self.test_conf.redis_sessioneventdb)
        conn.flushdb()

        conn = redis.StrictRedis(host=self.test_conf.redis_host, port=self.test_conf.redis_port, db=self.test_conf.redis_sysdb)
        conn.flushdb()
        

    @classmethod
    def load_fixture(self, fixture_name):
        fixture_file = SPSHOME + "integration-tests/fixtures/" + fixture_name + ".sql"
        fixture_cmd = self.mysql_cmd + " < %s" % fixture_file 
        rc = call([fixture_cmd],shell=True)
        if rc != 0:
            raise Exception("Error loading fixture: %s" % fixture_name)

    @classmethod
    def _delete_testapp(self):
        delete_cmd = "rm -rf %s" % TESTAPPHOME
        rc = call([delete_cmd],shell=True)
        if rc != 0:
            raise Exception("Unable to delete database")

    ##
    # Helper methods
    # TODO: Move these to diff module
    ##
    def content_from_get(self, url):
        resp = requests.get(url)
        return json.loads(resp.content)

    def token_url_param(self, apptoken, usertoken):
        return "apptoken=%s&usertoken=%s" %\
            (apptoken, usertoken)

    def get_user_profile(self,apptoken, userid, usertoken):
        profile_url = self.rest_base_url + "/user/%s?%s" % (userid, self.token_url_param(apptoken, usertoken))

        resp = requests.get(profile_url)
        content = json.loads(resp.content)
        return content

    def get_session(self, apptoken, usertoken, sessionid=None):
        if sessionid:
            url = self.rest_base_url + "/session/%s?%s" % (sessionid, self.token_url_param(apptoken, usertoken))
        else:
            url = self.rest_base_url + "/session?%s" % (self.token_url_param(apptoken, usertoken))

        resp = requests.get(url)
        content = json.loads(resp.content)
        return content

    def _add_beer(self, sessionid, beerid, usertoken):
        url = self.rest_base_url + "/session/%s/beer?%s" % (sessionid, self.token_url_param(self.apptoken, usertoken))
        data = { "beerid": beerid }
        resp = requests.post(url,data=data)
        content = json.loads(resp.content)
        self.assertEquals(content['status'], "OK")
        return content['sessionbeers']

class SBT(object):
    """
    Class to just hold some properties used for 
    Session Beer CRUD Tests
    """
    SESSION_CLOSED_ERRMSG = "Session is closed."
    
    #session-beer fixture data
    sessionid1 = 200
    sessionid2 = 201  #Session is closed
    sessionid3 = 202  #Session has closed beers
    sessionjoincd = 'abcd'
    userid1 = 101 #leader of sessionid 200
    userid2 = 102 #prtcp of sessionid 200
    user1_token = 'testtoken1'
    user2_token = 'testtoken2'

    tb1 = "tb1"
    tb2 = "tb2"
    tb3 = "tb3"
    tb4 = "tb4"
    tb5 = "tb5"

    beers = [tb1, tb2, tb3, tb4, tb5]
