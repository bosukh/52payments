from google.appengine.api import memcache

def mc_upsert(key, value):
    '''
    Given a key/value pair, update or insert into memcache
    '''
    if not key or not value:
        return False
    dat = memcache.get(key)
    if dat:
        memcache.replace(key, value)
    else:
        memcache.add(key, value)
    return True

def mc_getsert(key, func):
    '''
    Given key/func pair,
    If value is there for the key, return the value
    else, run func(usually a query) and insert to memcache and return the value
    '''
    if not key:
        return False
    dat = memcache.get(key)
    if not dat:
        value = func()
        memcache.add(key, value)
    return value
