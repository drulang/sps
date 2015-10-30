use sps;

insert into app(appid, name, datecreated, active) values (1, "testapp",NOW(), "Y");
insert into apptoken(appid, apptoken, datecreated) values (1, "testtoken", NOW());

# Insert rating values
insert ignore into ratingval (ratingval, name, displayname) values (1, 'One', 'One');
insert ignore into ratingval (ratingval, name, displayname) values (2, 'Two', 'Two');
insert ignore into ratingval (ratingval, name, displayname) values (3, 'Three', 'Three');
insert ignore into ratingval (ratingval, name, displayname) values (4, 'Four', 'Four');
insert ignore into ratingval (ratingval, name, displayname) values (5, 'Five', 'Five');

# Session status
insert ignore into sessionstatustyp (seqno, sessionstatustypcd, name, displayname) values (1, 'new','New','New');
insert ignore into sessionstatustyp (seqno, sessionstatustypcd, name, displayname) values (2, 'inprg','In Progress','In Progress');
insert ignore into sessionstatustyp (seqno, sessionstatustypcd, name, displayname) values (3, 'clsd','Closed','Closed');

# Beer Session Status Type
insert ignore into beersessionstatustyp (seqno, beersessionstatustypcd, name, displayname)
	values (1, 'new', 'New', 'New');
insert ignore into beersessionstatustyp (seqno, beersessionstatustypcd, name, displayname)
	values (2, 'actv', 'Active', 'Active');
insert ignore into beersessionstatustyp (seqno, beersessionstatustypcd, name, displayname)
	values (3, 'clsd', 'Closed', 'Closed');

# Rating Type code
insert ignore into ratingtyp (ratingtypcd, name, displayname)
	values ('hpy','Hoppy','Hoppy');
insert ignore into ratingtyp (ratingtypcd, name, displayname)
	values ('mlt','Malty','Malty');

# User Role
insert ignore into userroletyp (userroletypcd, name, displayname) values ('ldr', 'Leader','Leader');
insert ignore into userroletyp (userroletypcd, name, displayname) values ('prtcp', 'Participant','Participant');

