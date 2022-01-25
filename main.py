from tkinter import *
import live_tests as tests
import adaptive_main
import plotter

window = Tk()
window.title("Adaptive  Traffic Light System")
window.maxsize(1000, 800)
window.config(bg='white')

def run_sim():
    adaptive_main.main()

def test():
    tests.main()

def view_results():
    plotter.plot()

UI_frame = Frame(window, width=900, height=300, bg='white')
UI_frame.grid(row=0, column=0,padx=10, pady=5)

b1 = Button(UI_frame, text="Run Simulation", command=run_sim, bg='white')
b1.grid(row=1, column=1, padx=100, pady=50)

b2 = Button(UI_frame, text="Run all tests", command=test, bg='white')
b2.grid(row=2, column=1, padx=100, pady=50)

b3 = Button(UI_frame, text="View results", command=view_results, bg='white')
b3.grid(row=3, column=1, padx=100, pady=50)

window.mainloop()