import json
import time
import urllib
import urllib2

api_key = 'AIzaSyDAj9093jcPuXCGAYJ0mGvakV_7jdndZgE'
base_url = "https://maps.googleapis.com/maps/api/distancematrix/json?"


def buildUrl(origins, destinations):

    return base_url +  '&'.join((
        "origins=" + "|".join(o.replace(',', '').replace(' ', '+') for o in origins),
        "destinations=" + "|".join(o.replace(',', '').replace(' ', '+') for o in destinations),
        "units=metric",
        "mode=driving",
        "avoid=ferries",
        "key=" + api_key
    ))


def callAPI(url):

    # The maps_key defined below isn't a valid Google Maps API key.
    # You need to get your own API key.
    # See https://developers.google.com/maps/documentation/timezone/get-api-key

    current_delay = 0.1  # Set the initial retry delay to 100ms.
    max_delay = 3600  # Set the maximum retry delay to 1 hour.

    while True:
        try:
            # Get the API response.
            response = str(urllib2.urlopen(url).read())
        except IOError:
            pass  # Fall through to the retry loop.
        else:
            # If we didn't get an IOError then parse the result.
            result = json.loads(response.replace('\\n',''))
            if result['status'] == 'OK':
                return result
            elif result['status'] != 'UNKNOWN_ERROR':
                # Many API errors cannot be fixed by a retry, e.g. INVALID_REQUEST or
                # ZERO_RESULTS. There is no point retrying these requests.
                raise Exception(result['error_message'])

        if current_delay > max_delay:
            raise Exception('Too many retry attempts.')
        print 'Waiting',current_delay,'seconds before retrying.'
        time.sleep(current_delay)
        current_delay *= 2  # Increase the delay each time we retry.


print buildUrl(
    ("17000 31 Mile Road, Ray, MI, 48096", "17603 T St., Omaha, NE, 68135"),
    ("4682 Huron Hill Drive, Lansing, MI, 48864", "12412 W 110th Terrace, Overland Park, KS, 66210"))


"""
https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&units=metric&mode=driving&avoid=ferries&key=AIzaSyDAj9093jcPuXCGAYJ0mGvakV_7jdndZgE
https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=17000+31+Mile+Road+Ray+MI+48096|17603+T+St.+Omaha+NE+68135&units=metric&mode=driving&avoid=ferries&key=AIzaSyDAj9093jcPuXCGAYJ0mGvakV_7jdndZgE
https://maps.googleapis.com/maps/api/distancematrix/json?origins=17000+31+Mile+Road+Ray+MI+48096|17603+T+St.+Omaha+NE+68135&destinations=San+Francisco|Victoria+BC&units=metric&mode=driving&avoid=ferries&key=AIzaSyDAj9093jcPuXCGAYJ0mGvakV_7jdndZgE
https://maps.googleapis.com/maps/api/distancematrix/json?origins=17000+31+Mile+Road+Ray+MI+48096|17603+T+St.+Omaha+NE+68135&destinations=17000+31+Mile+Road+Ray+MI+48096|17603+T+St.+Omaha+NE+68135&units=metric&mode=driving&avoid=ferries&key=AIzaSyDAj9093jcPuXCGAYJ0mGvakV_7jdndZgE

"""