import os, sys
import xml.etree.ElementTree as ET
import json
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")
from sumolib import checkBinary
import traci
import traci.constants as tc

YELLOW_TIME = 3
GREEN_TIME = 20
MAX_GREEN_TIME = 30
MIN_GREEN_TIME = 10
LOWER_TIME_THRESHOLD = 15
UPPER_TIME_THRESHOLD = 20
SEED_TIME = 20



NS_GREEN_STATE = "GGgrrrGGgrrr"
NS_YELLOW_STATE = "YYyrrrYYyrrr"
WE_GREEN_STATE = "rrrGGgrrrGGg"
WE_YELLOW_STATE = "rrrYYyrrrYYy"


def run_algorithm():
    global waiting_times
    waiting_times = {}
    traci.junction.subscribeContext("intersection", tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])
    #Density for all incoming roads
    density = {}
    density["west"] = 0
    density["north"] = 0
    density["east"] = 0
    density["south"] = 0

    #Time needed for cars on incoming roads to pass through
    time = {}
    time["west"] = SEED_TIME
    time["north"] = SEED_TIME
    time["east"] = SEED_TIME
    time["south"] = SEED_TIME

    yellow = False
    yellow_timer = 0

    green_timer = GREEN_TIME
    green_time = GREEN_TIME

    max_density = 0
    max_density_edge = "west"

    step = 0
    extended = False

    waiting_time = 0
    waiting_time2 = 0
    vehicle_amount = 0

    counter = 0
    key = 0
    while traci.simulation.getMinExpectedNumber() > 0:
        
        traci.simulationStep()
        step += 1
        #print(waiting_time)
       
        if counter == 1200 and key < (len(live_traffic.keys())-1):
            
            counter = 0
            key +=1
        if counter == 0:
            delay_west = live_traffic[key]['west'][1]-live_traffic[key]['west'][0]
            delay_north = live_traffic[key]['north'][1]-live_traffic[key]['north'][0]
            delay_east = live_traffic[key]['east'][1]-live_traffic[key]['east'][0]
            delay_south = live_traffic[key]['south'][1]-live_traffic[key]['south'][0]
        #Switching between roads
        if yellow:
            if yellow_timer < YELLOW_TIME:
                yellow_timer += 1
            else:
                yellow_timer = 0
                yellow = False
                if max_density_edge == "west" or max_density_edge == "east":
                    traci.trafficlight.setRedYellowGreenState("intersection", WE_GREEN_STATE)
                else:
                    traci.trafficlight.setRedYellowGreenState("intersection", NS_GREEN_STATE)
        #Light is green
        elif green_timer < green_time :
            #optimize next phases' duration and start time
            if int(green_time) - green_timer == 5 and not extended:
                #get current state
                if traci.trafficlight.getRedYellowGreenState("intersection") == NS_GREEN_STATE:
                    if delay_east >= UPPER_TIME_THRESHOLD or delay_west >= UPPER_TIME_THRESHOLD:
                        #start next phase 4 seconds earlier
                        green_timer = green_time
                        #add split for next phase while checking if maximum allowed green time is exceeded
                        time['east'] = min(time['east']+4, MAX_GREEN_TIME)
                        time['west'] = min(time['west']+4, MAX_GREEN_TIME)
                        continue
                    elif delay_east <=LOWER_TIME_THRESHOLD or delay_west <= LOWER_TIME_THRESHOLD:
                        green_timer -= 4
                        time['east'] = max(time['east']-4, MIN_GREEN_TIME)
                        time['west'] = max(time['west']-4, MIN_GREEN_TIME)
                        extended = True
                        continue
                if traci.trafficlight.getRedYellowGreenState("intersection") == WE_GREEN_STATE:
                    if delay_north >= UPPER_TIME_THRESHOLD or delay_south >=UPPER_TIME_THRESHOLD:
                        green_timer = green_time
                        time['north'] = min(time['north']+4, MAX_GREEN_TIME)
                        time['south'] = min(time['south']+4, MAX_GREEN_TIME)
                        continue
                    elif delay_north <= LOWER_TIME_THRESHOLD or delay_south <= LOWER_TIME_THRESHOLD:
                        green_timer -= 4
                        time['north'] = max(time['north']-4, MIN_GREEN_TIME)
                        time['south'] = max(time['south']-4, MIN_GREEN_TIME)
                        extended = True
                        continue
            elif int(green_time) - green_timer == 5 and extended:
                extended = False
            green_timer += 1
        #Determine which road that should get green light
        else:
            #print("Time values at",step,"seconds: ",time)
            green_timer = 0

            #Set current green road's values to 0
            if max_density_edge == "west" or max_density_edge == "east":
                density["west"] = 0
                density["east"] = 0
                #time["west"] = 0
                #time["east"] = 0
            else:
                density["north"] = 0
                density["south"] = 0
                #time["north"] = 0
                #time["south"] = 0

            previous_edge = max_density_edge
            max_density = 0

            #Get highest density
            for edge in density:
                if density[edge] > max_density:
                    max_density = density[edge]
                    max_density_edge = edge

            #All roads have been taken, recalculate values
            if max_density == 0:
                #density["west"],_ = traffic_analyzer.getDensityAndTimeOnEdge("west_right")
                #density["north"],_ = traffic_analyzer.getDensityAndTimeOnEdge("north_down")
                #density["east"],_ = traffic_analyzer.getDensityAndTimeOnEdge("east_left")
                #density["south"],_ = traffic_analyzer.getDensityAndTimeOnEdge("south_up")

                density['west'] = delay_west
                density['east'] = delay_east
                density['north'] = delay_north
                density['south'] = delay_south

                #Get highest density, again
                for edge in density:
                    if density[edge] > max_density:
                        max_density = density[edge]
                        max_density_edge = edge

            if max_density_edge == "west" or max_density_edge == "east":
                green_time = min(max(time["west"], time["east"]), GREEN_TIME)
                if previous_edge != "west" and previous_edge != "east":
                    yellow = True
                    traci.trafficlight.setRedYellowGreenState("intersection", NS_YELLOW_STATE)
            else:
                green_time = min(max(time["north"], time["south"]), GREEN_TIME)
                if previous_edge != "north" and previous_edge != "south":
                    yellow = True
                    traci.trafficlight.setRedYellowGreenState("intersection", WE_YELLOW_STATE)
        
        #print("num",num_vehicles)
        counter +=1
         
    traci.close()
    sys.stdout.flush()
    tree = ET.parse('adaptive/tripinfo.xml')
    vehicles  = tree.getroot()
    av_waiting_time = 0
    for veh in vehicles:
        av_waiting_time += float(veh.attrib['waitingTime'])
        
    print("Average waiting time", av_waiting_time/len(vehicles)) 
   
    return av_waiting_time/len(vehicles), (av_waiting_time**2)/len(vehicles)


def get_data(file):
    data = {}
    with open(file) as live_data:
        counter = 0
        for line in live_data:
            line = json.loads(line)
           
            data[counter] = line
            counter+=1
    return data

def run(route,binary):
    global live_traffic 
    file = 'live_traffic_data/'+str(route[:-8])+'.txt' if route != '' else 'live.txt'
    
    live_traffic = get_data(file)
    #Get the binary for SUMO
    #sumoBinary = checkBinary('sumo')
    sumoBinary = checkBinary('sumo') if binary else checkBinary('sumo-gui')
    #Connect to SUMO via TraCI
    route  = 'live_routes/'+ route if route != '' else 'live.rou.xml'
    traci.start([sumoBinary,"-r", route,"-c", "intersection.sumocfg", "--waiting-time-memory", "1000"])

    return run_algorithm()

def main():
    run('',False)

if __name__ == '__main__':
    run('',False)
