# Chisel

Written by [David Zhou][dz] in [python][py], and forked by [ckunte][ck], [Chisel][ch] is an amazing blog engine -- all in just one file.

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

Install these on a Mac via pip -- python package installer:

	$ sudo easy_install pip
	$ Password:
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

While it is not required, keeping `chisel`, `posts`, and `www` is a good idea. It helps keep chisel folders clean (for future updates), aside from keeping the tool separated from the content you create using it (`posts`, and `www`).

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

	$ python chisel.py

## Sample Entry

sample.markdown:

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
[ck]: https://github.com/ckunte
