
insert into t_numbers_dummy values (1, 0);
insert into t_numbers_dummy values (2, 0);
insert into t_numbers_dummy values (3, 0);


insert into t_geo_nodes(gid, geog, desctiption) values(0, ST_SetSRID(ST_MakePoint(41.02558642576433, 28.97427949555822), 4326), 'Galata tower');
insert into t_geo_nodes(gid, geog, desctiption) values(1, ST_SetSRID(ST_MakePoint(41.03723287814689, 28.9851062287593), 4326), 'Taksim square');
insert into t_geo_nodes(gid, geog, desctiption) values(2, ST_SetSRID(ST_MakePoint(41.03959882754591, 29.000387580789805), 4326), 'Dolmabahce palace');


/*
insert into t_conns(gidn1, gidn2) values(0, 1);
insert into t_conns(gidn1, gidn2) values(0, 2);
insert into t_conns(gidn1, gidn2) values(1, 2);
insert into t_conns(gidn1, gidn2) values(2, 0);
insert into t_conns(gidn1, gidn2) values(1, 3);
insert into t_conns(gidn1, gidn2) values(3, 3);
*/

insert into t_conns(gidn1, gidn2) values(0, 1);
insert into t_conns(gidn1, gidn2) values(0, 2);
insert into t_conns(gidn1, gidn2) values(0, 3);
insert into t_conns(gidn1, gidn2) values(1, 8);
insert into t_conns(gidn1, gidn2) values(1, 9);
insert into t_conns(gidn1, gidn2) values(2, 7);
insert into t_conns(gidn1, gidn2) values(2, 17);
insert into t_conns(gidn1, gidn2) values(2, 18);
insert into t_conns(gidn1, gidn2) values(2, 19);
insert into t_conns(gidn1, gidn2) values(3, 4);
insert into t_conns(gidn1, gidn2) values(3, 5);
insert into t_conns(gidn1, gidn2) values(3, 6);
insert into t_conns(gidn1, gidn2) values(10, 11);
insert into t_conns(gidn1, gidn2) values(11, 12);
insert into t_conns(gidn1, gidn2) values(12, 12);
insert into t_conns(gidn1, gidn2) values(8, 21);
insert into t_conns(gidn1, gidn2) values(8, 22);
insert into t_conns(gidn1, gidn2) values(21, 23);
insert into t_conns(gidn1, gidn2) values(22, 24);
