__author__ = 'gumerovif'

import MySQLdb


class DBRunner(object):
    # TODO: add exception handler
    @classmethod
    def run(cls, db_query):
        print db_query
        db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="NEWPASSWORD", db="main",use_unicode=True)
        try:
            cur = db.cursor(MySQLdb.cursors.DictCursor)
            cur.execute(db_query)
            db.commit()
            results = []
            for i in xrange(cur.rowcount):
                results.append(cur.fetchone())
            return results
        except MySQLdb.Error, e:
            if db:
                db.rollback()
            print "Error %d: %s" % (e.args[0],e.args[1])
        finally:
            if db:
                db.close()


if __name__ == '__main__':
    db = MySQLdb.connect(host="127.0.0.1", user="root", passwd="NEWPASSWORD", db="main",use_unicode=True)
    cur = db.cursor()
    results = []
    try:
        cur.execute("INSERT INTO u_vertexes VALUE (661577530201611744, 1, '{}')")
        db.commit()
        for i in xrange(cur.rowcount):
            results.append(cur.fetchone())
    except MySQLdb.Error, e:
        if db:
            db.rollback()
        print "Error %d: %s" % (e.args[0],e.args[1])
    print results
    db.close()