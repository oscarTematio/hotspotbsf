from flask import Flask, render_template, redirect, url_for, request
import os, subprocess

app = Flask(__name__)


# Route for handling the login page logic
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' or request.form['password'] != 'admin':
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('formulaire'))
    return render_template('login.html', error=error)


def get_values():
    g_ssid = subprocess.check_output('cat /etc/hostapd/hostapd.conf | grep ^ssid', shell=True)
    passwd = subprocess.check_output('cat /etc/hostapd/hostapd.conf | grep ^wpa_passphrase', shell=True)
    stat = os.system('sudo systemctl is-active hostapd.service')
    g_ssid_1 = g_ssid.decode("utf-8").split('\n')[0]
    g_ssid_2 = g_ssid_1.split('=')

    passw = passwd.decode("utf-8").split('\n')[0]
    passwrd_1 = passw.split('=')

    status = str(stat)

    ssid = g_ssid_2[1]
    
    password = passwrd_1[1]

    return [ssid, status, password]


@app.route('/home',  methods=['GET', 'POST'])
def formulaire():
    error = None
  
    if request.method == 'POST': 
        
        liste = get_values()
        c_name = liste[0]
        c_pass = liste[2]
        if request.form.get('check') == 'on':
            os.system('sudo systemctl start hostapd.service')
            return render_template('started.html')
        else:
            os.system('sudo systemctl stop hostapd.service') 
           

            print('befoooooooooooooooooooooooooooooooooore')
            print(request.form)
            n_name = request.form['name']
            current_pass = request.form['current_pass']
            n_pass = request.form['new_pass']
            print(c_pass+"------"+current_pass)
            print('afterrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrrr')
            if c_pass != current_pass :
                error = "The Current password you've written is incorrect please check it"
            else:
                os.system("sudo sed -i 's/ssid=" + c_name + "/ssid=" + n_name + "/g' /etc/hostapd/hostapd.conf")
                os.system("sudo sed -i 's/wpa_passphrase=" + c_pass + "/wpa_passphrase=" + n_pass + "/g' /etc/hostapd/hostapd.conf")
                print('befoooooooooooooooooooooooooooooooooore')
                return render_template("change.html")

        
    return render_template("hotspot.html", error=error)


        
        



        
        



if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0' , port=5000)
    
