from flask import Flask, render_template, json, request,redirect,session
from flaskext.mysql import MySQL
from werkzeug import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)
app.secret_key = 'why would I tell you my secret key?'

# MySQL configurations
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'Santhu_1007'
app.config['MYSQL_DATABASE_DB'] = 'BucketList'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
mysql.init_app(app)


@app.route('/')
def main():
    return render_template('index.html')

@app.route('/showSignUp')
def showSignUp():
    return render_template('signup.html')

@app.route('/showSignin')
def showSignin():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('signin.html')

@app.route('/userHome')
def userHome():
    if session.get('user'):
        return render_template('userHome.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')


@app.route('/logout')
def logout():
    session.pop('user',None)
    return redirect('/')

@app.route('/signUp',methods=['POST'])
def signUp():
    try:
        _name = request.form['inputName']
        _email = request.form['inputEmail']
        _password = request.form['inputPassword']

        # validate the received values
        if _name and _email and _password:

            # All Good, let's call MySQL

            conn = mysql.connect()
            cursor = conn.cursor()
            _hashed_password = generate_password_hash(_password)
            cursor.callproc('sp_createUser',(_name,_email,_hashed_password))
            data = cursor.fetchall()

            if len(data) is 0:
                conn.commit()
                return json.dumps({'message':'User created successfully !'})
            else:
                return json.dumps({'error':str(data[0])})
        else:
            return json.dumps({'html':'<span>Enter the required fields</span>'})

    except Exception as e:
        return json.dumps({'error':str(e)})
    finally:
        cursor.close()
        conn.close()

@app.route('/validateLogin',methods=['POST'])
def validateLogin():
    try:
        _username = request.form['inputEmail']
        _password = request.form['inputPassword']



        # connect to mysql

        con = mysql.connect()
        cursor = con.cursor()
        cursor.callproc('sp_validateLogin',(_username,))
        data = cursor.fetchall()




        if len(data) > 0:
            if check_password_hash(str(data[0][3]),_password):
                session['user'] = data[0][0]
                return redirect('/userHome')
            else:
                return render_template('error.html',error = 'Wrong Email address or Password.')
        else:
            return render_template('error.html',error = 'Wrong Email address or Password.')


    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        con.close()


@app.route('/showAddSector')
def showAddSector():
    if session.get('user'):
        return render_template('addSector.html')
    else:
        return render_template('error.html',error = 'Unauthorized Access')

@app.route('/addSector',methods=['POST'])
def addSector():
    try:
        if session.get('user'):
                sector_number = request.form['inputSectorNumber']
                sector_name = request.form['inputSectorName']
                sector_city = request.form['inputCity']
                sector_state = request.form['inputState']
                sector_rain = request.form['inputRain']
                # validate the received values    # All Good, let's call MySQL
                conn = mysql.connect()
                cursor = conn.cursor()
                cursor.callproc('sp_createSector',(sector_number,sector_name,sector_city,sector_state,sector_rain))
                data = cursor.fetchall()
                if len(data) is 0:
                        conn.commit()
                        return redirect('/userHome')
                else:
                        return render_template('error.html',error = 'An error occurred!')

        else:
                return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()



@app.route('/addFarm',methods=['POST'])
def addFarm():
    try:
        if session.get('user'):
                sector_number = request.form['inputSectorNumber']
                farm_id = request.form['inputFarmId']
                last_produce = request.form['inputLastProduce']
                next_crop = request.form['NextCrop']
                req_supple = request.form['inputSupple']
                req_water=request.form['inputWater']
                conn = mysql.connect()
                cursor = conn.cursor()
                # validate the received values    # All Good, let's call MySQL
                cursor.callproc('sp_createFarm',(sector_number,farm_id,last_produce,next_crop,req_supple,req_water))
                data = cursor.fetchall()
                if len(data) is 0:
                        conn.commit()
                        return redirect('/userHome')
                else:
                        return redirect('/userHome')

        else:
                return render_template('error.html',error = 'Unauthorized Access')
    except Exception as e:
        return render_template('error.html',error = str(e))
    finally:
        cursor.close()
        conn.close()


@app.route('/showAddFarm',methods=['GET'])
def showAddFarm():
    # if session.get('user'):
        return render_template('addFarm.html')
    # else:
    #     return render_template('error.html',error = 'Unauthorized Access')

if __name__ == "__main__":
    app.run(port=5002)
