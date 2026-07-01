from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('index.html')

@app.route('/departements')
def departements():
    return render_template('departements.html')

@app.route('/formations')
def formations():
    return render_template('formations.html')

if __name__ == '__main__':
    app.run(debug=True)