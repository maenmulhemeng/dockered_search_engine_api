CREATE TABLE IF NOT EXISTS public.user (
  id SERIAL,
  username TEXT UNIQUE NOT NULL,
  password TEXT NOT NULL
) 
TABLESPACE pg_default
;




ALTER TABLE IF EXISTS public.user
    OWNER to search_engine_user;


-- Table: public.docs

-- DROP TABLE IF EXISTS public.docs;

CREATE TABLE IF NOT EXISTS public.docs
(
    id SERIAL,
    doc_url text,
    contents jsonb
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.docs
    OWNER to search_engine_user;
-- Index: contents_inverted_index

-- DROP INDEX IF EXISTS public.contents_inverted_index;

CREATE INDEX IF NOT EXISTS contents_inverted_index
    ON public.docs USING gin
    (contents jsonb_path_ops)
    WITH (fastupdate=True)
    TABLESPACE pg_default;
-- Index: doc_url_btree-index

-- DROP INDEX IF EXISTS public."doc_url_btree-index";

CREATE INDEX IF NOT EXISTS doc_url_btree_index
    ON public.docs USING btree
    (doc_url COLLATE pg_catalog."default" varchar_ops ASC NULLS LAST)
    WITH (deduplicate_items=True)
    TABLESPACE pg_default;
