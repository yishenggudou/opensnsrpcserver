def pub2qq(status):
    from lib import get_api
    o = get_api()
    o.tweet.add(status)

if __name__ == "__main__":
    pub2qq(u'tt....test')
