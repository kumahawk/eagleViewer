import os

if not os.environ.get('EAGLEVIEWERDB'):
    os.environ['EAGLEVIEWERDB'] = os.path.join(os.path.dirname(__file__), 'var', 'eagle.db')

import eagleviewer
eagleviewer.dbbuilder.start("C:\\exchange\\eagle\\SD.library")
x = eagleviewer.dbbuilder.wait(3)
print(x)
while x["running"]:
    x = eagleviewer.dbbuilder.wait(10)
    print(x)
