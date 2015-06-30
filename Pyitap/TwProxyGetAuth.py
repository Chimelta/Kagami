import tweepy
import configparser
import http.cookiejar
import urllib.request
import urllib.parse
import re


def get_auth(url: str, username: str, password: str):
    """
    :rtype: str
    """
    cookiejar = http.cookiejar.CookieJar()
    opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
    res = opener.open(url)
    resstr = str(res.read(), encoding='utf-8')
    at_pattern = re.compile('name="authenticity_token" type="hidden" value="(.*?)">')
    at_match = at_pattern.findall(resstr)
    at = at_match[0]
    ot_pattern = re.compile('name="oauth_token" type="hidden" value="(.*?)">')
    ot_match = ot_pattern.findall(resstr)
    ot = ot_match[0]
    data = urllib.parse.urlencode({
        'authenticity_token': at,
        'redirect_after_login': url,
        'oauth_token': ot,
        'session[username_or_email]': username,
        'session[password]': password,
    }).encode('utf-8')
    login_res = opener.open('https://api.twitter.com/oauth/authorize', data)
    login_res_str = str(login_res.read(), encoding='utf-8')
    pin_pattern = re.compile('<kbd aria-labelledby="code-desc"><code>(\d*?)</code></kbd>')
    pin_match = pin_pattern.findall(login_res_str)
    try:
        return pin_match[0]
    except:
        raise


def init_oauth(username: str, password: str, consumer_key: str, consumer_secret: str):
    """
    :return: access_token, access_token_secret
    :rtype: tuple
    """

    config = configparser.ConfigParser()
    config.read('config.ini', encoding='utf-8')
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    try:
        pin = get_auth(auth.get_authorization_url(), username, password)
    except:
        raise
    auth.get_access_token(pin)
    print('Auth succeeded')
    return auth.access_token, auth.access_token_secret
