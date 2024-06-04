/* ZIPCODES */
SELECT * FROM app_zipcodes;

/* NEIGHBORHOODS */
SELECT * FROM app_neighborhoods;

INSERT INTO app_neighborhoods
VALUES (0, 'Not assigned', NOW());

INSERT INTO app_neighborhoods
VALUES (1, 'Kimbrook', NOW());

/* NEIGHBORS */
SELECT * FROM app_neighbors;

/* ADDESSES */
SELECT * FROM app_addresses;

INSERT INTO app_addresses
VALUES ('Neighbor', 'Host', '8328 Radian Path',
	   'Baldwinsville', 'New York', '13027', 1, 1);

/* EVENTS */
SELECT * FROM app_events;

INSERT INTO app_events
VALUES (12, 1, 'Coding this website', 'neighborhost.com', CURRENT_DATE, CURRENT_DATE,
	   CURRENT_TIME, CURRENT_TIME, 'No', '8328 Radian Path', 'Baldwinsville', 'New York', 
		'13027', 'true', 'none', NOW());

/* VERIFICATIONS */
SELECT * FROM app_verifications;

INSERT INTO app_verifications
VALUES (1, '000001', NOW(), 1);

/* FRIENDS */
SELECT * FROM app_friends;

INSERT INTO app_friends
VALUES(3, 'Accepted', NOW(), 1);

/* FRIEND_REQUESTS */
SELECT * FROM app_friend_requests;

INSERT INTO app_friend_requests
VALUES (1, 3, NOW(), 1);

/* 2. TRACKING USER ACTIVITY */

/* HOME_CLICKS */
SELECT * FROM app_home_clicks;

INSERT INTO app_home_clicks
VALUES (1, NOW(), 1);
		
/* LOGINS */
SELECT * FROM app_logins;

INSERT INTO app_logins (login_id, neighbor_id, login_datetime, login_ip, login_rememberme)
VALUES (1, 1, NOW(), '127.0.0.1', 'false');

/* SIGNOUTS */
SELECT * FROM app_signouts;

INSERT INTO app_signouts
VALUES (1, 1, NOW());

/* VERIFICATION_SKIPS */
SELECT * FROM app_verification_skips;

INSERT INTO app_verification_skips
VALUES (1, 1, NOW());

/* VERIFY_LATERS */
SELECT * FROM app_verify_laters;

INSERT INTO app_verify_laters
VALUES (1, 1, NOW());

/* VERIFIERS */
SELECT * FROM app_verifiers;

INSERT INTO app_verifiers
VALUES (1, 1, NOW());

/* FRIEND_CHECKS */
SELECT * FROM app_friend_checks;

INSERT INTO app_friend_checks
VALUES (1, NOW(), 1);

/* LOCATION_FILTERS */
SELECT * FROM app_location_filters;

INSERT INTO app_location_filters
VALUES (1, 'All', NOW(), 1);

/* VIEW_FILTERS */
SELECT * FROM app_view_filters;

INSERT INTO app_view_filters
VALUES (1, 'List view', NOW(), 1);

/* CALENDAR_FILTERS */
SELECT * FROM app_calendar_filters;

INSERT INTO app_calendar_filters
VALUES (1, 5, 2024, NOW(), 1);

/* DATE_FILTERS */
SELECT * FROM app_date_filters;

INSERT INTO app_date_filters
VALUES (1, 'On', NOW()::timestamp::date, NOW(), 1);

/* EVENT_VIEWS */
SELECT * FROM app_event_views;

INSERT INTO app_event_views
VALUES (1, NOW(), 1, 1);

/* FRIEND_VIEWS */
SELECT * FROM app_friend_views;

INSERT INTO app_friend_views
VALUES (1, 3, NOW(), 1);

/* VISITS */
SELECT * FROM app_visits;

INSERT INTO app_visits
VALUES (1, '127.0.0.1', NOW());