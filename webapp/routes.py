import json
from datetime import datetime

from webapp import app
from flask import render_template, redirect, url_for, send_file, request, abort, send_file
from flask_login import current_user, login_user, logout_user, login_required
from webapp.User import User
from webapp.UsersManager import UsersManager
from webapp.API.Response import Response
from webapp.vars import ERROR_MISSING_PARAMS, ERROR_API, ERROR_GENERAL, ACCOUNT_TYPES, IMGS_DIR, SITEMAP
from webapp.API.userUpdate import userUpdate
from webapp.API.getTrend import getTrend
from webapp.API.getCustomTrend import getCustomTrend
from webapp.API.setCustomTrend import setCustomTrend
from webapp.API.addCustomTrend import addCustomTrend 
from webapp.API.delCustomTrend import delCustomTrend
from webapp.API.getUser import getUser
from webapp.API.signIn import signIn
from webapp.API.signUp import signUp
from webapp.API.demoRequest import demoRequest
from webapp.MailManager import MailManager


##################
#  WEB SECTIONS  #
##################

@app.route('/')
@app.route('/index', methods=['GET'])
def home():
    """ Anteo AI Home Page
    """
    user_logged = "true" if current_user.is_authenticated else "false"
    return render_template('home.html', logged = user_logged)

@app.route('/trends', methods=['GET'])
def trends():
    """ Anteo AI Trends Page
    """
    trend = request.args.get('trend', default = "", type = str)
    accepted_trends = ["finance", "sport"]
    
    user_logged = "true" if current_user.is_authenticated else "false"

    selected_trend = ""
    if trend in accepted_trends:
        selected_trend = trend

    return render_template('trends.html', logged = user_logged, trend = selected_trend)

@app.route('/custom', methods=['GET'])
@login_required
def custom():
    """ Custom Analysis page 
    """

    # Get custom trend id
    selected_trend = None
    request_trend = request.args.get('ctid', default = None, type = int)

    if request_trend == -1:
        selected_trend = -1
    elif request_trend in current_user.custom_trends.keys() and request_trend != None:
        selected_trend = request_trend
    else:
        if len(current_user.custom_trends.keys()) < 1:
            selected_trend = -1
        else:
            selected_trend = list(current_user.custom_trends.keys())[0]

    # Evaluate available Custom Trends for User Plan
    if current_user.plan == 3:
        available_trends = 3
    elif current_user.plan == 2:
        available_trends = 2
    elif current_user.plan == 1:
        available_trends = 1
    else:
        available_trends = 0
    

    if current_user.is_authenticated:
        return render_template('custom.html', selected_trend = selected_trend, custom_trends = json.dumps(current_user.custom_trends), available_trends = available_trends)
    else:
        return redirect(url_for('home'))
# /////////////////////////
@app.route('/roles', methods=['GET'])
def roles():
    return render_template('roles.html')

@app.route('/stories', methods=['GET'])
def stories():
    return render_template('stories.html')

@app.route('/resources', methods=['GET'])
def resources():
    return render_template('resources.html')

@app.route('/freeTools', methods=['GET'])
def freeTools():
    return render_template('freeTools.html')

@app.route('/competitive', methods=['GET'])
def competitive():
    return render_template('competitive.html')

@app.route('/contentStrategy', methods=['GET'])
def contentStrategy():
    return render_template('contentStrategy.html')

@app.route('/sentimentAnalysis', methods=['GET'])
def sentimentAnalysis():
    return render_template('sentimentAnalysis.html')

@app.route('/insightMarketing', methods=['GET'])
def insightMarketing():
    return render_template('insightMarketing.html')

@app.route('/performanceMonitoring', methods=['GET'])
def performanceMonitoring():
    return render_template('performanceMonitoring.html')

@app.route('/socialGamification', methods=['GET'])
def socialGamification():
    return render_template('socialGamification.html')
# /////////////////////////////
@app.route('/howitworks')
def hiw():
    """ How It Works page
    """
    user_logged = "true" if current_user.is_authenticated else "false"
    return render_template('howitworks.html', logged = user_logged)

@app.route('/form')
def form():
    """ Form Login/Register page
    """
    if current_user.is_authenticated:
        return redirect(url_for('account'))
    
    return render_template('user_login.html')


@app.route('/account')
def account():
    """ User profile page
    """
    
    if current_user.is_authenticated:
        account_type = ACCOUNT_TYPES[current_user.plan]
        expire = datetime.fromtimestamp(current_user.expire_plan).strftime('%d/%m/%Y')
        return render_template('user_profile.html', account_type = account_type, expire = expire)
    else:
        return redirect(url_for('form'))
        
@app.route('/demo')
def demo():
    user_logged = "true" if current_user.is_authenticated else "false"
    return render_template('demo.html', logged = user_logged)
    
@app.route('/terms')
def terms():
    user_logged = "true" if current_user.is_authenticated else "false"
    return render_template('terms.html', logged = user_logged)



#################
#  WEB SERVICES #
#################

@app.route('/signin', methods=['POST'])
def signin():
    """ User Login API
    """

    if current_user.is_authenticated:
        return redirect(url_for('account'))

    data = request.form

    if (data is not None) and ('username' in data) and ('password' in data):
        user = User('', username=data['username'], password=data['password'])
        users_manager = UsersManager(user)

        if 'remember' in data:
            rememberMe = data['remember']
        
        else:
            rememberMe = False

        if users_manager.check():

            if login_user(user, rememberMe):
                login_user(user, rememberMe)
                return redirect(url_for('account'))

            else:
                msg = 0
                return render_template('user_login.html', logmsg = msg)

        else:
            msg = 1
            return render_template('user_login.html', logmsg = msg)


@app.route('/signup', methods=['POST'])
def signup():
    """ User Registration API
    """

    if current_user.is_authenticated:
        return redirect(url_for('account'))

    data = request.form

    if (data is not None) and ('username' in data) and ('password' in data) and ('confirm_password' in data):
        user = User(data['username'], data['password'], data['name'], data['surname'], data['birthdate'], data['email'])
        manager = UsersManager(user)

        if data['password'] == data['confirm_password']:
            msg = 'Sign Up successful'

            if manager.fetch():
                msg = 'User already exists'

            else:
                manager.add()
                msg = 'Registration success, you can login'

        else:
            msg = 'Password unmatching'

        return render_template('user_login.html', message = msg)

    else:
        msg = 'Registration failed'
        return render_template('user_login.html', message = msg)


@app.route('/signout')
@login_required
def logout():
    """ User logout
    """

    logout_user()
    return redirect(url_for('home'))



@app.route('/mailregister', methods=['POST'])
def mailRegister():
    """ User registration mail request
    """

    data = request.form

    if (data is not None) and ('email' in data):
        m = MailManager()
        m.sendMail(data['email'])
        msg = 1

    else:
        msg = 0

    return render_template('user_login.html', regmsg = msg)



#################
#  SERVE FILES  #
#################

@app.route('/imgs/<path:filename>')
def getFile(filename):
    """ Serve static files utility
    """

    return send_file(IMGS_DIR + filename)
    

@app.route('/reports/<path:filename>')
@login_required
def getReport(filename):
    """ Serve custom report
    """
    
    try:
        if int(filename) in current_user.custom_trends.keys():
            return send_file('../data/ct/{}/Report.pdf'.format(filename), as_attachment=True)
        
        abort(401)
        
    except Exception as e: 
        print(e)
        abort(400)
    

@app.route('/sitemap')
def getSitemap():
    """ Serve webapp pages sitemap
    """

    return send_file(SITEMAP)


#########
#  API  #
#########

@app.route('/API/userupdate', methods=['POST'])
@login_required
def userUpdateAPI():
    """ User informations update API
    """

    data = request.get_json(force = True)
    manager = UsersManager(current_user)
    print(data)

    if (data is not None and 'name' in data and 'surname' in data and 'email' in data and 'birthdate' and 'newsletter'):
        manager.update(data['name'], data['surname'], data['email'], data['birthdate'], data['newsletter'])
        return redirect(url_for('account', saved = True))

    else:
        return redirect(url_for('account', failed = True))

@app.route('/API/pwdupdate', methods=['POST'])
@login_required
def userPwdAPI():
    """ User password update API
    """

    response = Response(True)
    data = request.get_json(force = True)
    manager = UsersManager(current_user)

    if (data is not None and 'new_pwd' in data):
        result, error = manager.newPassword(data['new_pwd'])

        if not result:
            response.status = False
            response.message = error

    else:
        response.status = False
        response.message = ERROR_MISSING_PARAMS


    return response.compose()

@app.route('/API/pwdlost', methods=['POST'])
def lostPwdAPI():
    """ User recovery lost password API
    """

    response = Response(True)
    data = request.get_json(force = True)

    if (data is not None and 'reg_email' in data):
        m = MailManager()
        m.sendRecovery(data['reg_email'])

    else:
        response.status = False
        response.message = ERROR_MISSING_PARAMS


    return response.compose()


@app.route('/API/gettrend', methods=['POST'])
def getTrendAPI():
    """ Get new home trends API
    """

    data = request.get_json(force = True)

    # Check params
    if (data is not None and 'key' in data and 'trend_id' in data and 'language'):

        # Check source
        if data['key'] == "anteo_frontend":
            return getTrend(data['trend_id'], data['language'])

    response = Response(False, ERROR_MISSING_PARAMS)
    return response.compose()


@app.route('/API/getcustomtrend', methods=['POST'])
@login_required
def getCustomTrendAPI():
    """Custom Trend API: retrieve custom trend data and configuration
    """

    data = request.get_json(force = True)
    
    if (data is not None and 'custom_trend_id' in data and data['custom_trend_id'] != ''):
        return getCustomTrend(data['custom_trend_id'])

    response = Response(False, ERROR_MISSING_PARAMS)
    return response.compose()


@app.route('/API/setcustomtrend', methods=['POST'])
@login_required
def setCustomTrendAPI():
    """ Set Trend API: retrieve custom trend data and configuration
    """

    data = request.get_json(force = True)

    if (data is not None and 'key' in data and 'custom_trend_id' in data['config']):
        return setCustomTrend(data['config']['custom_trend_id'], data['config'])
    
    else:
        response = Response(False, ERROR_MISSING_PARAMS)
        return response.compose()



@app.route('/API/addcustomtrend', methods=['POST'])
@login_required
def addCustomTrendAPI():
    """Add a new Custom Trend API
    """

    data = request.get_json(force = True)

    if (data is not None and 'key' in data and 'title' in data):
        used_trends = len(current_user.custom_trends.keys())
        if used_trends <= int(current_user.plan):
            try:
                return addCustomTrend(current_user.id, data['title'])
            except Exception as e:
                response = Response(False, ERROR_GENERAL)
                return response.compose()
        else:
            response = Response(False, ERROR_API)
    
    else:
        response = Response(False, ERROR_MISSING_PARAMS)
        
    return response.compose()



@app.route('/API/delcustomtrend', methods=['POST'])
@login_required
def delCustomTrendAPI():
    """Delete Custom Trend API: delete a trend
    """

    data = request.get_json(force = True)

    if (data is not None and 'key' in data and 'custom_trend_id' in data):
        return delCustomTrend(data['custom_trend_id'])
    else:
        return Response(False, ERROR_MISSING_PARAMS)


@app.route('/API/getuser', methods=['GET'])
@login_required
def getUserAPI():
    """Get user informations API
    """

    if current_user.is_authenticated:
        return getUser(current_user)
    else:
        return 'Sign in first'
        
@app.route('/API/demorequest', methods=['POST'])
def demoRequestAPI():
    data = request.get_json(force = True)

    if (data is not None and 'demo-mail' in data and 'demo-name' in data and 'demo-company' in data and 'demo-brand' in data):
        return demoRequest(data['demo-mail'], data['demo-name'], data['demo-company'], data['demo-brand'])
        
    else:
         return Response(False, ERROR_MISSING_PARAMS)
    

############
#  ERRORS  #
############

@app.errorhandler(Exception)
def error_moved(e):
    return render_template('error.html', code=e.code)
