# Adaptive Traffic System

A traffic management system that actuates traffic lights using TomTom API data.

## Project Description

The project uses Simulation of Urban Mobility(SUMO) to simulate traffic conditions on a single intersection([Haile Selassie Roundabout, Nairobi](https://goo.gl/maps/XbZQ2LKmG7LmMMuX9)).
The traffic lights in the simulation are controlled by a Python script via a Traffic Control Interface(TraCI). The script makes signalling decisions based solely on the average speed and travel time
of each of the 4 arms of the intersection. 

## To run this project you need:
  - Python3
  - SUMO v1.10.0
  
## How to Run Simulations
1. Run the main.py file
2. Choose between 3 options:
    - Run a single simulation with SUMO-GUI to observe the adaptive system in action 
    - Run 30 preset simulations(without GUI) and show performance data 
    - Show performance data of already-run simulations
  
## More Functionalities
- Run live_routes.py to generate a file that records 20 minutes worth of live traffic data
