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
# Beers
##
insert into beer (beerid, rawdata, datecreated)
    values ('tb1', null, NOW());

insert into beer (beerid, rawdata, datecreated)
    values ('tb2', null, NOW());

insert into beer (beerid, rawdata, datecreated)
    values ('tb3', null, NOW());

insert into beer (beerid, rawdata, datecreated)
    values ('tb4', null, NOW());

insert into beer (beerid, rawdata, datecreated)
    values ('tb5', null, NOW());

##
# Session 1
##
insert into session(sessionid, sessionstatustypcd, sessionjoincd, name, datecreated, dateopen)
    values (200, 'new','abcd','t',NOW(),'2011-01-01 3:30:30');

 insert into session_has_user(sessionid, userid, userroletypcd)
    values (200, 101, 'ldr');
 insert into session_has_user(sessionid, userid, userroletypcd)
    values (200, 102, 'prtcp');

#Add all beers to session 1 
insert into session_has_beer(sessionbeerid, sessionid, beerid, beersessionstatustypcd)
    values (2, 200, 'tb1', 'new');
insert into session_has_beer(sessionbeerid, sessionid, beerid, beersessionstatustypcd)
    values (3, 200, 'tb2', 'new');
insert into session_has_beer(sessionbeerid, sessionid, beerid, beersessionstatustypcd)
    values (4, 200, 'tb3', 'new');

#Create beer ratings
insert into beerrating (beerratingid, sessionbeerid, ratingtypcd, ratingval, userid, comment, daterated)
    values (1, 2,'hpy',5,101,"Good beer.",NOW());

insert into beerrating (beerratingid, sessionbeerid, ratingtypcd, ratingval, userid, comment, daterated)
    values (2, 2,'mlt',5,102,"decent beer.",NOW());

#Used for edit test
insert into beerrating (beerratingid, sessionbeerid, ratingtypcd, ratingval, userid, comment, daterated)
    values (5, 2,'mlt',5,101,"used for edit test",NOW());

##
# Session 2
##
insert into session(sessionid, sessionstatustypcd, sessionjoincd, name, datecreated, dateopen)
    values (201, 'clsd','abcd','t',NOW(),'2011-01-01 3:30:30');

 insert into session_has_user(sessionid, userid, userroletypcd)
    values (201, 101, 'ldr');
 insert into session_has_user(sessionid, userid, userroletypcd)
    values (201, 102, 'prtcp');

##
# Session 3
##
insert into session(sessionid, sessionstatustypcd, sessionjoincd, name, datecreated, dateopen)
    values (202, 'new','abcd','t',NOW(),'2011-01-01 3:30:30');

 insert into session_has_user(sessionid, userid, userroletypcd)
    values (202, 101, 'ldr');
 insert into session_has_user(sessionid, userid, userroletypcd)
    values (202, 102, 'prtcp');

insert into session_has_beer(sessionbeerid, sessionid, beerid, beersessionstatustypcd)
    values (1, 202, 'tb1', 'clsd');

insert into beerrating (beerratingid, sessionbeerid, ratingtypcd, ratingval, userid, comment, daterated)
    values (3, 1,'mlt',5,101,"decent beer.",NOW());

