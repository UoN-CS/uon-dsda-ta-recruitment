import json
import requests
import pandas as pd


class Station:
    def __init__(self, label):
        url = 'https://environment.data.gov.uk/flood-monitoring/id/stations?label=' + label

        # Try to make the http request, but throw an exception if something goes wrong
        try:
            response = requests.get(url)
        except requests.ConnectionError:
            raise Exception("Something went wrong with the internet")

        responsetext = response.text
        responsejson = json.loads(responsetext)

        # The JSON should contain one response in an array called 'items', so we take the zeroth item.
        station = responsejson['items'][0]

        # Then we start pulling out values from json and setting them as attributes on the instance
        self._id = station['@id']
        self.label = station['label']
        self.lat = station['lat']
        self.long = station['long']
        self.town = station['town']
        self.riverName = station['riverName']
        self.catchmentName = station['catchmentName']
        self._measures = station['measures']

    def __str__(self):
        return ('Station: ' + self.label + ' at ({:f},{:g}) in town: ' + self.town + ' on river: ' + self.riverName +
                ', catchment area: ' + self.catchmentName).format(self.lat, self.long)

    def getWaterLeveldf(self):
        # Check through each measure to see if we have a water flow measure
        hasmeasure= False
        for measure in self._measures:
            if 'Water Level'.__eq__('Water Level'):
                hasmeasure=True

        if not hasmeasure:
            raise Exception("Station does not support Water Level Measure")

        # set the url for
        url = self._id + '/readings'

        # Try to make the http request, but throw an exception if something goes wrong
        try:
            response = requests.get(url)
        except requests.ConnectionError:
            raise Exception("Something went wrong with the internet")

        responsetext = response.text
        responsejson = json.loads(responsetext)

        readingdata = list()

        # Append the reading dates and values to a list
        for reading in responsejson['items']:
            readingdata.append([reading['dateTime'], reading['value']])

        # Create a DataFrame to return to the client
        readingsdf = pd.DataFrame(readingdata, columns=['Date', 'Water Level'])

        return readingsdf



