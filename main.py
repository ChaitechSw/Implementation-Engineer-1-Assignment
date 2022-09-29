from bs4 import BeautifulSoup
import xml.etree.ElementTree as ETs
import urllib.parse
import requests
from flask import Flask, jsonify


def xml_response(resp1):
    """This function converts the response from the requests module into
    xml root and will be called when the output_format required is xml. The
    call to this function will pass a response from requests.get method.
    """
    # This converts and write the response content into 'geocode.xml'.
    with open("geocode.xml", 'wb') as fi:
        fi.write(resp1.content)

    # This opens 'geocode.xml' in read mode so as the BeautifulSoup can get
    #  desired data in order to arrange the data in xml format.
    with open("geocode.xml", 'r') as fi:
        file1 = fi.read()

    # To write the response content into xml file and get the desired content
    # soup will have the xml data in the form of a string scrapped using
    # BeautifulSoup. 'new_list' is the list containing the lattitude and
    # longitude of the given address stored as string elements of new_list.
    soup = BeautifulSoup(file1, 'xml')
    lat_lng_list = soup.find_all('location')
    new_list = lat_lng_list[0].text.split('\n')

    # This builds the xml format from the data we have till now
    # the xml is built starting from root and root is returned to the function
    # call. 'root' is element and 'address', 'coordinates', 'lattitude' and
    # 'longitude' are subelements created and arranged accordingly into xml.
    root = ETs.Element("root")
    root = ETs.SubElement(root, 'root')
    address = ETs.SubElement(root, 'address')
    address.text = str(request_data["address"])
    coordinates = ETs.SubElement(root, 'coordinates')
    lattitude = ETs.SubElement(coordinates, 'lat')
    lattitude.text = str(new_list[1])
    longitude = ETs.SubElement(coordinates, 'lng')
    longitude.text = str(new_list[2])

    return root


def json_response(resp1):
    """This function takes response as input and returns the dictionary
    containing desired data.
    """
    result = resp1.json()  # 'result' is a dictionary (json format)
    dict_of_results = result["results"][0]  # As the 'results' is a list
    return dict_of_results


# Request data used to create the url in order to get the desired data from
# Geocode API. desired 'output-format' must be specified i.e., 'json' or 'xml'
request_data = {
                "address": "# 3582,13 G Main Road, 4th Cross Rd, Indiranagar,\
                Bengaluru, Karnataka 560008",
                "output_format": "xml"
            }

# the API key and base url are stored as constants
API_KEY = "AIzaSyCOD3KvY2DDzEfel-NZ_LKIWXr86EF_EUw"
BASE_URL = "https://maps.googleapis.com/maps/api/geocode/"

# the properly encoded address and key part of the url is stored in params
params = urllib.parse.urlencode({"address": {request_data["address"]},
                                "key": API_KEY})

# response1 object contains the data fetched from the 'requests.get' method
response1 = requests.get(f"{BASE_URL}{request_data['output_format']}?{params}")

# creates object app from class Flask with argument __name__.
app = Flask(__name__)
# this disables app object's alphabetical sorting
app.config["JSON_SORT_KEYS"] = False


# this routes to the homepage
@app.route('/')
def home_page():
    return "<h1>Welcome, to the geolocator</h1>"


@app.route('/getAddressDetails')
def address_page():
    """Desired endpoint API : 1. Calls to the json_response func and returns
    the required data to API in json format if the 'output_format' is 'json'
    2. Calls to the xml_response func and returns the required data to API
    in xml format if the 'output_format' is 'xml'.
    """
    if request_data["output_format"] == "json":
        op_json = json_response(response1)
        # Return the json file containg the lattitude and longitude
        # in json format. Method 'jsonify' helps in achieving the same
        # The address to return is taken from request_data so as to match
        # exactly with the input as required in the assignment otherwise it
        # it could be taken from the response too.
        return jsonify({"coordinates": op_json["geometry"]["location"],
                        "address": request_data["address"]})

    elif request_data["output_format"] == "xml":
        xml_root = xml_response(response1)
        # response_class object returns the xml string (provided as
        # content_type and converted to string from root xml element using
        # 'ETs.tostring' method)
        return app.response_class(ETs.tostring(xml_root),
                                  content_type='text/xml; charset=utf-8')


# This keep the main function running in the debug mode.
if __name__ == "__main__":
    app.run(debug=True)
