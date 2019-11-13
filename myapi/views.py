from django.http import HttpResponse
from django.shortcuts import render, redirect
from proj.settings import API_APP_ID, API_APP_KEY
from myapi.models import FavouritePlan
from django.contrib.auth.decorators import login_required
import json
import requests



@login_required
def index(request):
    data = []
    login_flag = None

    if request.method == 'GET':
        print("--- GET ---")
        return render(request, "index.html")


    if request.method == "POST":
        print("--- POST ---")
        if request.user.is_authenticated:
            print("USER ID :", request.user)
            term_1 = request.POST.dict()['term_1']
            term_2 = request.POST.dict()['term_2']
            fromLocation, toLocation, msg = search_journey(term_1, term_2)
            return render(request, "index.html", {'from': fromLocation, 'to': toLocation, 'msg':msg })
        else :
            login_flag = 'Please Login Again!'

    return render(request, "index.html")

def search(request):
    """
    Autocomplete ajax call
    :param request:
    :return: HttpResponse which consist list of Places
    """

    word_count = {}

    if request.is_ajax():
        word_searched = request.GET.get('term').strip().lower()
        matchedWords  = []

        url = "https://api.tfl.gov.uk/Place/Search?name={0}&app_id={1}&app_key={2}".format(word_searched, API_APP_ID, API_APP_KEY)
        response = requests.get(url=url)

        if response.status_code == 200:
            place_list = json.loads(response.text)

            for match in place_list:
                matchedWords.append(str(match['commonName']))

        if len(matchedWords) == 0:
            matchedWords.append(" NO MATCH FOUND ")

        data = json.dumps(list(set(matchedWords)))
    else:
        data = ''
    return HttpResponse(data, 'application/json')

@login_required
def search_journey(term_1, term_2):
    msg = None
    journey_list = {}
    url = "https://api.tfl.gov.uk/Journey/JourneyResults/{0}/to/{1}?app_id={2}&app_key={3}".format(term_1, term_2, API_APP_ID, API_APP_KEY)
    response = requests.get(url)
    print(url)

    fromLocation = []
    toLocation = []

    if response.status_code in [300,200]:
        journey_list = json.loads(response.text)

        # location from
        fromLocationDisambiguation = journey_list['fromLocationDisambiguation']

        if fromLocationDisambiguation['matchStatus'] == "identified":
            fromLocation.append(term_1)
        else:
            for i in fromLocationDisambiguation['disambiguationOptions']:
                fromLocation.append(i['place']['commonName'])

        print("fromLocation : ", fromLocation)

        # Location to
        toLocationDisambiguation = journey_list['toLocationDisambiguation']

        if toLocationDisambiguation['matchStatus'] == "identified":
            toLocation.append(term_1)
        else:
            for i in toLocationDisambiguation['disambiguationOptions']:
                toLocation.append(i['place']['commonName'])

        print("toLocation : ", toLocation)

    else:
        print("--- : ", response.status_code)
        msg = "disambiguation not found from api! "

    return fromLocation, toLocation, msg

@login_required
def savePlan(request):
    print("--- PLAN POST ---")

    if request.method == "POST":

        if request.user.is_authenticated:
            print("USER ID :", request.user)
            from_radio = request.POST.dict()['fromradio']
            to_radio = request.POST.dict()['toradio']
            print("From : ", from_radio)
            print("To : ", to_radio)

            journey = FavouritePlan()
            journey.from_location = from_radio
            journey.to_location = to_radio
            journey.fav_flag = True
            journey.save()
            print("- Added to fav -- ")

    return render(request, "index.html", {'msg': 'Journey ( '+from_radio+' -> '+to_radio+' ) added to favourite !'})

@login_required
def favView(request):
    print("--- FAV GET ---")
    favList = []
    if request.method == "GET":
        if request.user.is_authenticated:
            print("USER ID :", request.user)
            favSet = FavouritePlan.objects.all()

            for record in favSet:
                favList.append(record)

            print("- Added to fav -- ")

    return render(request, "index.html", {'fav': favList} )

@login_required
def about(request):
    return render(request, "about.html")