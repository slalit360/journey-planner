from django.http import HttpResponse
from django.shortcuts import render, redirect
from myapi.form import JourneyForm
import json
import requests

def index(request):
    data = []
    login_flag = None
    if request.method == 'GET':
        print("--- GET ---")
        return render(request, "index.html")

    if request.method == "POST":
        print("--- POST ---")
        if request.user.is_authenticated:
            print("USER ID :", request.user.id)
            term_1 = request.POST.dict()['term_1']
            term_2 = request.POST.dict()['term_2']
            fromLocation, toLocation = search_journey(term_1, term_2)
        else :
            login_flag = 'Please Login Again!'

    return render(request, "index.html", {'from': fromLocation, 'to': toLocation })


def search_journey(term_1, term_2):
    journey_list = {}
    url = "https://api.tfl.gov.uk/Journey/JourneyResults/{0}/to/{1}".format(term_1, term_2)
    # response = requests.get("https://api.tfl.gov.uk/Journey/JourneyResults/{0}/to/{1}?date=20191109".format())
    response = requests.get(url)
    print(url)

    if response.status_code == 300:
        journey_list = json.loads(response.text)

        # location from
        fromLocation = []
        fromLocationDisambiguation = journey_list['fromLocationDisambiguation']

        if fromLocationDisambiguation['matchStatus'] == "identified":
            fromLocation.append(term_1)
        else:
            for i in fromLocationDisambiguation['disambiguationOptions']:
                fromLocation.append(i['place']['commonName'])

        print("fromLocation : ", fromLocation)


        # Location to
        toLocation = []
        toLocationDisambiguation = journey_list['toLocationDisambiguation']

        if toLocationDisambiguation['matchStatus'] == "identified":
            toLocation.append(term_1)
        else:
            for i in toLocationDisambiguation['disambiguationOptions']:
                toLocation.append(i['place']['commonName'])

        print("toLocation : ", toLocation)

    else:
        print("--- : ", response.status_code)

    return fromLocation, toLocation


def search(request):
    """
    Autocomplete ajax call
    :param request:
    :return: HttpResponse which consist list of words
    """
    word_count = {}
    if request.is_ajax():
        word_searched = request.GET.get('term').strip().lower()
        matchedWords  = []
        response = requests.get("https://api.tfl.gov.uk/Place/Search?name={0}".format(word_searched))

        if response.status_code == 200:
            place_list = json.loads(response.text)

            for match in place_list:
                matchedWords.append(str(match['commonName']))

        if len(matchedWords) == 0:
            matchedWords.append("-- NO MATCH --")

        data = json.dumps(list(set(matchedWords)))
    else:
        data = ''
    return HttpResponse(data, 'application/json')