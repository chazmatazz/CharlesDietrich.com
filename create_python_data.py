f = open('../htaccess', 'r')
for line in f:
    if line.startswith("Redirect"):
        path = line.split(" ")
        print "['%s', '%s']" % (path[2], path[3][:-1])