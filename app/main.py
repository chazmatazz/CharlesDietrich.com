from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
import os
from google.appengine.ext.webapp import template
from google.appengine.api import urlfetch
from google.appengine.ext import db

import gdata.sites.client

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
        home_content = "http://sites.google.com/feeds/content/site/charlesmdietrich?path=/home"
        try:
            feed = gdata.sites.client.SitesClient().GetContentFeed(uri=home_content)
            retrieve_date = datetime.datetime.now()
            title = feed.entry[0].title.text
            content = str(feed.entry[0].content.html)
            try:
                content_feed = ContentFeed(url = home_content,
                                   title = title,
                                   content = content,
                                   retrieve_date = retrieve_date)
                content_feed.put()
            except Exception, e:
                logging.error(e)
        except Exception, e:
            logging.error(e)

            try:
                feeds = ContentFeed.all()
                feeds.filter("url =", home_content)
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
        self.redirect(dst, False) # temporary redirect

class RedirectHandler(webapp.RequestHandler):
    def get(self, path):
        d = redirect.explicit_data
        if path in d.keys():
            dst = d[path]
            self.redirect(dst, False) # temporary redirect
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
