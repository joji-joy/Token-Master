# from flask import Flask, request, jsonify
from flask import *
import os
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import smtplib
import pandas as pd
import io
from datetime import timedelta

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'joji123'
app.config['MYSQL_DB'] = 'traffic'
 
mysql = MySQL(app)

app.secret_key = "joe123bhai321"
app.permanent_session_lifetime = timedelta(minutes=30)

token = 0  # Initialize the token value

globaldate = None

joenum = 0

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/logout')
def logout():
    session.clear()
    global joenum
    joenum = 0
    return render_template('loggingout.html')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('error.html'), 404

@app.route('/page1')
def page1():
    if joenum == 1:
        return render_template('test_page1.html')
    else:
        return render_template('login.html')

@app.route('/page2')
def page2():
    if joenum == 1:
        return render_template('test_page2.html')
    else:
        return render_template('login.html')

@app.route('/page3')
def page3():
    return render_template('test_page3.html')

@app.route('/list')
def liststart():
    if joenum == 1:
        return render_template('list.html')
    else:
        return render_template('login.html')

@app.route('/search')
def search():
    if joenum == 1:
        return render_template('search.html')
    else:
        return render_template('login.html')

@app.route('/get_token', methods=['GET'])
def get_token():
    formatted_token = f'{token:02d}'  # Format the token as a two-digit number with leading zeros
    return jsonify({'token': formatted_token})

@app.route('/increment_token', methods=['POST'])
def increment_token():
    global token
    token += 1
    formatted_token = f'{token:02d}'  # Format the token as a two-digit number with leading zeros
    return jsonify({'token': formatted_token})

@app.route('/jump_token', methods=['POST'])
def jump_token():
    global token
    data = request.get_json()
    if 'token' in data:
        token = data['token']
    return jsonify(token=token)

@app.route('/decrement_token', methods=['POST'])
def decrement_token():
    global token
    token -= 1
    token = max(0, token)  # Ensure the token value is not less than 0
    formatted_token = f'{token:02d}'  # Format the token as a two-digit number with leading zeros
    return jsonify({'token': formatted_token})

@app.route('/generate',methods= ['GET',"POST"])
def generate():
    if request.method == 'POST':
        # Create variables for easy access
        firstname = request.form['first']
        lastname = request.form['last']
        name = firstname + " " + lastname
        email = request.form['email']
        phone = request.form['pno']
        datee = request.form['date']
        nedate = datee.replace("-", "/")
        date = datee.replace("-", "_")

        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,10}$"
        pattern = re.compile(reg)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Check if account exists using MySQL)
        # cursor.execute('SELECT * FROM information_schema.tables WHERE table_name = %s', (date,))
        cursor.execute('SHOW TABLES LIKE %s', (date,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            cursor.execute(f"SELECT * FROM {date} WHERE Name = '{name}'")
            account = cursor.fetchone()
            if account:
                # return redirect(url_for('generate',invoke_exist=True))
                disname = account['Name']
                distoken = account['Token']
                newtoken = f'{distoken:02d}'
                return render_template('tokenissue.html',invoke_exist=True,name=disname,date=nedate,token=newtoken)
            else:
                cursor.execute(f"INSERT INTO {date} VALUES (NULL, '{name}', '{phone}', '{email}')")
                cursor.execute(f"SELECT * FROM {date} WHERE Name = '{name}'")
                nwaccount = cursor.fetchone()
                disname = nwaccount['Name']
                distoken = nwaccount['Token']
                newtoken = f'{distoken:02d}'
                mysql.connection.commit()
                return render_template('tokenissue.html',invoke_create=True,name=disname,date=nedate,token=newtoken)
        else:
            # Account doesnt exists and the form data is valid, now insert new account into employee table
            cursor.execute(f'CREATE TABLE {date} (Token INT AUTO_INCREMENT PRIMARY KEY, Name varchar(30), Phone varchar(30), Email varchar(30))')
            cursor.execute(f"INSERT INTO {date} VALUES (NULL, '{name}', '{phone}', '{email}')")
            cursor.execute(f"SELECT * FROM {date} WHERE Name = '{name}'")
            nwaccount = cursor.fetchone()
            disname = nwaccount['Name']
            distoken = nwaccount['Token']
            newtoken = f'{distoken:02d}'
            mysql.connection.commit()
            return render_template('tokenissue.html',invoke_create=True,name=disname,date=nedate,token=newtoken)
    if joenum == 1:
        return render_template('tokenissue.html')
    else:
        return render_template('login.html')

@app.route('/listfetch',methods= ['GET',"POST"])
def listfetch():
    if request.method == 'POST':
        datee = request.form['date']
        nedate = datee.replace("-", "/")
        date = datee.replace("-", "_")
        global globaldate
        globaldate = date
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM {date}")
            users = cursor.fetchall()
            return render_template('list.html', invoke_yes=True, users=users, date_value=datee)
        except MySQLdb.Error as err:
            return render_template('list.html', invoke_empty=True, date_value=datee)
        finally:
            cursor.close()

@app.route('/find',methods= ['GET',"POST"])
def find():
    if request.method == 'POST':
        datee = request.form['date']
        nedate = datee.replace("-", "/")
        date = datee.replace("-", "_")
        select = request.form['selec']
        selection = request.form['selection']
        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f"SELECT * FROM {date} WHERE {select} = '{selection}'")
            data = cursor.fetchone()
            if data:
                return render_template('search.html', invoke_yes=True, data=data, date2=date)
            else:
                return render_template('search.html', invoke_empty=True, data1=select, data2=selection, date2=datee)
        except MySQLdb.Error as err:
            return render_template('search.html', invoke_empty=True, data1=select, data2=selection, date2=datee)
        finally:
            cursor.close()

@app.route('/edit',methods= ['GET',"POST"])
def edit():
    if request.method == 'POST':
        edtoken = request.form['edtoken']
        edname = request.form['edname']
        edphone = request.form['edphone']
        edemail = request.form['edemail']
        eddate = request.form['edtable']
        edtable = str(eddate)

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute(f"UPDATE {edtable} SET Name='{edname}' , Phone='{edphone}' , Email='{edemail}'   WHERE Token='{edtoken}'")
        mysql.connection.commit()
        cursor.close()
        return render_template('search.html', invoke_success=True)
    else:
        return render_template('search.html')

@app.route('/delete',methods= ['GET',"POST"])
def delete():
    if request.method == 'POST':
        edtoken = request.form['edtoken']
        edname = request.form['edname']
        eddate = request.form['edtable']
        edtable = str(eddate)

        try:
            cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute(f"DELETE FROM {edtable} WHERE Name = '{edname}' AND Token = '{edtoken}'")
            mysql.connection.commit()
            return render_template('search.html', invoke_success=True)
        except MySQLdb.Error as err:
            return render_template('search.html', invoke_fail=True)
        finally:
            cursor.close()

@app.route('/export')
def export():
    # Connect to the database
    cur = mysql.connection.cursor()
    global globaldate
    # Execute a query to fetch data
    query = f"SELECT * FROM {globaldate}"
    cur.execute(query)

    # Fetch all rows from the executed query
    rows = cur.fetchall()
    columns = [desc[0] for desc in cur.description]

    # Close the cursor
    cur.close()

    # Convert the data to a pandas DataFrame
    df = pd.DataFrame(rows, columns=columns)

    # Save the dataframe to an Excel file in memory
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Sheet1')

    output.seek(0)  # Reset the buffer position to the beginning

    return send_file(output, download_name=f'{globaldate}.xlsx', as_attachment=True, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/register',methods= ['GET',"POST"])
def register():
    if request.method == 'POST':
        username = request.form['uname']
        email = request.form['email']
        phone = request.form['pno']
        password = request.form['pass']

        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        # Check if account exists using MySQL)
        cursor.execute('SELECT * FROM register WHERE Username = %s', (username,))
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            return render_template('login.html', invoke_exist=True ,invoke_reg=True)
        else:
            # Account doesnt exists and the form data is valid, now insert new account into employee table
            cursor.execute('INSERT INTO register VALUES (NULL, %s, %s, %s, %s)', (username, password, email, phone))
            mysql.connection.commit()
            return render_template('tokenissue.html',invoke_joe=True)
    return render_template('login.html', invoke_reg=True)

@app.route('/login',methods= ['GET',"POST"])
def login():
    global joenum
    if 'user_id' in session:
        session.permanent = True
        joenum = 1
        return render_template('loggingin.html')
    else:
        return render_template('login.html')

@app.route('/loginaction', methods =['GET', 'POST'])
def loginaction():
    global joenum
    if request.method == 'POST':
        username = request.form['uname']
        password = request.form['pass']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM register WHERE username = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            # redirect(url_for('generate'))
            session['user_id'] = username
            joenum = 1
            return render_template('tokenissue.html')
        else:
            return render_template('login.html',invoke_exist=True)
    return render_template('login.html')

if __name__ == '__main__':
    app.run()
