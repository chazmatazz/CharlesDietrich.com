import app.redirect
import httplib
import urlparse

external = ("external_data", "", app.redirect.external_data, {})
internal = ("internal_data", "http://localhost:8081", app.redirect.internal_data, {})

lst = [external]

for (type, prefix, data, dst) in lst:
    for k in data.keys():
        host, path = urlparse.urlsplit(prefix+data[k])[1:3]
        try:
            connection = httplib.HTTPConnection(host)  ## Make HTTPConnection Object
            connection.request("HEAD", path)
            responseOb = connection.getresponse()      ## Grab HTTPResponse Object
    
            dst[k] = data[k]
        except Exception, e:
            pass
        
        
    print "%s = {%s}" % (type, ",\n".join("'%s': '%s'" % (k, dst[k]) for k in sorted(dst.keys())))