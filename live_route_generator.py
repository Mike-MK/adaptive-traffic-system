import random
import json

traffic_dict = {}
def get_data():
    data = []
    with open('live_data.txt') as live_data:
        counter = 0
        for line in live_data:
            line = json.loads(line)
           
            traffic_dict[counter] = line
            counter+=1
    
    return traffic_dict
   

def generate_vehicle(road):
    vehType = random.randint(0, 3)
    vehRoute = random.randint(0, 2) + road
    vehColorRed = random.randint(0, 1)
    vehColorGreen = random.randint(0, 1)
    vehColorBlue = random.randint(0, 1)
    if vehColorRed == 0 and vehColorGreen == 0 and vehColorBlue == 0:
        vehColorRed = 1
    return vehType, vehRoute, vehColorRed, vehColorGreen, vehColorBlue

def generate_routefile(d, variable):
    N = 1200 #Number of time steps

    if variable:
        print("Variable demand.")

    #Demand per second from any direction
    demand = d

    #Generate the route file
    with open("live.rou.xml", "w") as routes:
        print(
            """
            <routes>
                <vType id="0" accel="2" decel="4.5" sigma="0.5" length="5" minGap="2.5" maxSpeed="14" guiShape="passenger"/>
                <vType id="1" accel="2" decel="4.5" sigma="0.5" length="3" minGap="2.5" maxSpeed="14" guiShape="passenger"/>
                <vType id="2" accel="2" decel="4.5" sigma="0.5" length="4" minGap="2.5" maxSpeed="14" guiShape="passenger"/>
                <vType id="3" accel="2" decel="4.5" sigma="0.5" length="10" minGap="3" maxSpeed="14" guiShape="bus"/>

                <route id="0" edges="west_right north_up" />
                <route id="1" edges="west_right east_right" />
                <route id="2" edges="west_right south_down" />

                <route id="3" edges="north_down east_right" />
                <route id="4" edges="north_down south_down" />
                <route id="5" edges="north_down west_left" />

                <route id="6" edges="east_left south_down" />
                <route id="7" edges="east_left west_left" />
                <route id="8" edges="east_left north_up" />

                <route id="9" edges="south_up west_left" />
                <route id="10" edges="south_up north_up" />
                <route id="11" edges="south_up east_right" />

            """
        , file=routes)
        vehNr = 0
        
        timer = N
        counter = 0
        vehNr = 0 
        key = 0
        for k in range(timer):
            #print(k)    
            
            if counter == 60 and key < (len(traffic_dict.keys())-1):
                counter = 0
                key +=1

            if counter == 0:
                delay_west = (traffic_dict[key]['west'][1]-traffic_dict[key]['west'][0])/(traffic_dict[key]['west'][1])
                delay_north = (traffic_dict[key]['north'][1]-traffic_dict[key]['north'][0])/(traffic_dict[key]['north'][1])
                delay_east =  (traffic_dict[key]['east'][1]-traffic_dict[key]['east'][0])/(traffic_dict[key]['east'][1])
                delay_south = (traffic_dict[key]['south'][1]-traffic_dict[key]['south'][0])/(traffic_dict[key]['south'][1])
                print("delay",delay_west)

            random_value = random.uniform(0,1)
            if random_value < delay_west:
                vehType, vehRoute, vehCR, vehCG, vehCB = generate_vehicle(0)
                print('    <vehicle id="veh_%i" type="%i" route="%i" color="%f,%f,%f" depart="%i" />' % (vehNr, vehType, vehRoute, vehCR, vehCG, vehCB, k), file=routes)
                vehNr +=1

            
            if random_value < delay_north:
                vehType, vehRoute, vehCR, vehCG, vehCB = generate_vehicle(3)
                print('    <vehicle id="veh_%i" type="%i" route="%i" color="%f,%f,%f" depart="%i" />' % (vehNr, vehType, vehRoute, vehCR, vehCG, vehCB, k), file=routes)
                vehNr +=1
            if random_value < delay_east:
                vehType, vehRoute, vehCR, vehCG, vehCB = generate_vehicle(6)
                print('    <vehicle id="veh_%i" type="%i" route="%i" color="%f,%f,%f" depart="%i" />' % (vehNr, vehType, vehRoute, vehCR, vehCG, vehCB, k), file=routes)
                vehNr +=1
            if random_value < delay_south:
                vehType, vehRoute, vehCR, vehCG, vehCB = generate_vehicle(9)
                print('    <vehicle id="veh_%i" type="%i" route="%i" color="%f,%f,%f" depart="%i" />' % (vehNr, vehType, vehRoute, vehCR, vehCG, vehCB, k), file=routes)
                vehNr +=1
            
            counter +=1  
            
            
        print("</routes>", file=routes)


if __name__ == "__main__":
    print(get_data())
    generate_routefile(1./10, False)
