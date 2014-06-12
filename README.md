# Chisel

Written by [David Zhou][dz], Chisel is a a simple static blog generation utility written in [python][py].

This fork by [ckunte][c] includes the following additions:

- RSS feed generator script using PyRSS2Gen (Hat tip: @ronjouch)
- A shorter year based permalink structure.
- Added an option for clean URLs.
- Smartypants content parsing.
- Removed redundant code.
- Simplified step template definitions.
- Additional shorter date formats included for archive listing.

## How it works

1. Write the post in Markdown, save it as `post-title.md` or `posttitle.md` (or post_title.md) in a designated folder, say, `posts`. 
2. Run `python chisel.py` in a Terminal, and Chisel will parse all `.md`, `.markdown` or `.mdown` files in `posts` folder to another designated folder, say `www` in html -- ready to be served using a web server.
3. Sync [See Note] all files and folders from the local `www` folder to the root of your web host, and you've got a fully functioning web site.

(Note: There are a number of ways one can sync files, [git][], [rsync][], or plain vanilla (s)[ftp][]. The sync can be further automated using a (ana)cron job, or via the Automator.)

## Requirements

If you are using a Mac or Linux, then python comes pre-installed. In addition, you'll need just a few python packages for Chisel to function. They are as follow:

1. [Jinja2][ji] is a templating engine, developed by [Pocoo Team][pt].
2. [Markdown][md] is a text markup language, developed by [John Gruber][jg].
3. [Smartypants][sp] is a typographical enhancer, also by [John Gruber][jg].
4. [PyRSS2Gen][p2] is a library for generating RSS 2.0 feeds, by [Andew Dalke][ad], et al.

#### Install these on a [Mac OS X][m] via [pip][] -- python package installer:

    $ sudo easy_install pip
    Password:
    $ sudo pip install jinja2 markdown mdx_smartypants PyRSS2Gen
    
#### On [Ubuntu][u] (Debian) linux:

    $ sudo apt-get install python-pip
    Password:
    $ sudo pip install jinja2 markdown mdx_smartypants PyRSS2Gen

To update these packages, you may run the following:

    $ sudo pip install --upgrade jinja2 markdown mdx_smartypants PyRSS2Gen

## Create a site structure on your computer (This is just an example)

    $ mkdir ~/site
    $ cd ~/site
    $ mkdir posts www chisel

Now download Chisel as a zip file or via git (`git clone git://github.com/ckunte/chisel.git`). Move the unzipped contents into `chisel` folder created above. The structure should look like this following:

    ~/site/
    ~/site/posts/
    ~/site/www/
    ~/site/chisel/
                 /README.md
                 /chisel.py
                 /templates/
                           /archive.html
                           /base.html
                           /detail.html
                           /home.html

While it is not required, keeping `chisel`, `posts`, and `www` separate is a good idea. It helps keep chisel folders clean (for future updates), aside from keeping the tool separated from the content you create using it (`posts`, and `www`).

Remember to open and edit templates, particularly `base.html` as it contains site name, description and other `meta` into in the `<head>` section hard-coded. In addition, you will need to update the settings below.

### Updating Settings to suit

Open `chisel.py` in a text editor and have a look at the Settings section, and update your preferences.

### Usage

    $ cd ~/site/chisel
    $ python chisel.py

### Sample Entry

`sample.md` (Note: Filenames shall not have spaces. Good examples: `hotel-california.md`, `i_love_cooking.md`, and so on):

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

Use the @step decorator. The main loop passes in the master file list and jinja environment. Here's an example of a @step decorator added to chisel.py to generate a colophon page:

Add this below in chisel.py code -- to create a separate standalone page, say, colophon (requires a jinja template called colophon.html within `templates` folder):

    @step
    def gen_colophon(f, e):
        write_file('colophon' + URLEXT, e.get_template('colophon.html').render(entry=file))

### Clean URLs - Howto

GitHub (via nginx rewrite I think) recognizes post files ending with `.html` or feed URLs ending with `.xml`. So, generate the files with these extensions as usual, but tell chisel to skip the extensions in permalinks using settings.

The default setting in chisel now -- assuming server recognizes `.html` extension but does not require its inclusion when referring to a URL -- is as follows:

    URLEXT = ""
    
This above is what I use. (Note that you should not set both to empty or `.html` strings in the above; this would lead to unintended results.)

The fallback option is as follows:

    URLEXT = ".html"

This above setting would be suitable if your server does not recognize `.html` files if they are referred to without `.html` extension in URLs.

### I have a large number of posts in WordPress. How do I convert?

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

Further, the date would need a fix to read as m/d/Y, or change it in Settings sections in `chisel.py` to suit date format.

[ep]: https://github.com/thomasf/exitwp
[dz]: https://github.com/dz
[ch]: https://github.com/ckunte/chisel
[py]: http://www.python.org/
[ji]: http://jinja.pocoo.org/docs/
[md]: http://daringfireball.net/projects/markdown/
[sp]: http://daringfireball.net/projects/smartypants/
[ad]: http://www.dalkescientific.com
[pt]: http://www.pocoo.org/ "Led by Georg Brandl and Armin Ronacher."
[jg]: http://daringfireball.net/ "John Gruber"
[p2]: http://pypi.python.org/pypi/PyRSS2Gen
[git]: http://git-scm.com
[rj]: https://github.com/ronjouch
[u]: http://www.ubuntu.com/
[m]: http://www.apple.com/macosx
[pip]: http://pypi.python.org/pypi/pip
[mj]: http://www.mathjax.org/
[tx]: http://en.wikipedia.org/wiki/LaTeX
[c]: https://github.com/ckunte