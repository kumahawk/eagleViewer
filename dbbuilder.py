import eagleviewer

eagleviewer.dbbuilder.start("\\\\yoqnap\\exchange\\eagle\\SD.library")
x = eagleviewer.dbbuilder.wait(3)
print(x)
while x["running"]:
    x = eagleviewer.dbbuilder.wait(10)
    print(x)
