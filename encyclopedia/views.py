from django.shortcuts import render,HttpResponse
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, title):
    content = util.get_entry(title)
    if content != None:
        return render(request, "encyclopedia/wiki/entry.html", {
            "title": title,
            "content": content
        })
    else:
        return render(request, "encyclopedia/wiki/error.html")