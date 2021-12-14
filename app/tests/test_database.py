import unittest
import sys
sys.path.append('../')

from database import DataMgmtClass
import conf

class TestDatabase(unittest.TestCase):

    def test_select(self):
        db = DataMgmtClass()
        if db._isConnected():
            n = db._select("select * from t_numbers_dummy where number > %(num)s", {'num': 1})
            if (n):
                self.assertTrue(True)
                print(n)
            else:
                self.assertTrue(False)
        else:
            self.assertTrue(False)
            
    def test_insert(self):
        db = DataMgmtClass()
        if db._isConnected():
            n = {'num': 5, 'ts': 9}
            ret = db._execute("insert into t_numbers_dummy (number, timestamp) values ( %(num)s, %(ts)s )", n, True)
            n = db._select("select * from t_numbers_dummy")
            print(n)
            self.assertEqual(ret, conf.SUCCESS)
        else:
            self.assertTrue(False)

    def test_bulk_insert(self):
        db = DataMgmtClass()
        n = ({'num': 57, 'ts': 97}, {'num': 58, 'ts': 98}, {'num': 59, 'ts': 99})
        if db._isConnected():
            ret = db._bulkInsert("insert into t_numbers_dummy (number, timestamp) values ( %(num)s, %(ts)s )", n, True)
            n = db._select("select * from t_numbers_dummy")
            print(n)
            self.assertEqual(ret, conf.SUCCESS)
        else:
            self.assertTrue(False)

    def test_insert_plainnodes_table(self):
        db = DataMgmtClass()
        if db._isConnected():
            n = {'gid': 1, 'x': -110, 'y': 99}
            ret = db._execute("insert into t_plain_nodes (gid, geog) values (%(gid)s, ST_GeomFromText('POINT(%(x)s %(y)s)', 4326))", n, True)
            n = db._select("select gid, ST_AsText(geog) from t_plain_nodes")
            print(n)
            self.assertEqual(ret, conf.SUCCESS)
        else:
            self.assertTrue(False)

    def test_insert_plainlines_table(self):
        db = DataMgmtClass()
        if db._isConnected():
            n = {'gidn1': 1, 'gidn2': 2, 'vals': "LINESTRING(0 0,70 0,70 -99)"}
            ret = db._execute("insert into t_plain_lines (gidn1, gidn2, geog) values (%(gidn1)s, %(gidn2)s, ST_GeomFromText(%(vals)s, 4326))", n, True)
            n = db._select("select gidn1, gidn2, ST_AsText(geog) from t_plain_lines")
            print(n)
            self.assertEqual(ret, conf.SUCCESS)
        else:
            self.assertTrue(False)

    def test_cleanUp(self):
        db = DataMgmtClass()
        if db._isConnected():
            db._cleanUp()
            self.assertTrue(True)
        else:
            self.assertTrue(False)

    
if __name__ == '__main__':
    unittest.main()