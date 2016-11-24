from google.appengine.api import memcache


def mc_upsert(key, data):
    if not key or not data:
        return False
    dat = memcache.get(key)
    if dat:
        memcache.replace(key, data)
    else:
        memcache.add(key, data)
    return True

def mc_getsert(key, func):
    if not key:
        return False
    dat = memcache.get(key)
    if dat:
        return dat
    else:
        data = func()
        memcache.add(key, data)
        return data
