from flask import Flask
from flask import render_template

app = Flask(__name__)

# localhost:5000
@app.route('/index')
def index():
    # current_title -> set in index.html file
    return render_template('index.html', current_title = 'Index Endpoint')

@app.route('/about')
def about():
    # current_title -> set in index.html file
    return render_template('about.html', current_title = 'About Endpoint')



if __name__ == "__main__":
    app.run(debug=True)