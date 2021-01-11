from django.shortcuts import render, HttpResponse, redirect, HttpResponseRedirect
from . import util
from random import choice
from markdown2 import Markdown
import re

markdowner = Markdown()

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)
    if content != None:
        return render(request, "encyclopedia/wiki/entry.html", {
            "title": title,
            "content": markdowner.convert(content)
        })
    else:
        return render(request, "encyclopedia/wiki/error.html")


def search(request):
    query = request.GET['q']
    queryLower = query.lower()
    entries = util.list_entries()
    exists = False
    for entry in entries:
        entryLower = entry.lower()
        if(entryLower == queryLower):
            exists = True
            title = entry
    if exists:
        content = util.get_entry(query)
        return HttpResponseRedirect("/wiki/" + title)
    else:
        results = []
        for entry in entries:
            entryLower = entry.lower()
            if queryLower in entryLower:
                results.append(entry)
        return render(request, "encyclopedia/wiki/search/results.html",
                  {
                      "results": results
                  })

def new(request):
    return render(request, "encyclopedia/wiki/new.html")

def create(request):
    title = request.POST['title']
    content = request.POST['content']
    exists = False
    titleLower = title.lower()
    entries = util.list_entries()
    for entry in entries:
        entryLower = entry.lower()
        if(entryLower == titleLower):
            exists = True
    if exists:
        return render(request, "encyclopedia/wiki/new.html", {
            "validation": True,
            "title": title,
            "content": content
        })
    else:
        util.save_entry(title, content)
        return render(request, "encyclopedia/wiki/entry.html", {
            "title": title,
            "content": content
        })

def editor(request, title):
    oldContent = util.get_entry(title)
    newContent = request.POST.get("ncontent", False)
    if newContent:
        saveContent = newContent.replace('\r', '')
        util.save_entry(title, saveContent)
        return HttpResponseRedirect("/wiki/"+title)
    elif oldContent:
        return render(request, "encyclopedia/wiki/editor.html", {
            "title": title,
            "content": oldContent
        })
    else:
        return HttpResponse("this entry does not exist")

def random(request):
    entries = util.list_entries()
    title = choice(entries)
    return HttpResponseRedirect("/wiki/"+title)
