import json
from flask import Flask, request, redirect, flash, render_template, \
    get_flashed_messages
from hashlib import sha256


app = Flask('file_checker')

# Secret is placed to simplify development
app.secret_key = b'\x18c\xe9Fk\xdd\x95\xbe\xa3\xb1\xc0\xf7\xf1\xaa\xb4\x82' \
                 b'\xb1\xder\x7f\xc6\tS\x18'


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render()

    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            checksum = sha256(file.stream.read()).hexdigest()
            return render(checksum=checksum, total=0)


def render(**context):
    if request.is_xhr:
        context['messages'] = get_flashed_messages()
        return json.dumps(context)

    return render_template('index.html', **context)
