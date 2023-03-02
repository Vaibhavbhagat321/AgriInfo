from typing import re

from flask import *
from AfriInfo_db import AgriInfo

app = Flask(__name__)
app.secret_key = 'abra ka dabra'
fobj=AgriInfo()

@app.route('/', methods=["POST", "GET"])
def index():
    crop_rec = fobj.get_crop_db()
    crop = []
    prod = []
    for item in crop_rec:
        crop.append(item[0])
        if str(fobj.get_crop_prod_db(item[0])[0]) == "None":
            prod.append(str(0))
        else:
            prod.append(str(fobj.get_crop_prod_db(item[0])[0]))
    if request.method == "GET":
        return render_template('login.html', crop = crop, prod = prod)
    if request.method == "POST":
        user = request.form["userid"]
        pwd = request.form["pass"]
        db_pwd = None
        if user == "admin@gmail.com" and pwd != "admin@123":
            msg = 'Userid or Password incorrect'
            return render_template('login.html', msg=msg, crop = crop, prod = prod)
        elif user == "admin@gmail.com" and pwd == "admin@123":
            rabi = fobj.get_crop_season_db('Rabi')
            kharif = fobj.get_crop_season_db('Kharif')
            zaid = fobj.get_crop_season_db('Zaid')
            dist = fobj.get_dist_db()
            d_prod = []
            for d in dist:
                d_prod.append(fobj.get_crop_district_db(d[0]))
            return render_template('home.html', rabi = rabi, kharif = kharif, zaid = zaid, dist = dist, dprod = d_prod)
        else:
            db_pwd = fobj.get_password_db(user)
            print(db_pwd)
        if db_pwd != None:
            if pwd == db_pwd[0]:
                session['userid'] = user
                rabi = fobj.get_crop_season_db('Rabi')
                kharif = fobj.get_crop_season_db('Kharif')
                zaid = fobj.get_crop_season_db('Zaid')
                msp = fobj.get_msp_db()
                return render_template('f-home.html', rabi = rabi, kharif = kharif, zaid = zaid, msp = msp)
            else:
                msg = 'Userid or Password incorrect'
                return render_template('login.html', msg = msg, crop = crop, prod = prod)
        else:
            msg = 'Userid or Password incorrect'
            return render_template('login.html', msg=msg, crop=crop, prod=prod)

@app.route('/msp&storage', methods=["GET", "POST"])
def msp_storage():
    if request.method == "GET":
        msp = fobj.get_msp_db()
        warehouse = fobj.get_warehouse_db()
        return render_template('msp&storage.html', rec = msp, wh = warehouse)
    # else:
    #     return render_template('msp&storage.html')

@app.route('/expert', methods=["POST", "GET"])
def expert():
    if request.method == "GET":
        rec = fobj.get_all_doubt_db()
        return render_template('expert.html', rec = rec)
    if request.method == "POST":
        sug = request.form['sug']
        doubt = request.form['doubt']
        fobj.update_doubt_db(sug, doubt)
        rec = fobj.get_all_doubt_db()
        return render_template('expert.html', rec = rec)

@app.route('/enrollfarmer', methods=['GET', 'POST'])
def enroll_farmer():
    if request.method == 'GET':
        return render_template('enrollfarmer.html')
    if request.method == 'POST':
        fname = request.form['fname']
        fcity = request.form['fcity']
        fdist = request.form['fdist']
        fuser = request.form['fuser']
        fpwd = request.form['fpass']
        fmail = request.form['fmail']
        fcont = request.form['fcont']
        rows = fobj.enroll_farmer_db(fname, fcity, fdist, fuser, fpwd, fmail, fcont)
        if rows != 0:
            msg = 'Farmer Enrolled.'
        return render_template('enrollfarmer.html', msg = msg)


@app.route('/crop-info', methods=["POST", "GET"])
def crop_info():
    districts = fobj.get_dist_db()
    years = fobj.get_year_db()
    if request.method == "GET":
        rec = fobj.get_all_crop_db()
        return render_template('crop-info.html', rec = rec, d = districts, y = years)
    if request.method == "POST":
        dist = request.form['district']
        year = request.form['year']
        rec = fobj.get_scrop_db(dist, year)
        return render_template('crop-info.html', rec = rec, d = districts, y = years)

@app.route('/msp&warehouseupate', methods = ["GET", "POST"])
def msp_warehouse_update():
    operate = request.form["operate"]
    if operate == 'msp':
        crop = request.form['hidden']
        msp = request.form['newmsp']
        fobj.update_msp_db(crop, msp)
        msp = fobj.get_msp_db()
        warehouse = fobj.get_warehouse_db()
        return render_template('msp&storage.html', rec=msp, wh=warehouse)
    elif operate == 'warehouse':
        nm = request.form['hidden']
        newqty = request.form['newqty']
        fobj.update_warehouse_db(nm, newqty)
        msp = fobj.get_msp_db()
        warehouse = fobj.get_warehouse_db()
        return render_template('msp&storage.html', rec=msp, wh=warehouse)

@app.route('/addwarehouse', methods=["GET", "POST"])
def add_warehouse():
    nm = request.form['crop']
    qty = request.form['qty']
    aqty = request.form['aqty']
    fobj.add_warehouse_db(nm, qty, aqty)
    msp = fobj.get_msp_db()
    warehouse = fobj.get_warehouse_db()
    return render_template('msp&storage.html', rec=msp, wh=warehouse)

@app.route('/faq', methods=["POST", "GET"])
def faq():
    if request.method == "GET":
        rec = fobj.get_faq_db()
        return render_template('faq.html', rec = rec)
    if request.method == "POST":
        que = request.form['que']
        ans = request.form['ans']
        rows = fobj.add_faq_db(que, ans)
        if rows != 0:
            msg = 'FAQ Posted.'
        rec = fobj.get_faq_db()
        return render_template('faq.html', msg = msg, rec = rec)

@app.route('/fhome')
def f_home():
    rabi = fobj.get_crop_season_db('Rabi')
    kharif = fobj.get_crop_season_db('Kharif')
    zaid = fobj.get_crop_season_db('Zaid')
    msp = fobj.get_msp_db()
    return render_template('f-home.html', rabi=rabi, kharif=kharif, zaid=zaid, msp=msp)



@app.route('/fask-expert', methods=["GET", "POST"])
def f_ask_expert():
    user = session['userid']
    if request.method == "GET":
        rec = fobj.get_doubt_db(user)
        return render_template('f-ask-expert.html', rec = rec)
    if request.method == "POST":
        doubt = request.form["txtarea"]
        row = fobj.add_doubt_db(doubt, user)
        rec = fobj.get_doubt_db(user)
        if row != 0:
            msg = 'Doubt posted.'
        return render_template('f-ask-expert.html', msg = msg, rec = rec)

@app.route('/fcrop-info', methods=["POST", "GET"])
def f_crop_info():
    lcrop = fobj.get_crop_db()
    user = session['userid']
    rec = fobj.get_user_db(user)
    if request.method == "GET":
        return render_template('f-crop-info.html', rec = rec, crop = lcrop)
    if request.method == "POST":
        crop = request.form['fcrop']
        season = request.form['fseason']
        qty = request.form['fqty']
        row = fobj.add_crop_db(crop, season, qty, rec[2], rec[0], 2021)
        if row != 0:
            msg = 'Crop added.'
        return render_template('f-crop-info.html', rec = rec, msg = msg, crop = lcrop)

@app.route('/ffaq')
def f_faq():
    rec = fobj.get_faq_db()
    print(rec)
    return render_template('f-faq.html', rec=rec)

@app.route('/logout')
def logout():
    session.pop('userid', None)
    crop_rec = fobj.get_crop_db()
    crop = []
    prod = []
    for item in crop_rec:
        crop.append(item[0])
        if str(fobj.get_crop_prod_db(item[0])[0]) == "None":
            prod.append(str(0))
        else:
            prod.append(str(fobj.get_crop_prod_db(item[0])[0]))
    return render_template('login.html', crop = crop, prod = prod)

@app.route('/home')
def home():
    rabi = fobj.get_crop_season_db('Rabi')
    kharif = fobj.get_crop_season_db('Kharif')
    zaid = fobj.get_crop_season_db('Zaid')
    dist = fobj.get_dist_db()
    d_prod = []
    for d in dist:
        d_prod.append(fobj.get_crop_district_db(d[0]))
    return render_template('home.html', rabi=rabi, kharif=kharif, zaid=zaid, dist=dist, dprod=d_prod)

@app.route('/pesticide')
def pesticide():
    return render_template('pesticides.html')

if __name__ == '__main__':
    app.run()
