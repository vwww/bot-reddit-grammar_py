#!/usr/bin/python

from .http import getNew
from .auth import authorize
from .wording import MakeWording

from .config import subreddit
import storage

import json
import logging
from google.appengine.api import taskqueue


uh = ''
session = ''


def startup():
    global uh, session
    uh, session = authorize()


def do(simulate=False):
    # Get previous offest
    count = storage.getCounter()
    # Fetch new links
    resp = getNew(count.last, subreddit)

    # Check if there are links
    links = json.loads(resp.content)['data']['children']
    if not links:
        logging.debug('No links to parse!')
        return

    logging.debug('Processing %d links' % (len(links)))

    # Update the offset
    count.last = links[0]['data']['name']
    count.put()

    skipped = []

    # Process new links
    for link in links:
        l = link['data']
        # Ensure correct subreddit
        if l['subreddit'] != subreddit:
            skipped.append(l['title'])
            continue
        # Try to correct the user
        corrected = MakeWording(l['title'], l['selftext'], l['author'])
        if corrected:
            if simulate:
                logging.info(corrected)
            else:
                logging.warning('Deferred %s' % (corrected))
                taskqueue.add(url='/do/post', params={
                    'parent': l['name'],
                    'text': corrected,
                })
        else:
            skipped.append(l['title'])

    # Log skipped links
    if skipped:
        logging.debug('[Skipped %d] %s' % (len(skipped), skipped))


def comment(parent, text):
    req = http.postComment(parent, text, uh, session)
    logging.debug(req.status_code)
    logging.debug(req.headers)
    logging.debug(req.content)
