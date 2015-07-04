from kagami import app
from flask import session, render_template, abort, redirect, request, url_for
import tweepy
from kagami.handler import reply_handle, quote_handle


@app.route('/')
def show():
    if session.get('logged_in'):
        auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
        auth.set_access_token(session.get('at'), session.get('as'))
        api = tweepy.API(auth)
        status = api.home_timeline()
        return render_template('send.html', statuses=status, me=session.get('me'))
    return render_template('send.html')


@app.route('/update', methods=['POST'])
def update():
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    api.update_status(status=request.form['text'])
    return redirect(url_for('show'))


@app.route('/reply/<status_id>', methods=['GET', 'POST'])
def reply(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    if request.method == 'POST':
        api.update_status(status=request.form['text'],
                          in_reply_to_status_id=status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('reply.html', status=status, head=reply_handle(status.text,
                                                                          session.get('me'),
                                                                          status.user.screen_name))


@app.route('/fav/<status_id>', methods=['GET', 'POST'])
def fav(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    if request.method == 'POST':
        api.create_favorite(status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('fav.html', status=status)


@app.route('/unfav/<status_id>', methods=['GET', 'POST'])
def unfav(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    if request.method == 'POST':
        api.destroy_favorite(status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('unfav.html', status=status)


@app.route('/retweet/<status_id>', methods=['GET', 'POST'])
def retweet(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    if request.method == 'POST':
        api.retweet(status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('retweet.html', status=status)


@app.route('/unretweet/<status_id>', methods=['GET', 'POST'])
def unretweet(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    if request.method == 'POST':
        api.destroy_status(status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('unretweet.html', status=status)


@app.route('/quote/<status_id>', methods=['GET', 'POST'])
def quote(status_id: str):
    if not session.get('logged_in'):
        abort(401)
    auth = tweepy.OAuthHandler(app.config['CK'], app.config['CS'])
    auth.set_access_token(session.get('at'), session.get('as'))
    api = tweepy.API(auth)
    if request.method == 'POST':
        api.update_status(status=request.form['text'],
                          in_reply_to_status_id=status_id)
        return redirect(url_for('show'))
    status = api.get_status(status_id)
    return render_template('reply.html', status=status, head=quote_handle(status.text,
                                                                          status.user.screen_name))
