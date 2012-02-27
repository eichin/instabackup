import urllib, urllib2
import os
import json
import datetime

API_KEY = "6e3014faf9dc441b84e69ac0fa94f6fa"
API_SECRET = "737cbfd564c443a08b434b3a91525706"

TOKEN_FILE = os.path.expandvars("$HOME/.instabackup.token")

def main():
    # look for existing token
    try:
        with file(TOKEN_FILE) as f:
            token = f.read().strip()

    except IOError:
        # ok, we don't have a token
        redirect = "http://movieos.org/toys/instabackup/"
        auth = "https://instagram.com/oauth/authorize/?client_id=%s&redirect_uri=%s&response_type=token"%(API_KEY, urllib.quote(redirect))
        print "Open\n\n%s\n\nin a web browser, then paste the token (bit after the # in the landing page) here:"%(auth)

        token = raw_input("--> ")
        with file(TOKEN_FILE, "w") as f:
            f.write(token)


    url = "https://api.instagram.com/v1/users/self/media/recent?access_token=%s"%token
    while url:
        print "fetching page.."
        conn = urllib2.urlopen(url)
        raw = conn.read()
        data = json.loads(raw)

        for photo in data["data"]:
            image = photo["images"]["standard_resolution"]["url"]
            try:
                title = photo["caption"]["text"]
            except (KeyError, TypeError):
                title = "untitled"
            print u"..%s"%title
            dt = datetime.datetime.utcfromtimestamp(float(photo["created_time"]))
            # can't use colons in time because macos gets whiny.
            filename = u"%s %s.jpg"%(dt.strftime("%Y-%m-%dT%H-%M-%S"), title)
            if not os.path.exists(filename):
                u = urllib2.urlopen(image)
                with open(filename, 'w') as f:
                    f.write(u.read())

        try:
            url = data["pagination"]["next_url"]
        except KeyError:
            break

    print "All done!"


if __name__ == "__main__":
    main()
