#!/usr/bin/python

import bot

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
        else:
            self.response.out.write('unknown action')

    def post(self, action):
        if action == 'comment':
            bot.comment(self.request.get('parent'), self.request.get('text'))

class WarmupHandler(webapp2.RequestHandler):

    def get(self):
        """Handle warmup requests"""
        bot.startup()
        self.response.out.write('started')

app = webapp2.WSGIApplication([
    ('/do/([a-z]+)/?', ExecHandler),
    ('/_ah/warmup', WarmupHandler),
], debug=True)
