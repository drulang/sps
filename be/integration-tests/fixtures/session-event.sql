use spstest;

##
# User 1
##
insert into user (userid, email, username, password, salt, datecreated)
    values (101, 'te1@test.com', 'testuser1','testpassword1','testsalt1',NOW());

insert into usertoken (userid, usertoken, datecreated) values (101, 'testtoken1',NOW());

##
# Session 1
##
insert into session(sessionid, sessionstatustypcd, sessionjoincd, name, datecreated, dateopen)
    values (100, 'new','a','t',NOW(),'2011-01-01 3:30:30');

 insert into session_has_user(sessionid, userid, userroletypcd)
    values (100, 101, 'ldr');
