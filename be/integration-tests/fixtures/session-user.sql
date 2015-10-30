use spstest;
##
# User 1
##
insert into user (userid, email, username, password, salt, datecreated)
    values (101, 'te1@test.com', 'testuser1','testpassword1','testsalt1',NOW());

insert into usertoken (userid, usertoken, datecreated) values (101, 'testtoken1',NOW());

##
# User 2
##
insert into user (userid, email, username, password, salt, datecreated)
    values (102, 'te2@test.com', 'testuser2','testpassword2','testsalt2',NOW());

insert into usertoken (userid, usertoken, datecreated) values (102, 'testtoken2',NOW());

##
# User 3
##
insert into user (userid, email, username, password, salt, datecreated)
    values (103, 'te3@test.com', 'testuser3','testpassword3','testsalt3',NOW());

insert into usertoken (userid, usertoken, datecreated) 
    values (103, 'testtoken3',NOW());
##
# User 4
##
insert into user (userid, email, username, password, salt, datecreated)
    values (104, 'te4@test.com', 'testuser4','testpassword4','testsalt4',NOW());

insert into usertoken (userid, usertoken, datecreated) values (104, 'testtoken4',NOW());

##
# User 5
##
insert into user (userid, email, username, password, salt, datecreated)
    values (105, 'te5@test.com', 'testuser5','testpassword5','testsalt5',NOW());

insert into usertoken (userid, usertoken, datecreated) values (105, 'testtoken5',NOW());

##
# User 6
##
insert into user (userid, email, username, password, salt, datecreated)
    values (106, 'te6@test.com', 'testuser6','testpassword6','testsalt6',NOW());

insert into usertoken (userid, usertoken, datecreated) values (106, 'testtoken6',NOW());

##
# Session 1
##
insert into session(sessionid, sessionstatustypcd, sessionjoincd, name, datecreated, dateopen)
    values (200, 'new','abcd','t',NOW(),'2011-01-01 3:30:30');

 insert into session_has_user(sessionid, userid, userroletypcd)
    values (200, 101, 'ldr');

 insert into session_has_user(sessionid, userid, userroletypcd)
    values (200, 104, 'prtcp');

 insert into session_has_user(sessionid, userid, userroletypcd)
    values (200, 105, 'prtcp');

##
# Session 2
##
insert into session(sessionid, sessionstatustypcd, sessionjoincd, name, datecreated, dateopen)
    values (201, 'new','efgh','u',NOW(),'2011-01-01 3:30:30');

 insert into session_has_user(sessionid, userid, userroletypcd)
    values (201, 106, 'ldr');

##
# Session 3
##
insert into session(sessionid, sessionstatustypcd, sessionjoincd, name, datecreated, dateopen)
    values (202, 'new','efgh','u',NOW(),'2011-01-01 3:30:30');

 insert into session_has_user(sessionid, userid, userroletypcd)
    values (202, 106, 'ldr');

 insert into session_has_user(sessionid, userid, userroletypcd)
    values (202, 105, 'prtcp');
