def http_auth(endpoint):
    def wrap(*args, **kwargs):
        print 'Calling function %s' % endpoint.__name__
        r = endpoint(*args, **kwargs)
        print ('Call finished')
        return r
    return wrap
