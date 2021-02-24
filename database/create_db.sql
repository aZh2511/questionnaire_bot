CREATE TABLE IF NOT EXISTS users
(
    chat_id   bigint            not null
        constraint users_pk
            primary key,
    username  text,
    full_name text,
    adding_date   timestamp,
    id        serial            not null
);

alter table users
    owner to postgres;

create unique index users_id_uindex
    on users (id);

CREATE TABLE IF NOT EXISTS questions
(
    question      text               not null,
    q_order       integer            not null,
    question_id   integer            GENERATED ALWAYS AS IDENTITY,
    PRIMARY KEY(question_id)
);

CREATE TABLE IF NOT EXISTS options
(
   option_id        SERIAL      PRIMARY KEY,
   option_text      text        not null,
   question_id      integer,
   FOREIGN KEY (question_id) REFERENCES questions(question_id) ON DELETE CASCADE
);