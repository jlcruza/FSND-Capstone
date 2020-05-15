--
-- PostgreSQL database dump
--

-- Dumped from database version 12.2
-- Dumped by pg_dump version 12.2

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
-- Name: actors; Type: TABLE; Schema: public; Owner: jorgecruz
--

CREATE TABLE public.actors (
    id integer NOT NULL,
    name character varying NOT NULL,
    age integer NOT NULL,
    gender character varying NOT NULL,
    picture_link character varying,
    bio character varying
);


ALTER TABLE public.actors OWNER TO jorgecruz;

--
-- Name: actors_id_seq; Type: SEQUENCE; Schema: public; Owner: jorgecruz
--

CREATE SEQUENCE public.actors_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.actors_id_seq OWNER TO jorgecruz;

--
-- Name: actors_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jorgecruz
--

ALTER SEQUENCE public.actors_id_seq OWNED BY public.actors.id;


--
-- Name: casts; Type: TABLE; Schema: public; Owner: jorgecruz
--

CREATE TABLE public.casts (
    id integer NOT NULL,
    actors_id integer NOT NULL,
    movies_id integer NOT NULL
);


ALTER TABLE public.casts OWNER TO jorgecruz;

--
-- Name: casts_id_seq; Type: SEQUENCE; Schema: public; Owner: jorgecruz
--

CREATE SEQUENCE public.casts_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.casts_id_seq OWNER TO jorgecruz;

--
-- Name: casts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jorgecruz
--

ALTER SEQUENCE public.casts_id_seq OWNED BY public.casts.id;


--
-- Name: movies; Type: TABLE; Schema: public; Owner: jorgecruz
--

CREATE TABLE public.movies (
    id integer NOT NULL,
    title character varying NOT NULL,
    released timestamp without time zone NOT NULL,
    picture_link character varying,
    synopsis character varying
);


ALTER TABLE public.movies OWNER TO jorgecruz;

--
-- Name: movies_id_seq; Type: SEQUENCE; Schema: public; Owner: jorgecruz
--

CREATE SEQUENCE public.movies_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.movies_id_seq OWNER TO jorgecruz;

--
-- Name: movies_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: jorgecruz
--

ALTER SEQUENCE public.movies_id_seq OWNED BY public.movies.id;


--
-- Name: actors id; Type: DEFAULT; Schema: public; Owner: jorgecruz
--

ALTER TABLE ONLY public.actors ALTER COLUMN id SET DEFAULT nextval('public.actors_id_seq'::regclass);


--
-- Name: casts id; Type: DEFAULT; Schema: public; Owner: jorgecruz
--

ALTER TABLE ONLY public.casts ALTER COLUMN id SET DEFAULT nextval('public.casts_id_seq'::regclass);


--
-- Name: movies id; Type: DEFAULT; Schema: public; Owner: jorgecruz
--

ALTER TABLE ONLY public.movies ALTER COLUMN id SET DEFAULT nextval('public.movies_id_seq'::regclass);


--
-- Data for Name: actors; Type: TABLE DATA; Schema: public; Owner: jorgecruz
--

COPY public.actors (id, name, age, gender, picture_link, bio) FROM stdin;
1	Actor 1	30	Female	sample.com	Romantic
2	Actor 2	28	Male	sample.com	Action
\.


--
-- Data for Name: casts; Type: TABLE DATA; Schema: public; Owner: jorgecruz
--

COPY public.casts (id, actors_id, movies_id) FROM stdin;
1	1	1
\.


--
-- Data for Name: movies; Type: TABLE DATA; Schema: public; Owner: jorgecruz
--

COPY public.movies (id, title, released, picture_link, synopsis) FROM stdin;
1	Movie 1	2010-08-15 00:00:00	movie.com	Actor 1 needs...
2	Movie 2	2010-05-20 00:00:00	movie.com	Actor 2 needs...
\.


--
-- Name: actors_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jorgecruz
--

SELECT pg_catalog.setval('public.actors_id_seq', 2, true);


--
-- Name: casts_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jorgecruz
--

SELECT pg_catalog.setval('public.casts_id_seq', 1, true);


--
-- Name: movies_id_seq; Type: SEQUENCE SET; Schema: public; Owner: jorgecruz
--

SELECT pg_catalog.setval('public.movies_id_seq', 2, true);


--
-- Name: actors actors_pkey; Type: CONSTRAINT; Schema: public; Owner: jorgecruz
--

ALTER TABLE ONLY public.actors
    ADD CONSTRAINT actors_pkey PRIMARY KEY (id);


--
-- Name: casts casts_pkey; Type: CONSTRAINT; Schema: public; Owner: jorgecruz
--

ALTER TABLE ONLY public.casts
    ADD CONSTRAINT casts_pkey PRIMARY KEY (id);


--
-- Name: movies movies_pkey; Type: CONSTRAINT; Schema: public; Owner: jorgecruz
--

ALTER TABLE ONLY public.movies
    ADD CONSTRAINT movies_pkey PRIMARY KEY (id);


--
-- Name: casts casts_actors_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jorgecruz
--

ALTER TABLE ONLY public.casts
    ADD CONSTRAINT casts_actors_id_fkey FOREIGN KEY (actors_id) REFERENCES public.actors(id);


--
-- Name: casts casts_movies_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: jorgecruz
--

ALTER TABLE ONLY public.casts
    ADD CONSTRAINT casts_movies_id_fkey FOREIGN KEY (movies_id) REFERENCES public.movies(id);


--
-- PostgreSQL database dump complete
--

