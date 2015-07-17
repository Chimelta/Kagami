from kagami import app, get_api
from flask import session, render_template, abort, request
import kagami.handler


@app.route('/mention')
def mention():
    if not session.get('logged_in'):
        abort(401)
    api = get_api(app.config['CK'], app.config['CS'], session.get('at'), session.get('as'))
    page = '1'
    if request.args.get('page', ''):
        page = request.args.get('page', '')
    mention_list = api.mentions_timeline(page=page)
    return render_template('send.html', statuses=mention_list,
                           page=page, ppage=str(int(page)-1),
                           npage=str(int(page)+1), op='mention', me=session.get('me'),
                           handler=kagami.handler)
