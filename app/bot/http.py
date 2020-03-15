#!/usr/bin/python

import logging
from .config import USERAGENT

import random
import urllib

from google.appengine.api import urlfetch


def getNew(last='', subreddit='all'):
    url = 'https://www.reddit.com/r/%s/new.json?limit=100' % (subreddit)
    if last:
        url += '&before=' + last
    url = '%s&%f' % (url, random.random())
    logging.debug(url)
    return urlfetch.fetch(url, headers={'User-Agent': USERAGENT})


def authorize(username, password):
    payload = urllib.urlencode({
        'api_type': 'json',
        'user': username,
        'passwd': password,
    })
    return urlfetch.fetch('https://ssl.reddit.com/api/login',
                          payload=payload,
                          method=urlfetch.POST,
                          headers={'User-Agent': USERAGENT})


def postComment(parent, text, modhash, session):
    payload = urllib.urlencode({
        'api_type': 'json',
        'text': text.encode('utf-8'),
        'thing_id': parent.encode('utf-8'),
        'uh': modhash,
    })
    logging.debug(payload)
    return urlfetch.fetch('https://www.reddit.com/api/comment',
                          payload=payload,
                          method=urlfetch.POST,
                          headers={
                              'User-Agent': USERAGENT,
                              'Cookie': 'reddit_session=%s; Domain=reddit.com; Path=/; HttpOnly' % urllib.quote(session),
                          })
