use sps;

insert into user (userid, email, username, password, salt, datecreated) 
	values (1, 'te@test.com', 'testuser','testpassword','testsalt',NOW());
insert into usertoken (userid, usertoken, datecreated) values (1, 'testtoken',NOW());

insert into user (userid, email, username, password, salt, datecreated) 
	values (2, 'te@test.com2', 'testuser2','testpassword2','testsalt2',NOW());
insert into usertoken (userid, usertoken, datecreated) values (2, 'testtoken2',NOW());


#Create a session
insert into session (sessionid, sessionstatustypcd, sessionjoincd, name, datecreated)
	values (1, 'new', 'abcd','Dev Session 1', NOW());

insert into session_has_user(sessionid, userid, userroletypcd)
	values (1, 1, 'ldr');

insert into beer (beerid, rawdata, datecreated)
	values ('tb1', null, NOW());
insert into beer (beerid, rawdata, datecreated)
	values ('tb2', null, NOW());
insert into beer (beerid, rawdata, datecreated)
	values ('tb3', null, NOW());

insert into session_has_beer (sessionbeerid, sessionid, beerid, beersessionstatustypcd)
	values (1, 1, 'tb1', 'new');
insert into session_has_beer (sessionbeerid, sessionid, beerid, beersessionstatustypcd)
	values (2, 1, 'tb2', 'new');
insert into session_has_beer (sessionbeerid, sessionid, beerid, beersessionstatustypcd)
	values (3, 1, 'tb3', 'new');