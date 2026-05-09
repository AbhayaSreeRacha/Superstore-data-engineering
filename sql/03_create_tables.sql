CREATE TABLE IF NOT EXISTS public.customers
(
    customer_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    customer_name text COLLATE pg_catalog."default",
    segment text COLLATE pg_catalog."default",
    country text COLLATE pg_catalog."default",
    region text COLLATE pg_catalog."default",
    CONSTRAINT customers_pkey PRIMARY KEY (customer_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.customers
    OWNER to postgres;
CREATE TABLE IF NOT EXISTS public.order_items
(
    row_id integer NOT NULL,
    order_id character varying(50) COLLATE pg_catalog."default",
    product_id character varying(50) COLLATE pg_catalog."default",
    sales numeric,
    quantity integer,
    discount numeric,
    profit numeric,
    CONSTRAINT order_items_pkey PRIMARY KEY (row_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.order_items
    OWNER to postgres;
CREATE TABLE IF NOT EXISTS public.orders
(
    order_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    order_date date,
    ship_date date,
    ship_mode text COLLATE pg_catalog."default",
    customer_id character varying(50) COLLATE pg_catalog."default",
    region text COLLATE pg_catalog."default",
    postal_code character varying(20) COLLATE pg_catalog."default",
    CONSTRAINT orders_pkey PRIMARY KEY (order_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.orders
    OWNER to postgres;
CREATE TABLE IF NOT EXISTS public.products
(
    product_id character varying(50) COLLATE pg_catalog."default" NOT NULL,
    product_name text COLLATE pg_catalog."default",
    category text COLLATE pg_catalog."default",
    sub_category text COLLATE pg_catalog."default",
    CONSTRAINT products_pkey PRIMARY KEY (product_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.products
    OWNER to postgres;