import os, sys
import xml.etree.ElementTree as ET
if 'SUMO_HOME' in os.environ:
    tools = os.path.join(os.environ['SUMO_HOME'], 'tools')
    sys.path.append(tools)
else:
    sys.exit("Please declare environment variable 'SUMO_HOME'")
from sumolib import checkBinary
import traci
import traci.constants as tc


YELLOW_TIME = 3
GREEN_TIME = 30
NS_GREEN_STATE = "GGgrrrGGgrrr"
NS_YELLOW_STATE = "YYyrrrYYyrrr"
WE_GREEN_STATE = "rrrGGgrrrGGg"
WE_YELLOW_STATE = "rrrYYyrrrYYy"

def run_algorithm():
    global waiting_times
    waiting_times = {}
    traci.junction.subscribeContext("intersection", tc.CMD_GET_VEHICLE_VARIABLE, 42, [tc.VAR_SPEED, tc.VAR_WAITING_TIME])

    GREEN_TIME = 30
    green = 0
    yellow = 0
    west_east = True
    yellow_phase = False
   
    step = 0
  
    waiting_time = 0
    waiting_time2 = 0
    vehicle_amount = 0

    while traci.simulation.getMinExpectedNumber() > 0:
        traci.simulationStep()
        step += 1

        #Increment time for the different phases
        if yellow_phase:
            yellow += 1
            #Time maximized, switch state
            if yellow > YELLOW_TIME:
                yellow = 0
                yellow_phase = False
                if west_east:
                    traci.trafficlight.setRedYellowGreenState("intersection", NS_GREEN_STATE)
                    west_east = False
                else:
                    traci.trafficlight.setRedYellowGreenState("intersection", WE_GREEN_STATE)
                    west_east = True
        else:
            green += 1
            #Time maximized, switch state
            if green > GREEN_TIME:
                green = 0
                yellow_phase = True
                if west_east:
                    traci.trafficlight.setRedYellowGreenState("intersection", WE_YELLOW_STATE)
                else:
                    traci.trafficlight.setRedYellowGreenState("intersection", NS_YELLOW_STATE)
        waiting_time_results = traci.junction.getContextSubscriptionResults("intersection")
        for veh in waiting_time_results:
            if veh not in waiting_times.keys():
                waiting_times[veh] = waiting_time_results[veh][122]
            else:
                waiting_times[veh] += waiting_time_results[veh][122]

    traci.close()   
    sys.stdout.flush()
    tree = ET.parse('timed/timed-tripinfo.xml')
    vehicles  = tree.getroot()
    av_waiting_time = 0
    for veh in vehicles:
        av_waiting_time += float(veh.attrib['waitingTime'])
        
    print("Average waiting time", av_waiting_time/len(vehicles)) 
    return av_waiting_time/len(vehicles), (av_waiting_time**2)/len(vehicles)

def run(route,binary):
    #Get the binary for SUMO
    sumoBinary = checkBinary('sumo') if binary else checkBinary('sumo-gui')
    route  = 'live_routes/'+ route if route != '' else 'live.rou.xml'
    #Connect to SUMO via TraCI
    traci.start([sumoBinary,"-r",route,"-c", "timed.sumocfg", "--waiting-time-memory", "1000"])

    return run_algorithm()

if __name__ == '__main__':
    run('',False)
       