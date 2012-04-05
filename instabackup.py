import urllib, urllib2
import os
import json
import datetime
import sys

API_KEY = "6e3014faf9dc441b84e69ac0fa94f6fa"
API_SECRET = "737cbfd564c443a08b434b3a91525706"

TOKEN_FILE = os.path.expandvars("$HOME/.instabackup.token")
one_image_template = file(os.path.join(sys.path[0], "instabackup_one_image.html")).read()
collection_template = file(os.path.join(sys.path[0], "instabackup_collection.html")).read()
collection_once_template = file(os.path.join(sys.path[0], "instabackup_collection_once.html")).read()

def batch_page_name(idx):
    "name the index pages"
    if idx < 0:
        return None # let the template drop the backlink
    if idx == 0:
        return "index.html"
    # could be more clever, "next" or "month" or something...
    return "index_%s.html" % idx

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
    index_page_offset = 0
    
    while url:
        print "fetching page.."
        try:
            raw = file(".debug.dump").read()
        except:
            conn = urllib2.urlopen(url)
            raw = conn.read()
            # debug only - cache the json instead of hitting the site each cycle
            #file(".debug.dump", "w").write(raw)

        data = json.loads(raw)
        pagelist = []

        for photo in data["data"]:
            image = photo["images"]["standard_resolution"]["url"]
            # grab 'thumbnail' and 'low_resolution' too?
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
            data_filename = u"%s %s.json"%(dt.strftime("%Y-%m-%dT%H-%M-%S"), title)
            if not os.path.exists(data_filename):
                # TODO: since we don't have to fetch this, always write it?
                #   (does the upstream data ever change anyway?)
                with open(data_filename, 'w') as f:
                    json.dump(photo, f)
            html_filename = (u"%s %s.html"%(dt.strftime("%Y-%m-%dT%H-%M-%S"), title)).replace(" ", "-")
            with open(html_filename, 'w') as f:
                print >> f, one_image_template.format(img=filename, **photo)
            pagelist.append(dict(html_filename=html_filename, **photo))

        index_filename = batch_page_name(index_page_offset)
        with open(index_filename, "w") as f:
            print pagelist
            print >> f, collection_template.format(prev_page=batch_page_name(index_page_offset-1),
                                                   next_page=batch_page_name(index_page_offset+1),
                                                   pagelist="\n".join([collection_once_template.format(**page)
                                                                       for page in pagelist]),
                                                   **data)
        # TODO: *get* a next_url and figure out what the page thing looks like...
        try:
            url = data["pagination"]["next_url"]
            print "NEXT:", url
        except KeyError:
            break

    print "All done!"


if __name__ == "__main__":
    main()
