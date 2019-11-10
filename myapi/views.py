from django.shortcuts import render, redirect
from myapi.form import JourneyForm


def index(request):
    journey_form = JourneyForm()
    return render(request, "index.html", {'form': JourneyForm})


def search_journey(request):
    if request.method == "POST":
        form = JourneyForm(request.POST)
        if form.is_valid():
            try:
                return redirect('/index', )
            except:
                pass
    else:
        form = JourneyForm()
    return render(request,'index.html',{'form':form})

