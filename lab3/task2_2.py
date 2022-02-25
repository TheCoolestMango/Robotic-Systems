from time import perf_counter, sleep
from multiprocessing import Process, Manager
from numpy import array, zeros, sin, pi, linspace
from scipy.integrate import odeint
import matplotlib.pyplot as plt
import os


# pendulum parameters
theta = pi/2 # start
dtheta_start = 0
m = 0.1      # mass
l = 0.1      # length
g = 9.81     # grav
b = 0.002        # damping coefficient

# Set the control loop timings
frequency = 500
sampling_time = 1/frequency
# dt of the simulator is sim_ratio times greater
sim_ratio = 10

positions = Manager().list()
velocities = Manager().list()
sim_time = Manager().list()

pendulum = Manager().Namespace()
# SET INITIAL STATE
pendulum.state = zeros(2)
pendulum.state = array([theta,0])
pendulum.control = 0 

def f(x, t, control):
  theta, dtheta = x
  return [dtheta, (-b/(m*l*l))*dtheta-(g/l)*sin(theta)+control/(m*l*l)]

# simulator process
def simulator(system):
    try:
        last_execution = 0
        initial_time = perf_counter()
        while True:
            # /////////////////////////////////////////// 
            time = perf_counter() - initial_time # get actual time in secs
            #print(time)
            dt = time - last_execution 
            if dt >= sampling_time/sim_ratio:
                t = linspace(last_execution,time,2)
                last_execution = time
                
                control = system.control
                out = odeint(f, system.state, t, args=(system.control,))

                system.state = array([out[-1][0], out[-1][1]])
                
                positions.append(out[:,1])
                velocities.append(out[:,0])
                sim_time.append(t)
                

    except KeyboardInterrupt:
        print('\nSimulator is terminated')
        

simulator_proc = Process(target=simulator, args=(pendulum,))
simulator_proc.start()

try:

  # Control process 

  
    last_execution = 0
    control = 0 
    # find the global time before intering control loop 
    initial_time = perf_counter()
    while True:
        time = perf_counter() - initial_time # get actual time in secs
        
        theta, dtheta = pendulum.state
        # ///////////////////////////////////////////
        # Update the control only on specific timings
        # /////////////////////////////////////////// 
        if (time - last_execution) >= sampling_time:
            last_execution = time
            control = 0

        pendulum.control = 0
        
        #print(f'State: {pendulum.state}', end='    \r', flush=True)


except KeyboardInterrupt:

    print('Disabled by interrupt')
except Exception as e:
    print(f'\n!!!! EXCEPTION !!!!\n {e} \n!!!! EXCEPTION !!!!\n')

finally:
    sleep(0.5)
    simulator_proc.join()

#print(positions)

flat_pos = [item for sublist in positions for item in sublist]
flat_vel = [item for sublist in velocities for item in sublist]
flat_time = [item for sublist in sim_time for item in sublist]

plt.plot(flat_time, flat_vel, label='$\\theta, rad$')
plt.plot(flat_time, flat_pos, label='$\\dot{\\theta}, \\frac{rad}{s}$')
plt.grid()
plt.title("Responces, no control")
plt.xlabel('time, s')
plt.ylabel('Position and velocity, rad, rad/s')
plt.legend()

plt.show()