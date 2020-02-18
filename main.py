import folium
import ssl
import time
import doctest
from geopy.geocoders import Nominatim
from geopy import distance

ssl._create_default_https_context = \
    ssl._create_unverified_context


def open_file(file):
    """
    str -> dict
    Function that opens file correctly and returns a dictionary where key is a year and values are places, where films were made
    """
    main_dict = {}
    with open(file, encoding='utf-8', errors='ignore') as f:

        for line in f:
            line = line.strip().split('\t')
            if line[-1].startswith('(') and line[-1].endswith(')'):
                line.pop(-1)
            new_line = line[0].split(' ')
            for el in new_line:
                if el.startswith('(') and el.endswith(')'):
                    if len(el) == 6:
                        year = el[1:5]
                        try:
                            year = int(year)
                        except:
                            continue
                    if year not in main_dict:
                        main_dict[year] = []
                        if line[-1] not in main_dict.values():
                            main_dict[year].append(line[-1])
                        else:
                            continue
                    else:
                        if line[-1] not in main_dict.values():
                            main_dict[year].append(line[-1])
                        else:
                            continue
    return main_dict


def convert_to_coordinates(year):
    """
    int -> list
    Function returns the coordinates of all places, where films were made in some year
    >>> convert_to_coordinates(2019)
    [(33.7490987, -84.3901849), (37.7790262, -122.4199061), (29.7589382, -95.3676974), (39.9527237, -75.1635262), (40.0757384, -74.4041622), (39.8681671, -75.5443967), (39.9527237, -75.1635262), (40.0757384, -74.4041622), (39.8681671, -75.5443967), (50.0874654, 14.4212535), (50.0874654, 14.4212535), (30.1765914, -85.8054879), (59.740687699999995, 10.509270396735879)]
    """
    start = time.time()
    dict = open_file('locations.list.txt')
    actual_year = dict[year]
    geolocator = Nominatim(user_agent="specify_your_app_name_here", timeout=3)
    all_coordinates = []
    for address in actual_year:
        try:
            location = geolocator.geocode(address)
            info = location.latitude, location.longitude
            all_coordinates.append(info)
            if time.time() - start >= 60:
                break
        except:
            continue
    return all_coordinates


def choose_the_nearest(coordinates, year):
    """
    list/tuple, int -> list
    Function returns the coordinates of top 10 places, where films were made in some year, and that are the closest to our coordinates
    >>> choose_the_nearest([49.83826, 24.02324], 2019)
    [[(50.0874654, 14.4212535)], [(59.740687699999995, 10.509270396735879)], [(42.3602534, -71.0582912)], [(40.0757384, -74.4041622)], [(39.9527237, -75.1635262)], [(39.8681671, -75.5443967)], [(33.7490987, -84.3901849)], [(30.1765914, -85.8054879)], [(29.7589382, -95.3676974)], [(37.7790262, -122.4199061)]]

    """
    dict_of_distances = {}
    lst = convert_to_coordinates(year)
    our_address = coordinates
    the_nearest = []
    for item in lst:
        dist = distance.distance(item, our_address).kilometers
        dict_of_distances[dist] = []
        dict_of_distances[dist].append(item)
    final_lst = sorted(dict_of_distances.items())
    for el in final_lst[:10]:
        the_nearest.append(el[1])
    return the_nearest


def generate_map(coordinates, year):
    """
    list, int -> object
    Function that generates map
    """
    locations = choose_the_nearest(coordinates, year)
    m = folium.Map(location=coordinates, zoom_start=8)

    ch = folium.FeatureGroup(name="Marker map")
    ch.add_child(folium.Marker(coordinates,
                               icon=folium.Icon(color='green'),
                               tooltip='your location'))

    for place in locations:
        for el in place:
            ch.add_child(folium.Marker(el, tooltip='filming place', icon=folium.Icon(color='red')))
    m.add_child(ch)
    m.save('map.html')
    return 'The map is generated. Please open it in new-created file map.html'


def user_input(user_location, year):
    """
    str, str -> None
    Function that checks user input
    """
    if len(user_location) != 2:
        print('You entered wrong location. Try something like that: 49.817545, 24.023932')
    if year > 2021:
        print('You entered wrong year. Try again')
    return None


if __name__ == '__main__':
    try:
        print('Type your location or location you want to see the map about in format: lat, long')
        coordinates = input()
        coordinates = coordinates.strip().split(',')
        user_location = []
        for el in coordinates:
            el = float(el)
            user_location.append(el)
        print('Type the year you want to know see the map about')
        year = int(input())
        user_input(user_location, year)
        print('Your map will be generated. Please wait')
        print(generate_map(user_location, year))
        print(doctest.testmod())
    except:
        user_input(user_location, year)
