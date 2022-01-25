from sys import addaudithook
from pandas import *
import matplotlib.pyplot as plt

def plot():
    data = read_csv('results.csv')

    timed = data['timed'].tolist()
    adaptive = data['adaptive'].tolist()
    adaptive,timed = zip(*sorted(zip(adaptive, timed)))
    print(timed,adaptive)

    fig,ax = plt.subplots()
  
    ax.plot(timed,label='Pretimed algorithm')
    ax.plot(adaptive,label='Adaptive algorithm')
    ax.set_xlabel('Average number of vehicles(\'00s)')
    ax.set_ylabel('Average waiting time (s)')
    ax.legend()


    #plt.plot(timed,'r', adaptive,'b');  # Plot some data on the axes.
    plt.show()

if __name__ == '__main__':
    plot()