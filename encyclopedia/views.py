from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms

import markdown 
import random, re

from . import util

#Form for collecting data for new page
class NewEntryForm(forms.Form):
    title = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control col-md-5'}))
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-9 '}))

#Form for editing data for existing page
class EditEntryForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control col-md-9'}))

#displays the homepage
def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

#Display the entry of the page 
def titleSearch(request, title):

    entry = util.get_entry(title)
    if entry:
        return render(request, "encyclopedia/mdlayout.html",{
            "title" : title,
            "content" : markdown.markdown(entry)  
        })
    else:
        return render(request, "encyclopedia/error.html",{
            "content": "Requested Page Not found"
        }) 

#Display any random entry
def random_page(request):
    rand_generator = random.choice(util.list_entries())
    return HttpResponseRedirect(reverse('titleSearch', args = (rand_generator,)))


#search bar for user
def search_bar(request):
    test_list = util.list_entries()
    data = request.GET['q']

    if data in test_list:
        return HttpResponseRedirect(reverse('titleSearch', args = (data,)))
    else:
        res = [x for x in test_list if re.search(data, x)]
        return render(request, "encyclopedia/search.html",{
            "list": res
        })


#Creates a new Entry
def new_entry(request):
    if request.method == "POST":
        form = NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data["title"]
            content = form.cleaned_data["content"]

            if title in util.list_entries():
                return render(request, "encyclopedia/error.html",{
                    "content": "Entry already exists"
                })
            else:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse('titleSearch', args = (title,)))
        else:
            return render(request, "encyclopedia/new_entry.html",{
                "form": form
            })
    return render(request, "encyclopedia/new_entry.html",{
        "form": NewEntryForm
    })
    

#Edit the existing entry
def edit_entry(request, title):
    if request.method == "POST":
        form = EditEntryForm(request.POST)
        if form.is_valid():
            new_data = form.cleaned_data["content"]
            
            util.save_entry(title, new_data)
            return HttpResponseRedirect(reverse('titleSearch', args = (title,)))
    else:
        old_data = util.get_entry(title)
        return render(request, "encyclopedia/edit_entry.html",{
            "form": EditEntryForm(initial={'content': old_data}),
            "title": title
        })