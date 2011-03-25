from xml.etree.ElementTree import ElementTree

redirect_type = '307'

tree = ElementTree()
tree.parse('charlesdietrich-wp.xml')
channel = tree.find('channel')
items = channel.getiterator('item')
for e in items:
    mywpstatus = e.find('mywpstatus')
    if mywpstatus is not None and mywpstatus.text != 'draft':
        link = e.find('link').text.replace("http://www.charlesdietrich.com", "")
        link2 = link[:-1]
        print "Redirect %s %s http://blog.charlesdietrich.com%s.html" % (redirect_type, link, link2)