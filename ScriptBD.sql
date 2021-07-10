-- Author: Armando Elorriaga
-- Script BD 
-- Nota: el esquema y tabla se crearon con un usuario con nombre y contraseña: mandi

-- Database: estadisticas

-- DROP DATABASE estadisticas;

CREATE DATABASE estadisticas
    WITH 
    OWNER = mandi
    ENCODING = 'UTF8'
    LC_COLLATE = 'es_ES.UTF-8'
    LC_CTYPE = 'es_ES.UTF-8'
    TABLESPACE = pg_default
    CONNECTION LIMIT = -1;
	
	


-- Table: public.estadisticas_lecturas

-- DROP TABLE public.estadisticas_lecturas;

CREATE TABLE public.estadisticas_lecturas
(
    ip character varying COLLATE pg_catalog."default",
    num_lecturas integer,
    anchob_total integer,
    anchob_media double precision,
    nocturno integer,
    nocturno_anchob_total integer,
    nocturno_anchob_media double precision,
    diurno integer,
    diurno_anchob_total integer,
    diurno_anchob_media double precision,
    id integer NOT NULL DEFAULT nextval('estadisticas_lecturas_id_seq'::regclass),
    fecha character varying COLLATE pg_catalog."default",
    CONSTRAINT estadisticas_lecturas_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.estadisticas_lecturas
    OWNER to mandi;
	

-- Table: public.estadisticas_nodos

-- DROP TABLE public.estadisticas_nodos;

CREATE TABLE public.estadisticas_nodos
(
    fecha date,
    nodos_total integer,
    nodos_lecturas integer,
    nodos_media double precision,
    nodos_nocturnos_total integer,
    nodos_nocturnos_lecturas integer,
    nodos_nocturnos_media double precision,
    nodos_diurnos_total integer,
    nodos_diurnos_lecturas integer,
    nodos_diurnos_media double precision,
    id integer NOT NULL DEFAULT nextval('estadisticas_nodos_id_seq1'::regclass),
    CONSTRAINT estadisticas_nodos_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.estadisticas_nodos
    OWNER to mandi;
	
	


-- Table: public.registro_nodos

-- DROP TABLE public.registro_nodos;

CREATE TABLE public.registro_nodos
(
    fecha timestamp without time zone,
    num_nodos integer,
    id integer NOT NULL DEFAULT nextval('registro_nodos_id_seq1'::regclass),
    CONSTRAINT registro_nodos_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.registro_nodos
    OWNER to mandi;
	
	
	
-- Table: public.registros_lecturas

-- DROP TABLE public.registros_lecturas;

CREATE TABLE public.registros_lecturas
(
    ip character varying COLLATE pg_catalog."default",
    anchob integer,
    fecha character varying COLLATE pg_catalog."default",
    id integer NOT NULL DEFAULT nextval('registros_lecturas_id_seq'::regclass),
    CONSTRAINT registros_lecturas_pkey PRIMARY KEY (id)
)
WITH (
    OIDS = FALSE
)
TABLESPACE pg_default;

ALTER TABLE public.registros_lecturas
    OWNER to mandi;

	