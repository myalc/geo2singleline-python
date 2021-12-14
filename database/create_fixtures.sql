CREATE TABLE IF NOT EXISTS t_geo_nodes (
    gid BIGINT,
    geog GEOMETRY(Point, 4326),
    desctiption varchar(1000)
);

CREATE TABLE IF NOT EXISTS t_conns (
    gidn1 BIGINT,
    gidn2 BIGINT
);

CREATE TABLE IF NOT EXISTS t_plain_nodes (
    gid BIGINT,
    geog GEOMETRY
);

CREATE TABLE IF NOT EXISTS t_plain_lines (
    gidn1 BIGINT,
    gidn2 BIGINT,
    geog GEOMETRY
);

--------- test
CREATE TABLE IF NOT EXISTS t_numbers_dummy (
    number BIGINT,
    timestamp BIGINT
);

