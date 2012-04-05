## Fork notes

instabackup just grabs the .jpg and stuffs the caption in the filename; great minimal first start, but I want a little more than that.  Current additions:

  * basic image page
  * basic (first-page only, I only have four pictures so far) index page with links
  * uses python str.format() - should upgrade to jinja2 or something that has loops :-)
  * stashes all of the metadata in a .json "next to" the .jpg, for easier (later) reprocessing with new templates

Next steps:  for now, actually see if I use instagram enough to polish the templates, and maybe split backup from rebuild-formatting.  (The Android instagram app is amazingly tedious to actually use - a dozen clicks to get a picture uploaded, and that's assuming you don't dither over filters?  I'm guessing the iphone app isn't like that, or it would never have gotten popular :)

## Original README

instabackup is a quick hack to back up your instagram stream. I put it together in 20 mins. It's raw. I don't care.

Run it, and it'll download all the photos from yuor instagram feed into the current directory, named with the upload date and title. It won't re-download files that already exist, so you can safely run it nightly and just download new photos if you want to do that.

The first time you run it, it'll need authentication. OAuth2 doesn't seem to have a pure desktop flow, so you'll end up on a page on movieos.org that will give you a token to cut and paste back to the command line. Not the best of solutions, but it'll do. It'll cache the token in a file called `.instabackup.token` in your home directory, and subsequent runs won't need authenticating.

I think that's it. Tell me (tom@movieos.org) if it breaks.


## TODO list (that probably won't get done)

* Write out a local HTML file that embeds the images and has comments / tags, so you get a pretty HTML file like the Tumblr backup tool provides.

* Write out the full backed up metadata as JSON or something so in extremis you can recover everything about a file.

* Take the file output directory as a command-line param so things don't just get spewed into the current directory.

* It's probably got unicode bugs in it. Everything always does.


## Flickr support

The vague long-term aim of this tool was a bulk-import-into-flickr-from-instagram-history tool. Maybe I want to do this. It should do tags and comments and things, and properly set the taken-date, and all that stuff. Not sure if I really care enough about that, though. It's enoguh to just have an automatable backup tool.


