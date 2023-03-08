import time  # The time module comes with Python, so no need to install
import wikipedia

from geopy.geocoders import Nominatim


#
# geocode(place)
#
# Parameters:
#
# * place: A string that denotes the name of a place, or an address (e.g.,
#          "University of Washington" or "1410 NE Campus Parkway, Seattle,
#          WA 98195") for which the latitude and longitude should be returned.
#
# Returns
#
# geocode(place) should return the latitude-longitude pair for place as a
# Python tuple, or None if no results are found.
# 
#
# Define your function here
def geocode(place):
    geolocator = Nominatim(user_agent="Learning Python")
    try:
        location = geolocator.geocode(place)
        return location.latitude, location.longitude
    except AttributeError:
        return None


#
# wikipedia_locationsearch(place, max_results=10, radius=2.0, sort=False)
#
# Parameters
# 
# * place: A string that denotes the name of a place, or an address (e.g., 
#          "University of Washington" or "1410 NE Campus Parkway, Seattle, WA 
#          98195") around which the search results should be returned.
# * max_results: An integer that denotes the maximum number of results that 
#                should be returned by the function. 
#                Default value: 10.
# * radius: A float that denotes the number of miles within which the search
#           results should be restricted.
#           Default value: 2.0
# * sort: A boolean value indicating whether the results should be sorted by
#         the length of the articles or not.
#         Default value: False.
#
# Returns
#
# A list of wikipedia.WikipediaPage objects that match the search parameters.
# If no results are found, a blank list (`[]`) is returned.
#
#
# Define your function here
def wikipedia_locationsearch(place, max_results=10, radius=2.0, sort=False):
    wiki_list = []
    place_geocode = geocode(place)
    if place_geocode is not None:
        pages = wikipedia.geosearch(place_geocode[0], place_geocode[1], None, max_results, round(radius * 1609))
        for page in pages:
            wiki_list.append(wikipedia.WikipediaPage(page))
        if sort:
            wiki_list.sort(key=page_length, reverse=True)
    return wiki_list


def page_length(page):
    return len(page.content)


## Code to test your function follows follows
def main():
    print("-- Trying to find the latitude and longitude of UW --")
    print(geocode("University of Washington"))

    # time.sleep(1) pauses the program for 1 second before proceeding 
    # This is an useful strategy for working with APIs that restrict how 
    # many times you call it in a given period of time (often referred to as
    # rate-limiting).
    time.sleep(1)

    print("-- Trying to find the latitude and longitude of a non-existent place --")
    print(geocode("University of Nowhere"))

    time.sleep(1)

    print("-- Getting 5 articles close to UW --")
    print("Content length\tURL")
    for article in wikipedia_locationsearch("University of Washington", max_results=5):
        print("{}\t\t{}".format(len(article.content), article.url))

    time.sleep(1)

    print("-- Getting 5 articles close to UW (sorted by article length, longest first) --")
    print("Content length\tURL")
    for article in wikipedia_locationsearch("University of Washington", max_results=5, sort=True):
        print("{}\t\t{}".format(len(article.content), article.url))

    time.sleep(1)

    print("-- Getting results for a non-existent place --")
    print(wikipedia_locationsearch("University of Nowhere"))


if __name__ == "__main__":
    try:
        main()
    except (NameError, SyntaxError):
        # pass does "nothing" - it is useful if you are trying to nothing in your code, 
        # but still need a line to avoid a syntax error
        pass
