from flask import Flask, render_template, abort, flash, redirect, request, url_for, render_template
import os
from werkzeug.utils import secure_filename


app = Flask(__name__)


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)