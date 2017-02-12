USE codem;

INSERT INTO users
	(uniqname, admin)
VALUES
	('circle', TRUE),
	('madchef', TRUE),
	('ridleyscot', FALSE),
	('chrisnolan', FALSE),
	('eliakazan', FALSE),
    ('denzelwash', FALSE),
	('angelina', FALSE),
	('spielberg', FALSE),
	('wesandersn', FALSE),
	('bradbird', FALSE),
	('timburton', FALSE),
	
	("samjackson", FALSE ),
    ("craignel", FALSE ),
    ("foxspencer", FALSE),
	("violadavis", FALSE),
	("russhrons" , FALSE),
	("stephhend" , FALSE)
;



INSERT INTO events
	(eventID, name, host,datetime, location, description, accessCode, open, points, semester)
VALUES
	(1,"Incredible Mass Meeting","bradbird@umich.edu", '2004-11-05 18:30:00', '1690 BBB' , "Enjoy free food, games, and learn about the club at this mass meeting.", "f3ba8", 0 , 1.00, 'F2004' ),
    (2,"Fencing Workshop", "denzelwash@umich.edu", '2016-12-25 19:00:00', '1010 DOW',"Denzel will be walking us through the new 'fencing' programming techniques, and how they can apply to everything you do.", "1e66f",0,1.50, 'F2016'),
	(3,"Something good", "denzelwash@umich.edu", '2017-1-25 19:00:00', '1012 EECS',"What will it be???", "d72h22", 1, 1.50, 'W2017')
;

INSERT INTO attendance
	(attID, uniqname, eventID)
VALUES
    ( 1 , "madchef"   , 1 ),
    ( 2 , "circle"    , 1 ),
    ( 3 , "samjackson", 1 ),
    ( 4 , "craignel"  , 1 ),
    ( 5 , "foxspencer", 1 ),
	( 6 , "violadavis", 2 ),
	( 7 , "russhrons" , 2 ),
	( 8 , "stephhend" , 2 ),
	( 9 , "madchef"   , 2 ),
    (10 , "circle"    , 2 ),
	(11 , "denzelwash", 2 ),
	(12 , "madchef"   , 3 )
;
