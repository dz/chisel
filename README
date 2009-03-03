Chisel
David Zhou
==========

USAGE
=====

$ python chisel.py


SAMPLE ENTRY
===========

sample.markdown:
-------# start of file
The First Line Contains the Title
3/2/2009 <-- second line contains date. Must be in this format by default. Change via ENTRY_TIME_FORMAT setting.
<a blank line separate title/date from post body>
This is now the body of the post.  By default, the body is evaluated and parsed with markdown.
Another line

New paragraph

Another paragraph
-------# end of file


ADDING STEPS
============

Use the @step decorator.  The main loop passes in the master file list and jinja environment.


SETTINGS
========

Change these settings:

SOURCE:
Location of source files for entries
Must end in slash.  
Example: SOURCE = "./blog/" 

DESTINATION:
Location to place generated files.
Must end in slash.
Example: DESTINATION = "./explort/"

HOME_SHOW:
Number of entries to show on homepage
Example: HOME_SHOW = 15

TEMPLATE_PATH:
Path to folder where tempaltes live.
Must end in slash.
Example: TEMPLATE_PATH = "./templates/" 

TEMPLATE_OPTIONS:
Dictionary of options to give jinja2.
Default: TEMPLATE_OPTIONS = {}

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
Callable that takes in text and returns formatted
text.
Default: FORMAT = lambda text: markdown.markdown(text, ['footnotes',]) 




