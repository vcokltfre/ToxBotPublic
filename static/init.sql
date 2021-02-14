CREATE TABLE IF NOT EXISTS Guilds (
    id          BIGINT NOT NULL,
    config      TEXT NOT NULL,
    banned      BOOLEAN NOT NULL DEFAULT FALSE,
    daily       BIGINT NOT NULL DEFAULT 14400,
    today       BIGINT NOT NULL DEFAULT 0,
    lastreset   BIGINT NOT NULL DEFAULT 0,
    PRIMARY KEY (id)
);

CREATE TABLE IF NOT EXISTS Infractions (
    id          VARCHAR(12) NOT NULL,
    userid      BIGINT NOT NULL,
    guildid     BIGINT NOT NULL,
    content     TEXT NOT NULL,
    scores      TEXT NOT NULL,
    itype       VARCHAR(16) NOT NULL,
    PRIMARY KEY (id),
    FOREIGN KEY (guildid) REFERENCES Guilds (id) ON DELETE CASCADE
);
