from kagami import app, get_api
from flask import session, render_template, abort, redirect, request, url_for
from kagami.handler import reply_handle, quote_handle


@app.route('/')
def show():
    if not session.get('logged_in'):
        return render_template('send.html')
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    page = '1'
    if request.args.get('page', ''):
        page = request.args.get('page', '')
    status = api.home_timeline(page=int(page))
    return render_template('send.html', statuses=status, me=session.get('me'),
                           page=page, npage=int(page)+1, ppage=int(page)-1, op='show')


@app.route('/update', methods=['POST'])
def update():
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    api.update_status(status=request.form['text'])
    return redirect(url_for('show'))


@app.route('/reply/<status_id>', methods=['GET', 'POST'])
def reply(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    if request.method == 'POST':
        api.update_status(status=request.form['text'],
                          in_reply_to_status_id=status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('detail.html', status=status, head=reply_handle(status.text,
                                                                          session.get('me'),
                                                                          status.user.screen_name),
                           reply=True, me=session.get('me'))


@app.route('/fav/<status_id>', methods=['GET', 'POST'])
def fav(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    if request.method == 'POST':
        api.create_favorite(status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('detail.html', fav=True, status=status, me=session.get('me'))


@app.route('/unfav/<status_id>', methods=['GET', 'POST'])
def unfav(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    if request.method == 'POST':
        api.destroy_favorite(status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('detail.html', unfav=True, status=status, me=session.get('me'))


@app.route('/retweet/<status_id>', methods=['GET', 'POST'])
def retweet(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    if request.method == 'POST':
        api.retweet(status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('detail.html', retweet=True, status=status, me=session.get('me'))


@app.route('/unretweet/<status_id>', methods=['GET', 'POST'])
def unretweet(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    if request.method == 'POST':
        api.destroy_status(status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('detail.html', unretweet=True, status=status, me=session.get('me'))


@app.route('/quote/<status_id>', methods=['GET', 'POST'])
def quote(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    if request.method == 'POST':
        api.update_status(status=request.form['text'],
                          in_reply_to_status_id=status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('detail.html', status=status, quote=True,
                           head=quote_handle(status.text, status.user.screen_name), me=session.get('me'))


@app.route('/detail/<status_id>')
def detail(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    status = api.get_status(status_id)
    return render_template('detail.html', status=status, me=session.get('me'))


@app.route('/delete/<status_id>', methods=['GET', 'POST'])
def delete(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    status = api.get_status(status_id)
    if request.method == 'POST':
        api.destroy_status(status_id)
        return redirect(url_for('show'))
    return render_template('detail.html', status=status, delete=True, me=session.get('me'))
