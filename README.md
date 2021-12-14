# geo2singleline-python


```bash
cd geo2singleline-python
docker images
docker-compose build
docker-compose up -d db
docker-compose up app

docker logs <id>
```

```bash
docker build -t myalc/geo2singleline/db .
docker run -d myalc/geo2singleline/db
docker run -d -p 5432:5432 myalc/geo2singleline/db
docker exec -it <id> bash

cd /docker-entrypoint-initdb.d/
psql postgres://myuser:mypass@localhost:5432/mydb
```

```sql
SELECT * FROM t_numbers_dummy;
SELECT * FROM t_geo_nodes;
SELECT * FROM t_conns;
SELECT * FROM t_plain_nodes;
SELECT * FROM t_plain_lines;
```

```sql
SELECT gid, ST_AsText(geog), desctiption FROM t_geo_nodes;
SELECT gid, ST_AsText(geog) FROM t_plain_nodes;
SELECT gidn1, gidn2, ST_AsText(geog) FROM t_plain_lines;

SELECT ST_AsGeoJSON(geog) from t_geo_nodes;
SELECT ST_AsGeoJSON(geog) from t_plain_nodes;
SELECT ST_AsGeoJSON(geog) from t_plain_lines;

SELECT ST_AsSVG(geog) from t_plain_lines;
SELECT ST_AsText(ST_ConvexHull(ST_Collect(geog))) FROM t_plain_lines;
```
