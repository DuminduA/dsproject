--
-- PostgreSQL database dump
--

-- Dumped from database version 13.4
-- Dumped by pg_dump version 13.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: workspace; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.workspace (
    id uuid NOT NULL,
    name character varying(150) NOT NULL,
    credit double precision NOT NULL,
    created_at timestamp without time zone,
    modified_at timestamp without time zone
);


ALTER TABLE public.workspace OWNER TO postgres;

--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
b5b4e08c5bef
\.


--
-- Data for Name: workspace; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.workspace (id, name, credit, created_at, modified_at) FROM stdin;
ff02e026-1862-4271-b634-d9e3283190f0	test1	79.40000000000117	2024-03-12 15:24:59.846	2024-03-12 15:24:59.846008
\.


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: workspace workspace_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.workspace
    ADD CONSTRAINT workspace_pkey PRIMARY KEY (id);


--
-- Name: ix_workspace_id; Type: INDEX; Schema: public; Owner: postgres
--

CREATE UNIQUE INDEX ix_workspace_id ON public.workspace USING btree (id);


--
-- PostgreSQL database dump complete
--

