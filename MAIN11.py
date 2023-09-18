from flask import Flask, render_template, request, redirect, url_for, flash
from flask_mysqldb import MySQL
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa, padding
import base64
import hashlib


import encryptData
import decryptData
import createKey

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'localhost'  
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'massageapp'

mysql = MySQL(app)


@app.route('/main')
def main():
    return render_template('welcome.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST' :
         h=hashlib.new("sha1")
         role=request.form['role']
         username=request.form['username']
         password=request.form['password']
         cursor = mysql.connection.cursor()
         h.update(password.encode())
         hashpw=h.hexdigest()

         cursor.execute("INSERT INTO users VALUES (NULL, %s, %s, %s)", (role, username, hashpw))
         mysql.connection.commit()
         
         cursor.close()
         return redirect('/')
    
    return render_template('register.html')


@app.route('/', methods=['GET', 'POST'])
def send_message():
    if request.method == 'POST':
        role = request.form['role'].upper()
        message = request.form['message']
        print('Saved: ' + message)

        # Call the functions to generate keys and encrypt data
        createKey.KeyGeneration()
        encryptData.EncryptAndSaveMessage(role, message)

        # Redirect to the success page or display a success message
        return redirect('/message')
    else:
        # Render the form template when the page is accessed via GET request
        return render_template('messagebox.html')

# @app.route('/', methods=['GET', 'POST'])
# def gotoRegistre():

#     if 'go_to_register' in request.form:
#             # Redirect to the register page
#             return redirect('/register')
#     return render_template('message.html')

@app.route('/message', methods=['GET', 'POST'])
def show_message():

    # error_message = None 
    if request.method == 'POST':
        h=hashlib.new("sha1")
        username = request.form['username']
        password = request.form['password']
        h.update(password.encode())
        

        hashpw=h.hexdigest()

        if username != '' and password != '':
            cursor = mysql.connection.cursor()
            cursor.execute("SELECT * FROM users where username = %s AND password = %s", (username, hashpw))
            result = cursor.fetchone()
            if result:
                print(result[1])
                role = result[1].upper()
                message = decryptData.DecryptAndDisplayMessage(role)
                return render_template('message.html', role=role, message=message)    
        #     else:
        #       error_message='error_message ' 
    return render_template('message.html')

    
if __name__ == '__main__':
    app.run(debug=True)
