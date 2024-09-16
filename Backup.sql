PGDMP                         {            kartik    15.1    15.1                0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false                       0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false                       0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false                       1262    16398    kartik    DATABASE     h   CREATE DATABASE kartik WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE kartik;
                postgres    false            �            1259    16410    ques    TABLE     	  CREATE TABLE public.ques (
    username character varying(50),
    q1 character varying(100) NOT NULL,
    q2 character varying(100) NOT NULL,
    q3 character varying(100) NOT NULL,
    q4 character varying(100) NOT NULL,
    q5 character varying(100) NOT NULL
);
    DROP TABLE public.ques;
       public         heap    postgres    false            �            1259    16400    users    TABLE       CREATE TABLE public.users (
    username character varying(50) NOT NULL,
    password character varying(50) NOT NULL,
    firstname character varying(50) NOT NULL,
    lastname character varying(50) NOT NULL,
    emailid character varying(50) NOT NULL,
    phoneno integer NOT NULL
);
    DROP TABLE public.users;
       public         heap    postgres    false            �            1259    16399    users_phoneno_seq    SEQUENCE     �   CREATE SEQUENCE public.users_phoneno_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 (   DROP SEQUENCE public.users_phoneno_seq;
       public          postgres    false    215                       0    0    users_phoneno_seq    SEQUENCE OWNED BY     G   ALTER SEQUENCE public.users_phoneno_seq OWNED BY public.users.phoneno;
          public          postgres    false    214            s           2604    16403    users phoneno    DEFAULT     n   ALTER TABLE ONLY public.users ALTER COLUMN phoneno SET DEFAULT nextval('public.users_phoneno_seq'::regclass);
 <   ALTER TABLE public.users ALTER COLUMN phoneno DROP DEFAULT;
       public          postgres    false    215    214    215                      0    16410    ques 
   TABLE DATA           <   COPY public.ques (username, q1, q2, q3, q4, q5) FROM stdin;
    public          postgres    false    216   j       
          0    16400    users 
   TABLE DATA           Z   COPY public.users (username, password, firstname, lastname, emailid, phoneno) FROM stdin;
    public          postgres    false    215   �                  0    0    users_phoneno_seq    SEQUENCE SET     @   SELECT pg_catalog.setval('public.users_phoneno_seq', 1, false);
          public          postgres    false    214            u           2606    16407    users users_emailid_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_emailid_key UNIQUE (emailid);
 A   ALTER TABLE ONLY public.users DROP CONSTRAINT users_emailid_key;
       public            postgres    false    215            w           2606    16409    users users_phoneno_key 
   CONSTRAINT     U   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_phoneno_key UNIQUE (phoneno);
 A   ALTER TABLE ONLY public.users DROP CONSTRAINT users_phoneno_key;
       public            postgres    false    215            y           2606    16405    users users_pkey 
   CONSTRAINT     T   ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (username);
 :   ALTER TABLE ONLY public.users DROP CONSTRAINT users_pkey;
       public            postgres    false    215            z           2606    16415    ques ques_username_fkey    FK CONSTRAINT     }   ALTER TABLE ONLY public.ques
    ADD CONSTRAINT ques_username_fkey FOREIGN KEY (username) REFERENCES public.users(username);
 A   ALTER TABLE ONLY public.ques DROP CONSTRAINT ques_username_fkey;
       public          postgres    false    216    3449    215                  x������ � �      
      x������ � �     