# Chisel

Written by [David Zhou][dz] in [python][py], forked and enhanced by [Chyetanya Kunte][ck], [Chisel][ch] is an amazing blog engine -- all in just one file.

This fork includes the following additions and enhancements:

- Smartypants content parsing to emit typographically nicer quotes, proper em and en dashes, etc.
- A shorter (just year based) permalink structure.
- RSS feed generator script (Hat-tip: [Ronan Jouchet][rj]).
- Support for [title-less posts][tl] (like for links and quotes).
- Support for Page titles in title tag for permalinks added in templates.
- Supports [clean URLs][cu].
- Send pings to various search engines to let them know that your blog has been updated via the lovely [Pingomatic][p].

## Screenshot

- [Screenshot][scr].
- [Live site example][log].

### What it does not do

Chisel keeps it simple and stupid. And so, there is

- No taxonomy support, i.e., no categories, and no tags.
- No built-in search. (When you carry an entire copy of your site on your hard drive, I think you don't need one; use grep, Spotlight or find instead. If you are inclined to create a search, go ahead and do it. It isn't too complicated. Just like populating the RSS feed file or the Archive file, it is possible to update an index for new posts in a JSON enclosure, and query it.)

### What it does best

- No loss of fidelity. All your posts would be plain text, which kind of makes it timeless. Great for archiving. Burn on a CD, or save it on a USB stick.
- You can regenerate your entire site again if you just have native markdown draft posts, and Chisel + templates.
- It's incredibly lightweight -- less than 8kB! (Compare that with anything out there, and they all seem like they weigh a ton, not to mention the complexity of install, maintain, and backup.)
- Zero security issues. Generate site locally, and upload only the thus created html files out of markdown post drafts. 
- Pure static site. Pretty robust to network spikes, and heavy loads. No server-side scripting ensures no overload.
- Helps you blog offline, run your own private blog, information system, if you don't want to host it on the web, and still have a web like interface.
- Written in python: Simple to understand, simple to modify, but most of all, simpler to use. (Knowledge of python is not required, except for installation, which is explained in detail below.)

## How it works

1. Write your post in Markdown, save it as `post-title.markdown` in a designated folder, say, `posts`. 

2. Run `python chisel.py` in a Terminal, and Chisel parses all `.markdown` files in `posts` folder to another designated folder, say `www` in html -- ready to be served using a webserver.

3. Sync [See Note] all files and folders from the local `www` folder to the root of your webhost, and you've got a fully functioning website.

(Note: There are a number of ways one can sync files, [git][], [rsync][], or plain vanilla (s)[ftp][]. The sync can be further automated using a (ana)cron job, or via the Automator.)

## Requirements

If you are using a Mac or Linux, then python comes pre-installed. In addition, you'll need just a few python packages for Chisel to function. They are as follow:

1. [Jinja2][ji] is a templating engine, developed by [Pocoo Team][pt].
2. [Markdown][md] is a text markup language, developed by [John Gruber][jg]. It's nearly plain text, i.e., zero learning curve, which is why it's awesome.
3. [Smartypants][sp] is a typographical enhancer, also by [John Gruber][jg].
4. [PyRSS2Gen][p2] is a library for generating RSS feeds.

#### Install these on a [Mac OS X][m] via [pip][] -- python package installer:

	$ sudo easy_install pip
	Password:
	$ sudo pip install jinja2 markdown mdx_smartypants PyRSS2Gen
	
#### On [Ubuntu][u] (Debian) linux:

	$ sudo apt-get install python-pip
	Password:
	$ sudo pip install jinja2 markdown mdx_smartypants PyRSS2Gen

## Create a site structure on your computer (This is just an example)

	$ mkdir ~/site
	$ cd ~/site
	$ mkdir posts www chisel

Now download Chisel as a zip file or via git (`git clone git://github.com/ckunte/chisel.git`). Move the unzipped contents into `chisel` folder created above. The structure should look like this following:

	~/site/
	~/site/posts/
	~/site/www/
	~/site/chisel/
				 /README.markdown
				 /chisel.py
				 /templates/
				 		   /archive.html
						   /base.html
						   /detail.html
						   /home.html

While it is not required, keeping `chisel`, `posts`, and `www` separate is a good idea. It helps keep chisel folders clean (for future updates), aside from keeping the tool separated from the content you create using it (`posts`, and `www`).

Remember to open and edit templates, particularly `base.html` as it contains site name, description and other `meta` into in the `<head>` section hard-coded. In addition, you will need to update the settings below.

### Updating Settings to suit

Open `chisel.py` in a text editor and have a look at the section Settings. You may need to update the following:

	# Settings
	BASEURL = "http://yoursite.com/" # Must end with a trailing slash.
	SOURCE = "../posts/"             # Must end with a trailing slash.
	DESTINATION = "../www/"          # Must end with a trailing slash.
	HOME_SHOW = 15                   # Number of entries to show on homepage.
	TEMPLATE_PATH = "./templates/"	 # Path of Jinja2 template files.
	TEMPLATES = {
    	'home': "home.html",
    	'detail': "detail.html",
    	'archive': "archive.html",
	}
	TIME_FORMAT = "%b %d, %Y"
	ENTRY_TIME_FORMAT = "%m/%d/%Y"
	FORMAT = lambda text: markdown.markdown(text, ['footnotes','smartypants',])
	RSS = PyRSS2Gen.RSS2(
	    title = "My Blog Title",
	    link = BASEURL + "feed.xml",
	    description = "My Tagline or Blog Description",
	    lastBuildDate = datetime.datetime.now(),
	    items = [])

## Usage

	$ cd ~/site/chisel
	$ python chisel.py

## Sample Entry

`sample.markdown` (Note: Filenames shall not have spaces. Good examples: `hotel-california.markdown`, `i_love_cooking.markdown`, and so on):

	Title of the post
	3/14/1879

	Content in Markdown here onward.

	Next paragraph.

	Next paragraph.

The very simple post entry format, shown above, is as follows:

- Line 1: Enter a Title.
- Line 2: Enter date in m/d/Y format.
- Line 3: Blank line.
- Line 4: Content in Markdown here onward.

### Also want daringfireball.net like posts (for quotes, and links) without titles?

Pretty easy. Leave the first line blank in the above entry format. Jinja2 template (see `templates/detail.html`) below looks for a post title, and does not produce one, if it finds none. (The permalink URL is dependent on filename -- not the post title.)

	{% if entry.title != '' %}
		<h2>{{ entry.title }}</h2>
	{% endif %}
	{{ entry.content }}

### Adding Steps

Use the @step decorator. The main loop passes in the master file list and jinja environment.

	TEMPLATES:
	Dictionary of templates.  
	Required keys: 'home', 'detail', 'archive'.
	Example: 
	        TEMPLATES = {
	            'home': "home.html",
	            'detail': "detail.html",
	            'archive': "archive.html",
	        }

	TIME_FORMAT:
	Format of human readable timestamp.
	Default: "%B %d, %Y - %I:%M %p"

	ENTRY_TIME_FORMAT:
	Format of date declaration in second line of posts
	Default: "%m/%d/%Y"

	FORMAT:
	Callable that takes in text and returns formatted text (without Smartypants). 
	Default: FORMAT = lambda text: markdown.markdown(text, ['footnotes',]) 

Here's an example of a @step decorator added to chisel.py to generate a colophon page:

First add the following to TEMPLATES list above:

	            'colophon': "colophon.html",	

Then, add this below in chisel.py code:

	@step
	def generate_colophon(f, e):
	    """Generate an about page"""
	    template = e.get_template(TEMPLATES['colophon'])
	    write_file("colophon.html", template.render(entries=f))


## Can I use this to run a site locally, like offline?

Yes! Just navigate to `~/site/www` and run the following to start a simple HTTP server in Terminal:

	$ python -m SimpleHTTPServer

Then, point your browser to: `http://localhost:8000` and your site is live on your computer.

## I have a large number of posts in WordPress. How do I convert?

Have a look at Thomas Frössman's tool, [exitwp][ep]. While it's written primarily for Jekyll, it does a very good job of converting all WordPress posts to Markdown post -- one file per post. Each post thus converted shows some preformatted lines in the beginning. much of which you don't need in Chisel (You only require Title and Date in the format illustrated above.) You could either manually edit each markdown file, or you could fork Thomas's exitwp and change the following lines (between line 253 and 259) from

	yaml_header = {
          'title': i['title'],
          'date': i['date'],
          'slug': i['slug'],
          'status': i['status'],
          'wordpress_id': i['wp_id'],
        }

to

       yaml_header = {
          i['title'],
          i['date'],
        }

Further, the date would need a fix to read as m/d/Y. But at least for now, it reduces your edits to just changing dates. Or you could write a [shell script][ss] to chuck out needless information generated for Jekyll to suit Chisel.

## I miss pinging my site via [Pingomatic][p]. How do I?

Put the following script (hat-tip: [Ned Batchelder][nb] for this lovely script) in a file, say `ping.py`, and run `python ping.py` (please do remember to change the title and URL in the script below):

	import xmlrpclib

	remoteServer = xmlrpclib.Server("http://rpc.pingomatic.com/RPC2")
	ret = remoteServer.weblogUpdates.ping(
	    "Title of your blog",
	    "http://yourblogurl.com"
	    )
	print ret['message']

## My blog is now powered by Chisel. How do I automate all this?

Easy. Put this in a script (say, `log.sh`, for example) like the example below (do take note of folders, these are from my set-up, if yours is setup differently, then do make those changes in lines 3, 5, and 10 below):

	#!/usr/bin/env sh
	echo ""
	cd ~/Sites/chisel
	python chisel.py
	cd ~/Sites/ckunte.github.com
	echo "Updating log.."
	git add -A
	git commit -m 'Updating log.'
	git push -u origin master
	cd ~/Sites/chisel
	echo "Pinging Pingomatic.."
	python ping.py
	cd ~/
	echo ""
	echo "All done."

When you're ready to generate and post it to your site, run `sh log.sh`, and your post(s) are published.

[ss]: http://www.cyberciti.biz/faq/unix-linux-replace-string-words-in-many-files/
[ep]: https://github.com/thomasf/exitwp
[dz]: https://github.com/dz
[ch]: https://github.com/ckunte/chisel
[ftp]: http://panic.com/transmit/
[py]: http://www.python.org/
[ji]: http://jinja.pocoo.org/docs/
[md]: http://daringfireball.net/projects/markdown/
[sp]: http://daringfireball.net/projects/smartypants/
[pt]: http://www.pocoo.org/ "Led by Georg Brandl and Armin Ronacher."
[jg]: http://daringfireball.net/ "John Gruber"
[p2]: http://pypi.python.org/pypi/PyRSS2Gen
[ck]: http://log.ckunte.net/2012/chisel "Tinkering Chisel"
[rsync]: http://en.wikipedia.org/wiki/Rsync
[git]: http://git-scm.com
[rj]: https://github.com/ronjouch
[tl]: https://github.com/ckunte/chisel/blob/master/README.markdown#also-want-daringfireballnet-like-posts-for-quotes-and-links-without-titles
[u]: http://www.ubuntu.com/
[m]: http://www.apple.com/macosx
[pip]: http://pypi.python.org/pypi/pip
[scr]: http://ckunte.net/images/chisel.png
[log]: http://ckunte.net/
[cu]: http://ckunte.net/2012/rewrite
[nb]: http://nedbatchelder.com/blog/200406/pingomatic_and_xmlrpc.html "Ping-o-matic and xml-rpc"
[p]: http://pingomatic.com/
