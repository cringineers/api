-- DROP SCHEMA tag_system;

CREATE SCHEMA tag_system;

-- DROP SEQUENCE tag_system.newtable_id_seq;

CREATE SEQUENCE tag_system.newtable_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE tag_system.object_types_id_seq;

CREATE SEQUENCE tag_system.object_types_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE tag_system.objects_id_seq;

CREATE SEQUENCE tag_system.objects_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE tag_system.tag_group_id_seq;

CREATE SEQUENCE tag_system.tag_group_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE tag_system.tags_id_seq;

CREATE SEQUENCE tag_system.tags_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE tag_system.tags_id_seq1;

CREATE SEQUENCE tag_system.tags_id_seq1
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;
-- DROP SEQUENCE tag_system.users_id_seq;

CREATE SEQUENCE tag_system.users_id_seq
	INCREMENT BY 1
	MINVALUE 1
	MAXVALUE 2147483647
	START 1
	CACHE 1
	NO CYCLE;-- tag_system.object_types definition

-- Drop table

-- DROP TABLE tag_system.object_types;

CREATE TABLE tag_system.object_types (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" text NOT NULL,
	CONSTRAINT object_types_pk PRIMARY KEY (id)
);


-- tag_system.tag_group definition

-- Drop table

-- DROP TABLE tag_system.tag_group;

CREATE TABLE tag_system.tag_group (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" text NOT NULL,
	"binary" bool NOT NULL,
	CONSTRAINT tag_group_pk PRIMARY KEY (id)
);


-- tag_system.users definition

-- Drop table

-- DROP TABLE tag_system.users;

CREATE TABLE tag_system.users (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	login text NOT NULL,
	hash text NOT NULL
);


-- tag_system.objects definition

-- Drop table

-- DROP TABLE tag_system.objects;

CREATE TABLE tag_system.objects (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"name" text NULL,
	source_path text NOT NULL,
	"type" int4 NOT NULL,
	CONSTRAINT objects_pk PRIMARY KEY (id),
	CONSTRAINT objects_fk FOREIGN KEY ("type") REFERENCES tag_system.object_types(id)
);


-- tag_system.tags definition

-- Drop table

-- DROP TABLE tag_system.tags;

CREATE TABLE tag_system.tags (
	id int4 NOT NULL GENERATED ALWAYS AS IDENTITY,
	"text" varchar NOT NULL,
	latent_space bytea NULL,
	"name" text NOT NULL,
	group_id int4 NOT NULL,
	CONSTRAINT tags_pk PRIMARY KEY (id),
	CONSTRAINT tags_fk FOREIGN KEY (group_id) REFERENCES tag_system.tag_group(id)
);


-- tag_system.object_tags definition

-- Drop table

-- DROP TABLE tag_system.object_tags;

CREATE TABLE tag_system.object_tags (
	object_id int4 NOT NULL,
	tag_id int4 NOT NULL,
	CONSTRAINT object_tags_fk FOREIGN KEY (object_id) REFERENCES tag_system.objects(id) ON DELETE CASCADE,
	CONSTRAINT object_tags_fk_1 FOREIGN KEY (tag_id) REFERENCES tag_system.tags(id)
);


INSERT INTO tag_system.users (login, hash)
VALUES ('cool_user', '$2b$12$vjUOaUTtj9QDmBnKZ3UO6O01tQnAYOnHnmo.u.xkWFdvLeonOcTv6')
