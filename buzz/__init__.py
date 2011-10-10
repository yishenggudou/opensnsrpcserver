def pub2sina(status):
    from lib import get_api
    o = get_api()
    o.update_status(status)

def get_sina_status():
    from lib import get_api
    o = get_api()
    print dir(o)
    return o.user_timeline(count=10, page=1)

