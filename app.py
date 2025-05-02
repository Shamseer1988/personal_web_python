from flask import Flask, render_template, request, redirect, url_for, session

from lights import lights_bp  # ← Import the blueprint
from frigate import frigate_bp  # ← Import the blueprint

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Use a secure, random value in production

# Register blueprint
app.register_blueprint(lights_bp)
app.register_blueprint(frigate_bp)

########################### AUTH SECTION ##############################
# Hardcoded credentials
USERNAME = 'admin'
PASSWORD = 'pass123'


@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = request.form['username']
        pw = request.form['password']
        if user == USERNAME and pw == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('dashboard'))
        return render_template('login.html', error='Invalid Credentials')
    return render_template('login.html')


@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    return render_template('dashboard.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))


################## AUTH SECTION ####################################



if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
