import json
import time
import urllib
import urllib2

def timezone(lat, lng, timestamp):
    # The maps_key defined below isn't a valid Google Maps API key.
    # You need to get your own API key.
    # See https://developers.google.com/maps/documentation/timezone/get-api-key

    maps_key = 'AIzaSyDAj9093jcPuXCGAYJ0mGvakV_7jdndZgE'
    timezone_base_url = "https://maps.googleapis.com/maps/api/distancematrix/json?origins=Vancouver+BC|Seattle&destinations=San+Francisco|Victoria+BC&mode=bicycling&language=fr-FR&key="

    # This joins the parts of the URL together into one string.
    # url = timezone_base_url + '?' + urllib.urlencode({
    #     'location': "%s,%s" % (lat, lng),
    #     'timestamp': timestamp,
    #     'key': maps_key,
    # })

    url = timezone_base_url + maps_key

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
            result = json.loads(response.replace('\\n', ''))
            if result['status'] == 'OK':
                return result['timeZoneId']
            elif result['status'] != 'UNKNOWN_ERROR':
                # Many API errors cannot be fixed by a retry, e.g. INVALID_REQUEST or
                # ZERO_RESULTS. There is no point retrying these requests.
                raise Exception(result['error_message'])

        if current_delay > max_delay:
            raise Exception('Too many retry attempts.')
        print 'Waiting', current_delay, 'seconds before retrying.'
        time.sleep(current_delay)
        current_delay *= 2  # Increase the delay each time we retry.

tz = timezone(39.6034810, -119.6822510, 1331161200)
print 'Timezone:', tz