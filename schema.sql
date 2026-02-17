create table url_mapper
(
    short_url varchar(255) primary key,
    long_url varchar(255) not null ,
    created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);