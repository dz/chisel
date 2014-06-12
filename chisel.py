#!/usr/bin/env python
# encoding: utf-8
# Chisel
# David Zhou, github.com/dz
# Chyetanya Kunte, github.com/ckunte
try:
    import sys, os, re, time, jinja2, markdown, mdx_smartypants, PyRSS2Gen, datetime
except ImportError as error:
    print 'ImportError:', str(error)
    exit(1)

# BEGIN SETTINGS
BASEURL = "http://ckunte.net/log/" #trailing slash
SOURCE = "../posts/" #trailing slash
DESTINATION = "../www/" #trailing slah
TEMPLATE_PATH = "./templates/" #trailing slash
HOME_SHOW = 3 # number of entries to show on homepage
URLEXT = "" # for clean urls (else use: ".html")
# Date formats
TIME_FORMAT = "%B %-d, %Y" # shown on post entries
STIME_FORMAT = "%b %d" # shown on the archive page
ENTRY_TIME_FORMAT = "%m/%d/%Y" # to be input on the second line of post in markdown
# RSS details
RSS = PyRSS2Gen.RSS2(
    title = "Chyetanya Kunte", # Blog title
    description = "ckunte.net/log.", # Blog description
    link = BASEURL + "rss.xml", 
    lastBuildDate = datetime.datetime.now(),
    items = [])

# END SETTINGS
#
TEMPLATE_OPTIONS = {}
#
FORMAT = lambda text: markdown.markdown(text, ['smartypants','footnotes'])
#
if URLEXT == ".html":
    PATHEXT = ""
    pass
if URLEXT == "":
    PATHEXT = ".html"
    pass

STEPS = []

def step(func):
    def wrapper(*args, **kwargs):
        print "Starting " + func.__name__ + "...",
        func(*args, **kwargs)
        print "Done."
    STEPS.append(wrapper)
    return wrapper

def get_tree(source):
    files = []
    for root, ds, fs in os.walk(source):
        for name in fs:
            if name[0] == ".": continue
            if not re.match(r'^.+\.(md|mdown|markdown)$', name): continue
            path = os.path.join(root, name)
            with open(path, "rU") as f:
                title = f.readline().decode('UTF-8')[:-1].strip('\n\t')
                date = time.strptime(f.readline().strip(), ENTRY_TIME_FORMAT)
                year, month, day = date[:3]
                content = FORMAT(''.join(f.readlines()[1:]).decode('UTF-8'))
                url = '/'.join([str(year), os.path.splitext(name)[0] + URLEXT])
                files.append({
                    'title': title,
                    'epoch': time.mktime(date),
                    'content': content,
                    'url': url,
                    'pretty_date': time.strftime(TIME_FORMAT, date),
    				'sdate': time.strftime(STIME_FORMAT, date),
                    'date': date,
                    'year': year,
                    'month': month,
                    'day': day,
                    'filename': name})
    return files

def write_file(url, data):
    path = DESTINATION + url + PATHEXT
    dirs = os.path.dirname(path)
    if not os.path.isdir(dirs): os.makedirs(dirs)
    with open(path, "w") as file:
        file.write(data.encode('UTF-8'))

def write_feed(url, data):
    path = DESTINATION + url
    with open(path, "w") as file:
        file.write(data.encode('UTF-8'))

@step
def gen_rss(f, e):
    for file in f[:3]:
        RSS.items.append(PyRSS2Gen.RSSItem(title=file['title'], link=BASEURL + file['url'], description=file['content'], author="Chyetanya Kunte", guid = PyRSS2Gen.Guid(BASEURL + file['url']), pubDate=datetime.datetime(file['year'], file['month'], file['day'])))
    RSS.write_xml(open(DESTINATION + "rss.xml", "w"))

@step
def gen_home(f, e):
    write_file('index' + URLEXT, e.get_template('home.html').render(entries=f[:HOME_SHOW]))

@step
def gen_detailpages(f, e):
    for file in f:
        write_file(file['url'], e.get_template('detail.html').render(entry=file))    

@step
def gen_archive(f, e):
    write_file('archive' + URLEXT, e.get_template('archive.html').render(entries=f))

def main():
    print "Chiseling..."
    print "\tReading files...",
    files = sorted(get_tree(SOURCE), key=lambda entry: entry['epoch'], reverse=True)
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), **TEMPLATE_OPTIONS)
    print "Done."
    print "\tRunning steps..."
    for step in STEPS:
        print "\t\t",
        step(files, env)
    print "\tDone."
    print "Done."

if __name__ == "__main__":
    sys.exit(main())