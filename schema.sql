-- ************** Users ************
CREATE TABLE "Users"
(
 "id"         integer NOT NULL,
 "first_name" varchar(50) NOT NULL,
 "last_name"  varchar(20) NOT NULL,
 "email"      varchar(50) NOT NULL,
 "password"   varchar(50) NOT NULL,
 CONSTRAINT "PK_users" PRIMARY KEY ( "id" )
);

-- Contacts 

CREATE TABLE "Contacts"
(
 "id"         integer NOT NULL,
 "first_name" varchar(40) NOT NULL,
 "last_name"  varchar(20) NOT NULL,
 "phone"      varchar(50) NOT NULL,
 "email"      varchar(50) NOT NULL,
 "user_id"    integer NOT NULL,
 CONSTRAINT "PK_contacts" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_users_contacts" FOREIGN KEY ( "user_id" ) REFERENCES "Users" ( "id" )
);

-- ************************************** "Groups"

CREATE TABLE "Groups"
(
 "id"      integer NOT NULL,
 "name"    varchar(10) NOT NULL,
 "user_id" integer NOT NULL,
 CONSTRAINT "PK_groups" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_users_groups" FOREIGN KEY ( "user_id" ) REFERENCES "Users" ( "id" )
);

-- ************************************** "Messages"

CREATE TABLE "Messages"
(
 "id"           integer NOT NULL,
 "message_type" bit NOT NULL,
 "message"      varchar(50) NOT NULL,
 "user_id"      integer NOT NULL,
 CONSTRAINT "PK_message" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_users_messages" FOREIGN KEY ( "user_id" ) REFERENCES "Users" ( "id" )
);

-- ************************************** "Templates"

CREATE TABLE "Templates"
(
 "id"            integer NOT NULL,
 "name"          varchar(50) NOT NULL,
 "text"          varchar(50) NOT NULL,
 "template_type" bit NOT NULL,
 CONSTRAINT "PK_templates" PRIMARY KEY ( "id" )
);


-- ************************************** "Contacts_Groups"

CREATE TABLE "Contacts_Groups"
(
 "id"         integer NOT NULL,
 "contact_id" integer NOT NULL,
 "group_id"   integer NOT NULL,
 CONSTRAINT "PK_contacts_groups" PRIMARY KEY ( "id" ),
 CONSTRAINT "FK_contacts" FOREIGN KEY ( "contact_id" ) REFERENCES "Contacts" ( "id" ),
 CONSTRAINT "FK_groups" FOREIGN KEY ( "group_id" ) REFERENCES "Groups" ( "id" )
);
