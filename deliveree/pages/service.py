import psycopg2 as pg 

class DBService:
    def __init__(self):
        try:
            self.con = pg.connect("dbname = 'deliveree' user = 'postgres' host = 'localhost' password = 'GPA40' ")
        except (Exception, pg.DatabaseError) as error:
            print(error)
        # self.selectAll = query = "select firstname, lastname, address, date, time, contact, id from deliveree_user WHERE status = false ORDER BY id"
        self.selectAll = query = "select firstname, lastname, address, date, time, contact, id from deliveree_user WHERE status = false ORDER BY date ASC, time ASC, distance DESC"

    def fetchAll(self):
        cur = self.con.cursor()
        try:
            cur.execute(self.selectAll)
        except (Exception, pg.DatabaseError) as error:
            print(error)
        rows = cur.fetchall()
        return rows

    def updateById(self, id):
        cur = self.con.cursor()
        try:
            cur.execute("UPDATE deliveree_user SET status = TRUE WHERE id =" + str(id))
            self.con.commit()
        except (Exception, pg.DatabaseError) as error:
            print(error)
        return True

    def deleteById(self, id):
        cur = self.con.cursor()
        try:
            cur.execute("DELETE from deliveree_user WHERE id=" + str(id))
            self.con.commit()
        except (Exception, pg.DatabaseError) as error:
            print(error)
        return True 


# db = DBService()
# rows = db.fetchAll()
# for row in rows:
#     print(row)





