from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from google.appengine.ext import db

from BeautifulSoup import BeautifulStoneSoup


import datetime

import redirect

import logging

class ContentFeed(db.Model):
    url = db.LinkProperty()
    title = db.TextProperty()
    content = db.TextProperty()
    retrieve_date = db.DateTimeProperty()

class MainPage(webapp.RequestHandler):
    def get(self):
        url = "http://sites.google.com/feeds/content/site/charlesmdietrich?path=/home"
        result = urlfetch.fetch(url)
        if result.status_code == 200:
            retrieve_date = datetime.datetime.now()
            soup = BeautifulStoneSoup(result.content)
            category = soup.find('category')
            title = category.title.string
            content = "".join([str(c) for c in category.find('content').contents]).replace('rel="nofollow"', "")
            try:
                content_feed = ContentFeed(url = url,
                                   title = title,
                                   content = content,
                                   retrieve_date = retrieve_date)
                content_feed.put()
            except Exception, e:
                logging.error(e)
                raise e
        else:
            try:
                feeds = ContentFeed.all()
                feeds.filter("url =", url)
                feeds.order("-retrieve_date")
                title = feeds[0].title
                content = feeds[0].content
            except Exception, e:
                logging.error(e)
                self.error(404)
            
        template_values = {
                'title': title,
                'content': content
                }
        path = os.path.join(os.path.dirname(__file__), 'index.html')
        self.response.out.write(template.render(path, template_values))
    
class TagRedirectHandler(webapp.RequestHandler):
    def get(self, root, path):
        dst = "%s%s" % (redirect.tags_dst, path)
        self.redirect(dst, True) # permanent redirect

class RedirectHandler(webapp.RequestHandler):
    def get(self, path):
        d = redirect.explicit_data
        if path in d.keys():
            dst = d[path]
            self.redirect(dst, True) # permanent redirect
        else:
            self.error(404)
            
application = webapp.WSGIApplication(
                                     [('/', MainPage),
                                      (redirect.tags_regex, TagRedirectHandler),
                                      ('(.*)', RedirectHandler)],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
