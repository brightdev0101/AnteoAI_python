from webapp import app

from flask import render_template, redirect, url_for, send_file, request, abort, send_file
from flask_login import current_user, login_user, logout_user, login_required


@app.route('/sanremo2022')
def sanremo2022():
    user_logged = "true" if current_user.is_authenticated else "false"
    return render_template('analysis/sanremo2022.html', logged = user_logged)
    
@app.route('/ducati')
def ducati():
    user_logged = "true" if current_user.is_authenticated else "false"
    return render_template('analysis/ducati_motogp_2022.html', logged = user_logged)
    
@app.route('/prema')
def prema():
    user_logged = "true" if current_user.is_authenticated else "false"
    return render_template('analysis/prema.html', logged = user_logged)

@app.route('/ferrari')
def ferrari():
    user_logged = "true" if current_user.is_authenticated else "false"
    return render_template('analysis/ferrari.html', logged = user_logged)

@app.route('/comau')
def comau():
    user_logged = "true" if current_user.is_authenticated else "false"
    return render_template('analysis/comau.html', logged = user_logged)

@app.route('/ukraine')
def ukraine():
    user_logged = "true" if current_user.is_authenticated else "false"
    return render_template('analysis/ua_ru_conflict.html', logged = user_logged)

