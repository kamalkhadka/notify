-- ************** Users ************
CREATE TABLE "users"
(
 "id"         serial PRIMARY KEY,
 "first_name" varchar(50) NOT NULL,
 "last_name"  varchar(20) NOT NULL,
 "email"      varchar(50) NOT NULL,
 "password"   text NOT NULL
);

-- Contacts 

CREATE TABLE "contacts"
(
 "id"         serial PRIMARY KEY,
 "first_name" varchar(40) NOT NULL,
 "last_name"  varchar(20) NOT NULL,
 "phone"      varchar(50) NOT NULL,
 "email"      varchar(50) NOT NULL,
 "user_id"    integer NOT NULL,
 CONSTRAINT "FK_users_contacts" FOREIGN KEY ( "user_id" ) REFERENCES "users" ( "id" )
);

-- ************************************** "Groups"

CREATE TABLE "groups"
(
 "id"      serial PRIMARY KEY,
 "name"    varchar(10) NOT NULL,
 "user_id" integer NOT NULL,
 CONSTRAINT "FK_users_groups" FOREIGN KEY ( "user_id" ) REFERENCES "users" ( "id" )
);

-- ************************************** "Messages"

CREATE TABLE "messages"
(
 "id"           serial PRIMARY KEY,
 "message_type" bit NOT NULL,
 "message"      varchar(50) NOT NULL,
 "user_id"      integer NOT NULL,
 CONSTRAINT "FK_users_messages" FOREIGN KEY ( "user_id" ) REFERENCES "users" ( "id" )
);

-- ************************************** "Templates"

CREATE TABLE "templates"
(
 "id"            serial PRIMARY KEY,
 "name"          varchar(50) NOT NULL,
 "text"          varchar(50) NOT NULL,
 "template_type" bit NOT NULL
);


-- ************************************** "Contacts_Groups"

CREATE TABLE "contacts_groups"
(
 "id"         serial PRIMARY KEY,
 "contact_id" integer NOT NULL,
 "group_id"   integer NOT NULL,
 CONSTRAINT "FK_contacts" FOREIGN KEY ( "contact_id" ) REFERENCES "contacts" ( "id" ),
 CONSTRAINT "FK_groups" FOREIGN KEY ( "group_id" ) REFERENCES "groups" ( "id" )
);
