CREATE TABLE IF NOT EXISTS raw_articles (
    id UUID PRIMARY KEY,
    source TEXT NOT NULL,
    title TEXT NOT NULL,
    content TEXT NOT NULL,
    url TEXT UNIQUE NOT NULL,
    published_at TIMESTAMP,
    checksum TEXT NOT NULL,
    ingested_at TIMESTAMP NOT NULL
);

CREATE TABLE IF NOT EXISTS positions (
    id UUID PRIMARY KEY,
    ticker TEXT NOT NULL,
    entry_price NUMERIC NOT NULL,
    quantity NUMERIC NOT NULL,
    thesis TEXT NOT NULL,
    confidence NUMERIC NOT NULL,
    sector TEXT,
    opened_at TIMESTAMP NOT NULL
);
