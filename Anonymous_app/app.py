from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['GET', 'POST'])
def submit_tip():
    if request.method == 'POST':
        tip = request.form['tip']
        # Save the tip here (file, DB, etc.)
        print(f"Tip received: {tip}")
        return redirect(url_for('thank_you'))
    return render_template('submit_tip.html')

@app.route('/thank-you')
def thank_you():
    return render_template('thank_you.html')

if __name__ == '__main__':
    app.run(debug=True, port=5001)
