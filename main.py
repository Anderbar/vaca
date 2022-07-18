from flask import Flask, flash, render_template, \
     request


app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route('/', methods=['GET', 'POST'])
def begin():
    if request.method == 'POST':
        budget = request.form.get("budget")
        flash(budget, category='error')
    
    return render_template('home.html')

if __name__ == '__main__':
   app.run(use_reloader=False, debug=True)