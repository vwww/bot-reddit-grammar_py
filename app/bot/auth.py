#!/usr/bin/python

from . import http

import config
import storage

import json
import logging


def authorize():
    req = storage.getAuthorization()
    if req:
    	logging.debug('Reusing old login')
        return req
    # Log in
    req = http.authorize(config.USERNAME, config.PASSWORD)
    # Load data
    logging.debug(req.headers)
    logging.debug(req.content)
    data = json.loads(req.content)['json']['data']
    # Save and return
    storage.setAuthorization(data['modhash'], data['cookie'])
    return data['modhash'], data['cookie']
