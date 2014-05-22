#!/usr/bin/python

import bot
from bot import storage

#import os
#import logging
#import urllib
import webapp2


class ExecHandler(webapp2.RequestHandler):

    def get(self, action):
        """Perform tasks"""
        if action == 'post':
            bot.do()
            self.response.out.write('ok')
        elif action == 'simulate':
            bot.do(True)
            self.response.out.write('simulated')
        elif action == 'session':
            # Incomplete HTML, but who cares?
            self.response.out.write("""
<form action="" method="POST">
    <input type="submit" value="Set!"><br>
    <input type="text" name="modhash" placeholder="modhash"><br>
    <input type="text" name="cookie" placeholder="cookie">
</form>""")
        else:
            self.response.out.write('unknown action')

    def post(self, action):
        if action == 'comment':
            bot.comment(self.request.get('parent'), self.request.get('text'))
        elif action == 'session':
            data = (self.request.get('modhash'), self.request.get('cookie'))
            storage.setAuthorization(*data)
            bot.authorized(data)
            self.response.out.write('session info set')

class WarmupHandler(webapp2.RequestHandler):

    def get(self):
        """Handle warmup requests"""
        bot.startup()
        self.response.out.write('started')

app = webapp2.WSGIApplication([
    ('/do/([a-z]+)/?', ExecHandler),
    ('/_ah/warmup', WarmupHandler),
], debug=True)
