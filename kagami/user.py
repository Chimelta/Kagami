from kagami import app, get_api
from flask import session, render_template, abort, redirect, url_for
from flask import request
import kagami.handler


@app.route('/user/<username>')
def user(username: str):
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    page = '1'
    if request.args.get('page', ''):
        page = request.args.get('page', '')
    friendships = None
    if username != session.get('me'):
        friendships = api.show_friendship(source_screen_name=session.get('me'), target_screen_name=username)[0]
    status_list = api.user_timeline(username, page=int(page))
    user = api.get_user(username)
    return render_template('user.html', head='@'+username+' ', statuses=status_list, me=session.get('me'),
                           page=page, npage=int(page)+1, ppage=int(page)-1, username=username,
                           handler=kagami.handler, user=user, friendship=friendships)


@app.route('/me')
def me():
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    username = api.me().screen_name
    return redirect(url_for('user', username=username))


@app.route('/follow/<username>')
def follow(username: str):
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    api.create_friendship(screen_name=username)
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
def unfollow(username: str):
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    api.destroy_friendship(screen_name=username)
    return redirect(url_for('user', username=username))
