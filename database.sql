CREATE TABLE IF NOT EXISTS urls (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL UNIQUE,
    created_at DATE DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE IF NOT EXISTS url_checks(
    id SERIAL PRIMARY KEY,
    url_id SERIAL REFERENCES urls (id),
    status_code INT,
    h1 VARCHAR(255),
    title TEXT,
    description VARCHAR(255),
    created_at DATE DEFAULT CURRENT_TIMESTAMP
);
