import os

if not os.environ.get('EAGLEVIEWERDB'):
    os.environ['EAGLEVIEWERDB'] = os.path.join(os.path.dirname(__file__), 'var', 'eagle.db')

from eagleviewer import app

app.run(port=5000, debug=True)