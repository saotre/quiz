CREATE SCHEMA IF NOT EXISTS content;

CREATE TABLE IF NOT EXISTS content.category (
    id int PRIMARY KEY,
    title TEXT NOT NULL
);


CREATE TABLE IF NOT EXISTS content.questions (
    id int PRIMARY KEY,
    question TEXT NOT NULL,
    answer TEXT NOT NULL,
    created_at timestamp with time zone,
    category_id int NOT NULL,
    value int,
    created_rec timestamp with time zone,
    FOREIGN KEY (category_id) REFERENCES content.category (id) ON DELETE CASCADE
);



CREATE INDEX ON content.questions (created_at, value);
