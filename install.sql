--
-- PostgreSQL database dump
--

SET statement_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = off;
SET check_function_bodies = false;
SET client_min_messages = warning;
SET escape_string_warning = off;

SET search_path = public, pg_catalog;

ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_version_id_fkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_update_date_id_fkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_size_id_fkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_rating_id_fkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_rating_count_id_fkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_price_id_fkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_icon_id_fkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_download_id_fkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_developer_id_fkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_category_id_fkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintime_application_id_fkey;
ALTER TABLE ONLY public.pointintime_permissions DROP CONSTRAINT pointintime_permissions_pointintime_id_fkey;
ALTER TABLE ONLY public.pointintime_permissions DROP CONSTRAINT pointintime_permissions_permission_id_fkey;
ALTER TABLE ONLY public.versions DROP CONSTRAINT versions_value_key;
ALTER TABLE ONLY public.versions DROP CONSTRAINT versions_pkey;
ALTER TABLE ONLY public.update_dates DROP CONSTRAINT updates_pkey;
ALTER TABLE ONLY public.sizes DROP CONSTRAINT sizes_pkey;
ALTER TABLE ONLY public.ratings DROP CONSTRAINT ratings_pkey;
ALTER TABLE ONLY public.rating_counts DROP CONSTRAINT rating_counts_pkey;
ALTER TABLE ONLY public.prices DROP CONSTRAINT prices_pkey;
ALTER TABLE ONLY public.pointsintime DROP CONSTRAINT pointsintim_pkey;
ALTER TABLE ONLY public.permissions DROP CONSTRAINT permissions_pkey;
ALTER TABLE ONLY public.icons DROP CONSTRAINT icons_sha1_key;
ALTER TABLE ONLY public.icons DROP CONSTRAINT icons_pkey;
ALTER TABLE ONLY public.icons DROP CONSTRAINT icons_id_key;
ALTER TABLE ONLY public.downloads DROP CONSTRAINT downloads_pkey;
ALTER TABLE ONLY public.developers DROP CONSTRAINT developers_pkey;
ALTER TABLE ONLY public.developers DROP CONSTRAINT developers_id_key;
ALTER TABLE ONLY public.content_ratings DROP CONSTRAINT content_ratings_pkey;
ALTER TABLE ONLY public.categories DROP CONSTRAINT categories_pkey;
ALTER TABLE ONLY public.applications DROP CONSTRAINT applications_pkey;
ALTER TABLE ONLY public.applications DROP CONSTRAINT applications_identifier_key;
ALTER TABLE public.versions ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.update_dates ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.sizes ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.ratings ALTER COLUMN value DROP DEFAULT;
ALTER TABLE public.ratings ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.rating_counts ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.prices ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.pointsintime ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.pointintime_permissions ALTER COLUMN permission_id DROP DEFAULT;
ALTER TABLE public.icons ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.downloads ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.developers ALTER COLUMN id DROP DEFAULT;
ALTER TABLE public.content_ratings ALTER COLUMN id DROP DEFAULT;
DROP SEQUENCE public.versions_id_seq;
DROP TABLE public.versions;
DROP SEQUENCE public.updates_id_seq;
DROP TABLE public.update_dates;
DROP SEQUENCE public.sizes_id_seq;
DROP TABLE public.sizes;
DROP SEQUENCE public.ratings_value_seq;
DROP SEQUENCE public.ratings_id_seq;
DROP TABLE public.ratings;
DROP SEQUENCE public.rating_counts_id_seq;
DROP TABLE public.rating_counts;
DROP SEQUENCE public.prices_id_seq;
DROP TABLE public.prices;
DROP SEQUENCE public.pointsintim_id_seq;
DROP TABLE public.pointsintime;
DROP SEQUENCE public.pit_permissions_permission_id_seq;
DROP TABLE public.pointintime_permissions;
DROP TABLE public.permissions;
DROP SEQUENCE public.permissions_id_seq;
DROP SEQUENCE public.icons_id_seq;
DROP TABLE public.icons;
DROP SEQUENCE public.downloads_id_seq;
DROP TABLE public.downloads;
DROP SEQUENCE public.developers_id_seq;
DROP TABLE public.developers;
DROP SEQUENCE public.content_ratings_id_seq;
DROP TABLE public.content_ratings;
DROP TABLE public.categories;
DROP SEQUENCE public.categories_id_seq;
DROP TABLE public.applications;
DROP SEQUENCE public.applications_id_seq;
DROP SCHEMA public;
--
-- Name: public; Type: SCHEMA; Schema: -; Owner: postgres
--

CREATE SCHEMA public;


ALTER SCHEMA public OWNER TO postgres;

--
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: postgres
--

COMMENT ON SCHEMA public IS 'standard public schema';


SET search_path = public, pg_catalog;

--
-- Name: applications_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE applications_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.applications_id_seq OWNER TO "android-permissions";

SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: applications; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE applications (
    id integer DEFAULT nextval('applications_id_seq'::regclass) NOT NULL,
    identifier text NOT NULL,
    name text,
    last_time_processed timestamp without time zone
);


ALTER TABLE public.applications OWNER TO "android-permissions";

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE categories_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO "android-permissions";

--
-- Name: categories; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE categories (
    id integer DEFAULT nextval('categories_id_seq'::regclass) NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.categories OWNER TO "android-permissions";

--
-- Name: content_ratings; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE content_ratings (
    id integer NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.content_ratings OWNER TO "android-permissions";

--
-- Name: content_ratings_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE content_ratings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.content_ratings_id_seq OWNER TO "android-permissions";

--
-- Name: content_ratings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE content_ratings_id_seq OWNED BY content_ratings.id;


--
-- Name: developers; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE developers (
    id integer NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.developers OWNER TO "android-permissions";

--
-- Name: developers_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE developers_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.developers_id_seq OWNER TO "android-permissions";

--
-- Name: developers_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE developers_id_seq OWNED BY developers.id;


--
-- Name: downloads; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE downloads (
    id integer NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.downloads OWNER TO "android-permissions";

--
-- Name: downloads_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE downloads_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.downloads_id_seq OWNER TO "android-permissions";

--
-- Name: downloads_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE downloads_id_seq OWNED BY downloads.id;


--
-- Name: icons; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE icons (
    id integer NOT NULL,
    sha1 text NOT NULL
);


ALTER TABLE public.icons OWNER TO "android-permissions";

--
-- Name: icons_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE icons_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.icons_id_seq OWNER TO "android-permissions";

--
-- Name: icons_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE icons_id_seq OWNED BY icons.id;


--
-- Name: permissions_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE permissions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.permissions_id_seq OWNER TO "android-permissions";

--
-- Name: permissions; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE permissions (
    id integer DEFAULT nextval('permissions_id_seq'::regclass) NOT NULL,
    name text NOT NULL,
    description text,
    regex text
);


ALTER TABLE public.permissions OWNER TO "android-permissions";

--
-- Name: pointintime_permissions; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE pointintime_permissions (
    pointintime_id integer NOT NULL,
    permission_id integer NOT NULL
);


ALTER TABLE public.pointintime_permissions OWNER TO "android-permissions";

--
-- Name: pit_permissions_permission_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE pit_permissions_permission_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pit_permissions_permission_id_seq OWNER TO "android-permissions";

--
-- Name: pit_permissions_permission_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE pit_permissions_permission_id_seq OWNED BY pointintime_permissions.permission_id;


--
-- Name: pointsintime; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE pointsintime (
    id integer NOT NULL,
    "timestamp" timestamp without time zone NOT NULL,
    application_id integer NOT NULL,
    developer_id integer,
    category_id integer,
    icon_id integer,
    rating_id integer,
    rating_count_id integer,
    download_id integer,
    size_id integer,
    price_id integer,
    update_date_id integer,
    version_id integer
);


ALTER TABLE public.pointsintime OWNER TO "android-permissions";

--
-- Name: pointsintim_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE pointsintim_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.pointsintim_id_seq OWNER TO "android-permissions";

--
-- Name: pointsintim_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE pointsintim_id_seq OWNED BY pointsintime.id;


--
-- Name: prices; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE prices (
    id integer NOT NULL,
    value real NOT NULL
);


ALTER TABLE public.prices OWNER TO "android-permissions";

--
-- Name: prices_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE prices_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.prices_id_seq OWNER TO "android-permissions";

--
-- Name: prices_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE prices_id_seq OWNED BY prices.id;


--
-- Name: rating_counts; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE rating_counts (
    id integer NOT NULL,
    value integer NOT NULL
);


ALTER TABLE public.rating_counts OWNER TO "android-permissions";

--
-- Name: rating_counts_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE rating_counts_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.rating_counts_id_seq OWNER TO "android-permissions";

--
-- Name: rating_counts_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE rating_counts_id_seq OWNED BY rating_counts.id;


--
-- Name: ratings; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE ratings (
    id integer NOT NULL,
    value real NOT NULL
);


ALTER TABLE public.ratings OWNER TO "android-permissions";

--
-- Name: ratings_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE ratings_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.ratings_id_seq OWNER TO "android-permissions";

--
-- Name: ratings_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE ratings_id_seq OWNED BY ratings.id;


--
-- Name: ratings_value_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE ratings_value_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.ratings_value_seq OWNER TO "android-permissions";

--
-- Name: ratings_value_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE ratings_value_seq OWNED BY ratings.value;


--
-- Name: sizes; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE sizes (
    id integer NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.sizes OWNER TO "android-permissions";

--
-- Name: sizes_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE sizes_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.sizes_id_seq OWNER TO "android-permissions";

--
-- Name: sizes_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE sizes_id_seq OWNED BY sizes.id;


--
-- Name: update_dates; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE update_dates (
    id integer NOT NULL,
    value date NOT NULL
);


ALTER TABLE public.update_dates OWNER TO "android-permissions";

--
-- Name: updates_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE updates_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.updates_id_seq OWNER TO "android-permissions";

--
-- Name: updates_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE updates_id_seq OWNED BY update_dates.id;


--
-- Name: versions; Type: TABLE; Schema: public; Owner: android-permissions; Tablespace: 
--

CREATE TABLE versions (
    id integer NOT NULL,
    value text NOT NULL
);


ALTER TABLE public.versions OWNER TO "android-permissions";

--
-- Name: versions_id_seq; Type: SEQUENCE; Schema: public; Owner: android-permissions
--

CREATE SEQUENCE versions_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MAXVALUE
    NO MINVALUE
    CACHE 1;


ALTER TABLE public.versions_id_seq OWNER TO "android-permissions";

--
-- Name: versions_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: android-permissions
--

ALTER SEQUENCE versions_id_seq OWNED BY versions.id;


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: android-permissions
--

ALTER TABLE ONLY content_ratings ALTER COLUMN id SET DEFAULT nextval('content_ratings_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: android-permissions
--

ALTER TABLE ONLY developers ALTER COLUMN id SET DEFAULT nextval('developers_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: android-permissions
--

ALTER TABLE ONLY downloads ALTER COLUMN id SET DEFAULT nextval('downloads_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: android-permissions
--

ALTER TABLE ONLY icons ALTER COLUMN id SET DEFAULT nextval('icons_id_seq'::regclass);


--
-- Name: permission_id; Type: DEFAULT; Schema: public; Owner: android-permissions
--

ALTER TABLE ONLY pointintime_permissions ALTER COLUMN permission_id SET DEFAULT nextval('pit_permissions_permission_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: android-permissions
--

ALTER TABLE ONLY pointsintime ALTER COLUMN id SET DEFAULT nextval('pointsintim_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: android-permissions
--

ALTER TABLE ONLY prices ALTER COLUMN id SET DEFAULT nextval('prices_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: android-permissions
--

ALTER TABLE ONLY rating_counts ALTER COLUMN id SET DEFAULT nextval('rating_counts_id_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: android-permissions
--

ALTER TABLE ONLY ratings ALTER COLUMN id SET DEFAULT nextval('ratings_id_seq'::regclass);


--
-- Name: value; Type: DEFAULT; Schema: public; Owner: android-permissions
--

ALTER TABLE ONLY ratings ALTER COLUMN value SET DEFAULT nextval('ratings_value_seq'::regclass);


--
-- Name: id; Type: DEFAULT; Schema: public; Owner: android-permissions
--
