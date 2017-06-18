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
        if 'checksum' in request.form and request.form['checksum']:
            checksum = request.form['checksum']
            total = update(checksum)
            return render(checksum=checksum, total=total)
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)

        if file:
            checksum = sha256(file.stream.read()).hexdigest()
            total = update(checksum)
            return render(checksum=checksum, total=total)


def update(checksum):
    try:
        db_file = open('db.json')
        db = json.load(db_file)
        db_file.close()
    except OSError:
        db = {}

    if checksum not in db:
        db[checksum] = 0
    db[checksum] += 1

    with open('db.json', 'w+') as db_file:
        json.dump(db, db_file)

    return db[checksum]


def render(**context):
    if request.is_xhr:
        context['messages'] = get_flashed_messages()
        return json.dumps(context)

    return render_template('index.html', **context)
