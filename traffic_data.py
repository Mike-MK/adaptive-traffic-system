import requests
import os
import json
import time

from requests.models import Response

coordinates ={}
coordinates['north'] = ["-1.29240954217018", "36.82036578390347"]
coordinates['south'] = ["-1.2931062453575046","36.820543205109104"]
coordinates['east'] = ["-1.2926898444299708", "36.82003745165547"]
coordinates['west'] = ["-1.2927727903675104", "36.82082903571767"]


traffic_data = {}
traffic_data['north'] = []
traffic_data['south'] = []
traffic_data['east'] = []
traffic_data['west'] = []

CURRENT_SPEED = 'currentSpeed'
FREEFLOW_SPEED = 'freeFlowSpeed'  
CURRENT_TRAVEL_TIME = 'currentTravelTime'
FREE_FLOW_TRAVEL_TIME = 'freeFlowTravelTime'
FLOW_SEGMENT_DATA = 'flowSegmentData'

def get_data(entry):
    api_key = "AYAu65a97RYakz6SjqIhe1wZDSYkel0b"
    
    for i in coordinates.keys():

        url = "https://api.tomtom.com/traffic/services/4/flowSegmentData/relative0/10/json?point={}%2C{}&key={}" \
                .format(
                    coordinates[i][0],
                    coordinates[i][1],
                    api_key)
        #print(url)
        #response = requests.get(url).json()
        #print(response)
        #print(response[FLOW_SEGMENT_DATA][FREEFLOW_SPEED])
        
        try:
            response = requests.get(url).json()
            if traffic_data[i]:
                traffic_data[i] = \
                    [response[FLOW_SEGMENT_DATA][CURRENT_SPEED],
                    response[FLOW_SEGMENT_DATA][FREEFLOW_SPEED],
                    response[FLOW_SEGMENT_DATA][CURRENT_TRAVEL_TIME],
                    response[FLOW_SEGMENT_DATA][FREE_FLOW_TRAVEL_TIME]]
                    
            else:
                traffic_data[i] = []
                traffic_data[i] = \
                    [response[FLOW_SEGMENT_DATA][CURRENT_SPEED],
                    response[FLOW_SEGMENT_DATA][FREEFLOW_SPEED],
                    response[FLOW_SEGMENT_DATA][CURRENT_TRAVEL_TIME],
                    response[FLOW_SEGMENT_DATA][FREE_FLOW_TRAVEL_TIME]]
                    
        except Exception as e:
            print("Exception", e)
        
        
    with open(entry,'a') as live_data:
        json.dump(traffic_data, live_data)
        live_data.write("\n")
    return traffic_data
    

if __name__ == '__main__':
    #get traffic data for 20 minutes
    N = 20
    data = []
    entry = 'live_traffic_data/data{}.txt'.format(time.time())
    with open(entry,'a'):
        for i in range(N):
            print(get_data(entry))
            print("Waiting 1 min ...")
            time.sleep(60)
    
    ''' 
    with open('live_data.txt') as live_data:
        for line in live_data:
            data.append(line.rstrip())
    print(data)
    '''
    
        
