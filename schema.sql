-- ************** Users ************
CREATE TABLE users (
        id SERIAL NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT NOT NULL,
        authy_id TEXT NOT NULL,
        is_valid BOOLEAN,
        password TEXT NOT NULL,
        PRIMARY KEY (id),
        UNIQUE (email)
);

-- Contacts 

CREATE TABLE contacts (
        id SERIAL NOT NULL,
        first_name TEXT NOT NULL,
        last_name TEXT NOT NULL,
        email TEXT NOT NULL,
        user_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
);

-- ************************************** "Groups"

CREATE TABLE groups (
        id SERIAL NOT NULL,
        name TEXT NOT NULL,
        user_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(user_id) REFERENCES users (id)
);

-- ************************************** "Messages"

-- CREATE TABLE messages (
--         id SERIAL NOT NULL,
--         -- message_type BOOLEAN NOT NULL,
--         name TEXT NOT NULL,
--         user_id INTEGER,
--         PRIMARY KEY (id),
--         FOREIGN KEY(user_id) REFERENCES users (id)
-- );

-- ************************************** "Templates"

-- CREATE TABLE templates (
--         id SERIAL NOT NULL,
--         name TEXT NOT NULL,
--         text TEXT NOT NULL,
--         template_type BOOLEAN NOT NULL,
--         PRIMARY KEY (id)
-- );


-- ************************************** "Contacts_Groups"

CREATE TABLE contacts_groups (
        id SERIAL NOT NULL,
        contact_id INTEGER,
        group_id INTEGER,
        PRIMARY KEY (id),
        FOREIGN KEY(contact_id) REFERENCES contacts (id),
        FOREIGN KEY(group_id) REFERENCES groups (id)
);

CREATE TABLE email_limit (
        id SERIAL NOT NULL,
        date TIMESTAMP WITHOUT TIME ZONE,
        count INTEGER,
        PRIMARY KEY (id)
);
