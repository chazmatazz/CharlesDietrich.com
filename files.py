redirect_type = '307'

f = open('files.txt', 'r')
for line in f:
    path = line[1:-1]
    print "Redirect %s %s http://media.charlesdietrich.com%s" % (redirect_type, path, path)