import time
from datetime import date, timedelta
import urllib2
import sys

#######################################
# Setup variables
#######################################

wunderground_url = "http://api.wunderground.com/api"
key = ""
country = "UK"
city = "Glasgow"

max_numer_of_queries = 500;
requests_per_minute = 9;

from_date = date.today()

#######################################
# Helper Functions
#######################################

def get_url(date):
    return wunderground_url + "/" + key + "/history_" + date.strftime("%Y%m%d") + "/q/" + country + "/" + city + ".json"

def get_nice_filename(date):
    return country + "_" + city + "_" + date.strftime("%Y%m%d") + ".json" 

#######################################
# Worker Loop
#######################################

time_delta_seconds = 60/requests_per_minute
the_date = from_date
request_number = 0;

try:

    sys.stdout.write("Starting acquisition loop, press Ctrl-C to exit\n")

    # Start the worker loop
    while(max_numer_of_queries > 1):
        max_numer_of_queries -= 1
        request_number += 1

        sys.stdout.write("Request #" + str(request_number) + "\n")
        sys.stdout.write("> Requesting data for " + the_date.strftime("%Y/%m/%d") + "... ")
        sys.stdout.flush()
        response = urllib2.urlopen(get_url(the_date))
        json = response.read()

        sys.stdout.write("success\n")

        the_file = get_nice_filename(the_date)
        sys.stdout.write("> Writing to file '" + the_file + "'\n")
        f = open(the_file, 'w')
        f.write(json)
        f.close()

        sys.stdout.write("> Waiting for next request in " + str(time_delta_seconds) + " seconds...\n")
        time.sleep(time_delta_seconds)

        the_date = the_date - timedelta(days=1)

# Catch Ctrl-C
except KeyboardInterrupt:
    print("<<< USER INPUT CAUGHT - EXITING >>>")
    sys.exit()












