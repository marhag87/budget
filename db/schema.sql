--
-- PostgreSQL database dump
--

-- Dumped from database version 10.1
-- Dumped by pg_dump version 10.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

DROP DATABASE budget;
--
-- Name: budget; Type: DATABASE; Schema: -; Owner: -
--

CREATE DATABASE budget WITH TEMPLATE = template0 ENCODING = 'UTF8' LC_COLLATE = 'en_GB.UTF-8' LC_CTYPE = 'en_GB.UTF-8';


\connect budget

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON EXTENSION plpgsql IS 'PL/pgSQL procedural language';


SET search_path = public, pg_catalog;

--
-- Name: insert_title(text); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION insert_title(f1 text) RETURNS TABLE(id integer)
    LANGUAGE sql
    AS $_$ WITH CTE AS (INSERT INTO title ("name") VALUES ($1) ON CONFLICT DO NOTHING RETURNING "id") SELECT "id" FROM title WHERE "name"=$1 UNION ALL SELECT * FROM CTE; $_$;


--
-- Name: transactions_for_month(integer, integer); Type: FUNCTION; Schema: public; Owner: -
--

CREATE FUNCTION transactions_for_month(f1 integer, f2 integer) RETURNS TABLE(title text, date date, amount integer, balance integer, category text)
    LANGUAGE sql
    AS $_$ SELECT title.name as title, date, amount, balance, category.name as category FROM transaction JOIN title ON title.id = transaction.title_id JOIN category ON category.id = transaction.category_id WHERE date_trunc('month', date) = cast(cast($1 as text) || '-' || cast($2 as text) || '-01' as date) $_$;


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: category; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE category (
    id integer NOT NULL,
    name text NOT NULL
);


--
-- Name: category_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE category_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: category_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE category_id_seq OWNED BY category.id;


--
-- Name: category_map; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE category_map (
    id integer NOT NULL,
    title_id integer NOT NULL,
    category_id integer NOT NULL
);


--
-- Name: category_map_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE category_map_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: category_map_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE category_map_id_seq OWNED BY category_map.id;


--
-- Name: title; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE title (
    id integer NOT NULL,
    name text NOT NULL
);


--
-- Name: title_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE title_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: title_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE title_id_seq OWNED BY title.id;


--
-- Name: transaction; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE transaction (
    id integer NOT NULL,
    title_id integer NOT NULL,
    date date NOT NULL,
    amount integer NOT NULL,
    balance integer NOT NULL,
    category_id integer NOT NULL
);


--
-- Name: transaction_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE transaction_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: transaction_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE transaction_id_seq OWNED BY transaction.id;


--
-- Name: category id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY category ALTER COLUMN id SET DEFAULT nextval('category_id_seq'::regclass);


--
-- Name: category_map id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY category_map ALTER COLUMN id SET DEFAULT nextval('category_map_id_seq'::regclass);


--
-- Name: title id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY title ALTER COLUMN id SET DEFAULT nextval('title_id_seq'::regclass);


--
-- Name: transaction id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY transaction ALTER COLUMN id SET DEFAULT nextval('transaction_id_seq'::regclass);


--
-- Name: category_map category_map_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY category_map
    ADD CONSTRAINT category_map_pkey PRIMARY KEY (id);


--
-- Name: category category_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_name_key UNIQUE (name);


--
-- Name: category category_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY category
    ADD CONSTRAINT category_pkey PRIMARY KEY (id);


--
-- Name: title title_name_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY title
    ADD CONSTRAINT title_name_key UNIQUE (name);


--
-- Name: title title_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY title
    ADD CONSTRAINT title_pkey PRIMARY KEY (id);


--
-- Name: transaction transaction_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_pkey PRIMARY KEY (id);


--
-- Name: category_map category_map_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY category_map
    ADD CONSTRAINT category_map_category_id_fkey FOREIGN KEY (category_id) REFERENCES category(id);


--
-- Name: category_map category_map_title_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY category_map
    ADD CONSTRAINT category_map_title_id_fkey FOREIGN KEY (title_id) REFERENCES title(id);


--
-- Name: transaction transaction_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_category_id_fkey FOREIGN KEY (category_id) REFERENCES category(id);


--
-- Name: transaction transaction_title_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY transaction
    ADD CONSTRAINT transaction_title_id_fkey FOREIGN KEY (title_id) REFERENCES title(id);


--
-- PostgreSQL database dump complete
--

