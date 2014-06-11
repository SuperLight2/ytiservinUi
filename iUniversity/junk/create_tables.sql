CREATE TABLE u_vertices (
    `uid` bigint(20) NOT NULL DEFAULT 0,
    `utype`int(11) NOT NULL DEFAULT 0,
    `data` text NOT NULL,
    PRIMARY KEY (`uid`),
    KEY `uid` (`uid`)
);

CREATE TABLE u_edges (
    `uid1` bigint(20) NOT NULL DEFAULT 0,
    `uid2` bigint(20) NOT NULL DEFAULT 0,
    `utype` int(11) NOT NULL DEFAULT 0,
    `info` varchar(255) NOT NULL DEFAULT '',
    `timestamp` bigint(20) NOT NULL DEFAULT 0,
    PRIMARY KEY (`uid1`, `uid2`, `utype`),
    KEY `uid1` (`uid1`),
    KEY `utype` (`utype`),
    FOREIGN KEY (`uid1`) REFERENCES u_vertices(`uid`),
    FOREIGN KEY (`uid2`) REFERENCES u_vertices(`uid`)
);