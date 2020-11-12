from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from PIL import Image
from PIL.ExifTags import TAGS
from .models import *
from .forms import *
from pymongo import MongoClient
uri = "mongodb://root:root@52.188.19.176:27017/?authSource=admin&authMechanism=SCRAM-SHA-256"
client = MongoClient(uri)
mydb = client["clouddatabase"]
mycol = mydb["imagemetadata"]

def returnimgfrompath(imagenamelist):
    imageslist = ImageSet.objects.all()
    retlist = []
    for name in imagenamelist:
        for img in imageslist:
            print(img.id)
            if str(img.image.path) == name:
                retlist.append(img)
                break
    return retlist

@login_required(login_url='login')
def imgsearchres(request,searchstr):
    querystrlist = searchstr.splitlines()
    isinvalid = False
    isempty = False
    imageslist = []
    if searchstr.count("=") != len(querystrlist):
        isinvalid = True
    else:
        querylist = []
        for st in querystrlist:
            attr, val = st.split('=')
            if attr[-1] == " ":
                attr = attr[:len(attr)-1]
            if val[0] == " ":
                val = val[1:]
            querylist.append({attr:val})
        if(len(querylist) == 1):
            query = querylist[0]
        else:
                query = {"$or":querylist}
        print(query)
        imagequery = mycol.find(query)
        imagequerylist = []
        for i in imagequery:
            imagequerylist.append(i)
        imagenamelist = [i.get("imgpath") for i in imagequerylist]
        imageslist = returnimgfrompath(imagenamelist)
        if len(imageslist)==0:
            isempty=True
        else:
            isempty=False
    context = {'empty' : isempty, 'invalid': isinvalid, 'images' : imageslist}
    return render(request, 'imgsearchres.html', context)

@login_required(login_url='login')
def imgsearch(request):
    if request.method=='POST':
        form = SearchForm(request.POST)
        if form.is_valid():
            text = form.cleaned_data['searchtext']
            url_path = '/imgsearchres/' + str(text)
            return redirect(url_path)
        else:
            context = {'form' : form}
            return render(request, 'imgsearch.html', context)
    else:
        form = SearchForm(request.POST)
        context = {'form' : form}
        return render(request, 'imgsearch.html', context)

@login_required(login_url='login')
def imgupload(request):
    if request.method=='POST':
        form = ImageForm(request.POST,request.FILES)
        if form.is_valid():
            form.save(commit=True)
            return redirect('index')
        else:
            context = {'form' : form}
            return render(request, 'imgupload.html', context)
    else:
        form = ImageForm(request.POST,request.FILES)
        context = {'form' : form}
        return render(request, 'imgupload.html', context)
