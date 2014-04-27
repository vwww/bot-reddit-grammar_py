#!/usr/bin/python

import json

from google.appengine.ext import ndb


class ProcessingOffset(ndb.Model):
    last = ndb.StringProperty(required=True, indexed=False)


def getCounter(key=1337):
    item = ProcessingOffset.get_by_id(key)
    if item is None:
        item = ProcessingOffset(id=key, last='')
    return item


class StoredAuth(ndb.Model):
    uh = ndb.StringProperty(required=True, indexed=False)
    s = ndb.StringProperty(required=True, indexed=False)


def getAuthorization():
    item = StoredAuth.get_by_id(1337)
    if item is None:
        return None
    return item.uh, item.s


def setAuthorization(modhash, session):
    item = StoredAuth.get_by_id(1337)
    if item is None:
        item = StoredAuth(id=1337, uh=modhash, s=session)
    else:
        item.uh = modhash
        item.s = session
    item.put()
