#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Chisel
# David Zhou
# 
# Requires:
# jinja2

import sys, re, time, os
import jinja2, markdown
from functools import cmp_to_key

#Settings
SOURCE = "./blog/" #end with slash
DESTINATION = "./export/" #end with slash
HOME_SHOW = 15 #numer of entries to show on homepage
TEMPLATE_PATH = "./templates/"
TEMPLATE_OPTIONS = {}
TEMPLATES = {
    'home': "home.html",
    'detail': "detail.html",
    'archive': "archive.html",
    'rss': "feed.xml",
}
TIME_FORMAT = "%B %d, %Y"
ENTRY_TIME_FORMAT = "%m/%d/%Y"
#FORMAT should be a callable that takes in text
#and returns formatted text
FORMAT = lambda text: markdown.markdown(text, extensions=['markdown.extensions.footnotes'])
#########

STEPS = []

def step(func):
    def wrapper(*args, **kwargs):
        print("\t\tGenerating %s..." %func.__name__, end="");
        func(*args, **kwargs)
        print("done.")
    STEPS.append(wrapper)
    return wrapper

def get_tree(source):
    files = []
    for root, ds, fs in os.walk(source):
        for name in fs:
            if name[0] == ".": continue
            path = os.path.join(root, name)
            f = open(path, "r")
            title = f.readline().strip('\n\t')
            date = time.strptime(f.readline().strip(), ENTRY_TIME_FORMAT)
            year, month, day = date[:3]
            files.append({
                'title': title,
                'epoch': time.mktime(date),
                'content': FORMAT(''.join(f.readlines()[1:])),
                'url': '/'.join([str(year), "%.2d" % month, "%.2d" % day, os.path.splitext(name)[0] + ".html"]),
                'pretty_date': time.strftime(TIME_FORMAT, date),
                'rssdate': time.strftime("%a, %d %b %Y %H:%M:%S %z", date),
                'date': date,
                'year': year,
                'month': month,
                'day': day,
                'filename': name,
            })
            f.close()
    return files

def compare_entries(x, y):
    result = (y['epoch'] > x['epoch']) - (y['epoch'] < x['epoch'])
    if result == 0:
        return (y['filename'] > x['filename']) - (y['filename'] < x['filename'])
    return result

def write_file(url, data):
    path = DESTINATION + url
    dirs = os.path.dirname(path)
    if not os.path.isdir(dirs):
        os.makedirs(dirs)
    file = open(path, "w")
    file.write(data)
    file.close()

@step
def generate_homepage(f, e):
    """Generate homepage"""
    template = e.get_template(TEMPLATES['home'])
    write_file("index.html", template.render(entries=f[:HOME_SHOW]))

@step
def generate_rss(f, e):
    """Generate rss feed"""
    template = e.get_template(TEMPLATES['rss'])
    write_file("rss.xml", template.render(entries=f[:HOME_SHOW]))

@step
def master_archive(f, e):
    """Generate master archive list of all entries"""
    template = e.get_template(TEMPLATES['archive'])
    write_file("archives.html", template.render(entries=f))

@step
def detail_pages(f, e):
    """Generate detail pages of individual posts"""
    template = e.get_template(TEMPLATES['detail'])
    for file in f:
        write_file(file['url'], template.render(entry=file, entries=f))

def main():
    print("Chiseling...");
    print("\tReading files...", end="");
    files = sorted(get_tree(SOURCE), key=cmp_to_key(compare_entries))
    env = jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_PATH), **TEMPLATE_OPTIONS)
    print("done.")
    print("\tRunning steps...");
    for step in STEPS:
        step(files, env)
    print("\tdone.")
    print("done.")

if __name__ == "__main__":
    sys.exit(main())
