import trivial_traffic_light as trivial
import adaptive_main as adaptive
import argparse
import os,csv
import plotter
LEARNING_RUNS = 5


def run_adaptive(file):
    return adaptive.run(file,True)

def run_timed(file):
    return trivial.run(file,True)

def main():
    av_wait = []
    directory = 'live_routes'
    
    for file in os.listdir(directory):
        av_adaptive, _ = run_adaptive(file)
        av_timed,_ = run_timed(file)

        av_wait.append([av_timed,av_adaptive])



     
    with open('results.csv','w') as results:
        writer = csv.writer(results)
        writer.writerow(['timed','adaptive'])
        for i in range(len(av_wait)):
            writer.writerow(av_wait[i])
    
    plotter.plot()

if __name__ == '__main__':
    main()
        


        