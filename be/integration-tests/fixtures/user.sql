use spstest;

insert into user(userid, email, username, password, salt, datecreated)
    values (5, 'testuser5@email.com', 'testuser5', 'testpassword5', 'testsalt5', NOW());

insert into usertoken (userid, usertoken, datecreated)
    values (5, 'testtoken5', NOW());
