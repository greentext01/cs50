import markdown2

from django.shortcuts import redirect, render
from django import forms
from django.urls import reverse

from . import util
from random import choice

class NewForm(forms.Form):
    title = forms.CharField(label="Title")
    body = forms.CharField(widget=forms.Textarea, label="")

class EditForm(forms.Form):
    body = forms.CharField(widget=forms.Textarea, label="")

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry(request, entry):
    # 
    if util.get_entry(entry) == None:
        return render(request, "encyclopedia/error.html", {
            "status": 404,
            "message": "Entry not found"
        }, status=404)

    return render(request, "encyclopedia/entry.html", {
        "title": entry,
        "body": markdown2.markdown(util.get_entry(entry))
    })

def search(request):
    if util.get_entry(request.GET['q']) == None:
        print(util.search_entries(request.GET['q']))
        return render(request, "encyclopedia/search.html", {
            "results": util.search_entries(request.GET['q'])
        })
    else:
        return redirect("/wiki/" + request.GET['q'])

def new(request):
    if request.method == 'GET':
        return render(request, "encyclopedia/new.html", {
            "form": NewForm()
        })
    elif request.method == 'POST':
        form = NewForm(request.POST)
        if form.is_valid():
            if not util.get_entry(form.cleaned_data["title"]):
                util.save_entry(
                    form.cleaned_data["title"], form.cleaned_data["body"])
            else:
                return render(request, "encyclopedia/error.html", {
                    "status": 400,
                    "message": "Entry already exists"
                }, status=400)
            return redirect(f"/wiki/{form.cleaned_data['title']}")

def edit(request, entry):
    print(util.get_entry(entry))
    if request.method == 'GET':
        if util.get_entry(entry):
            return render(request, "encyclopedia/edit.html", {
                "title": entry,
                "form": EditForm({
                    "body": util.get_entry(entry)
                })
            })
        else:
            return render(request, "encyclopedia/error.html", {
                "status": 404,
                "message": "Entry not found"
            })
    elif request.method == 'POST':
        form = EditForm(request.POST)
        if form.is_valid():
            util.save_entry(entry, form.cleaned_data['body'].replace('\r\n', '\n'))
            return redirect(reverse('wiki', args=[entry]))

        else:
            return render(request, "encyclopedia/error.html", {
                "status": 400,
                "message": "Invalid form"
            })

def random(request):
    return redirect("wiki", entry=choice(util.list_entries()))
