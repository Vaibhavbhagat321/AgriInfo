import mysql.connector as sql

class AgriInfo():
    def __init__(self):
        self.con = sql.connect(user='root', password='admin', database='agriinfo')

    def enroll_farmer_db(self, nm, ct, dst, user, pwd, mail, cont):
        cur = self.con.cursor()
        cmd = "select max(f_id) from farmers"
        cur.execute(cmd)
        rec = cur.fetchone()
        id = rec[0] + 1
        cur = self.con.cursor()
        cmd = "insert into farmers values (%s, %s, %s, %s, %s, %s, %s, %s)"
        cur.execute(cmd, [nm, ct, dst, user, pwd, id, mail, cont])
        self.con.commit()
        cur.close()
        return cur.rowcount

    def get_password_db(self, user):
        cur = self.con.cursor()
        cmd = 'select password from farmers where userid=%s'
        cur.execute(cmd, [user])
        rec = cur.fetchone()
        cur.close()
        return rec

    def get_msp_db(self):
        cur = self.con.cursor()
        cmd = "select * from msp"
        cur.execute(cmd)
        rec = cur.fetchall()
        cur.close()
        return rec

    def get_warehouse_db(self):
        cur = self.con.cursor()
        cmd = "select * from warehouse"
        cur.execute(cmd)
        rec = cur.fetchall()
        cur.close()
        return rec

    def update_msp_db(self, crop, msp):
        cur = self.con.cursor()
        cmd = "update msp set crop_msp = %s where crop = %s"
        cur.execute(cmd, [msp, crop])
        self.con.commit()
        cur.close()

    def update_warehouse_db(self, nm, qty):
        cur = self.con.cursor()
        cmd = "update warehouse set available_storage = %s where warehouse = %s"
        cur.execute(cmd, [qty, nm])
        self.con.commit()
        cur.close()

    def add_warehouse_db(self, nm, ttl, avl):
        cur = self.con.cursor()
        cmd = "insert into warehouse values (%s, %s, %s)"
        cur.execute(cmd, [nm, ttl, avl])
        self.con.commit()
        cur.close()

    def add_faq_db(self, que, ans):
        # cur = self.con.cursor()
        # cmd = "select max(faq_id) from faq"
        # cur.execute(cmd)
        # rec = cur.fetchone()
        # id = rec[0] + 1
        cur = self.con.cursor()
        cmd = "insert into faq values (%s, %s)"
        cur.execute(cmd, [que, ans])
        self.con.commit()    
        cur.close()
        return cur.rowcount

    def get_faq_db(self):
        cur = self.con.cursor()
        cmd = "select * from faq"
        cur.execute(cmd)
        rec = cur.fetchall()
        cur.close()
        return rec

    def add_doubt_db(self, dbt, user):
        cur = self.con.cursor()
        cmd = "insert into doubt values (%s,%s,%s)"
        cur.execute(cmd, [dbt, None, user])
        self.con.commit()
        cur.close()
        return cur.rowcount

    def get_doubt_db(self, user):
        cur = self.con.cursor()
        cmd = "select * from doubt where user=%s"
        cur.execute(cmd, [user])
        rec = cur.fetchall()
        cur.close()
        return rec

    def get_all_doubt_db(self):
        cur = self.con.cursor()
        cmd = "select * from doubt"
        cur.execute(cmd)
        rec = cur.fetchall()
        cur.close()
        return rec

    def update_doubt_db(self, sug, doubt):
        cur = self.con.cursor()
        cmd = "update doubt set d_advice = %s where doubt=%s"
        cur.execute(cmd, [sug, doubt])
        self.con.commit()
        cur.close()

    def get_user_db(self, user):
        cur = self.con.cursor()
        cmd = "select * from farmers where userid=%s"
        cur.execute(cmd, [user])
        rec = cur.fetchone()
        cur.close()
        return rec

    def add_crop_db(self, crop, season, qty, dist, far, year):
        cur = self.con.cursor()
        cmd = "insert into crop values (%s, %s, %s, %s, %s, %s)"
        cur.execute(cmd, [crop, season, qty, dist, far,year])
        self.con.commit()
        cur.close()
        return cur.rowcount

    def get_all_crop_db(self):
        cur = self.con.cursor()
        cmd = "select * from crop"
        cur.execute(cmd)
        rec = cur.fetchall()
        cur.close()
        return rec

    def get_scrop_db(self, dist, year):
        cur = self.con.cursor()
        cmd = "select * from crop where district=%s and year=%s"
        cur.execute(cmd, [dist, year])
        rec = cur.fetchall()
        cur.close()
        return rec

    def get_dist_db(self):
        cur = self.con.cursor()
        cmd = "select distinct district from crop"
        cur.execute(cmd)
        rec = cur.fetchall()
        cur.close()
        return rec

    def get_year_db(self):
        cur = self.con.cursor()
        cmd = "select distinct year from crop"
        cur.execute(cmd)
        rec = cur.fetchall()
        cur.close()
        return rec

    def get_crop_db(self):
        cur = self.con.cursor()
        cmd = "select crop from msp"
        cur.execute(cmd)
        rec = cur.fetchall()
        cur.close()
        return rec

    def get_crop_prod_db(self, crop):
        cur = self.con.cursor()
        cmd = "select sum(crop_qty) from crop where crop = %s"
        cur.execute(cmd, [crop])
        prod = cur.fetchone()
        cur.close()
        return prod

    def get_crop_season_db(self, season):
        cur = self.con.cursor()
        cmd = "select sum(crop_qty) from crop where crop_season = %s"
        cur.execute(cmd, [season])
        prod = cur.fetchone()
        cur.close()
        return prod[0]


    def get_crop_district_db(self, dist):
        cur = self.con.cursor()
        cmd = "select sum(crop_qty) from crop where district = %s"
        cur.execute(cmd, [dist])
        prod = cur.fetchone()
        cur.close()
        return prod[0]