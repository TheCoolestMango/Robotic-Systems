from numpy import array, zeros, sin, pi, linspace
import matplotlib.pyplot as plt
import pandas as pd

table_ff = pd.read_csv('pendulum_ff.csv')
table_ff =table_ff.rename(columns={'2.414047001366270706e-03': 'time', '1.579233221128267584e+00':'angle', '0.000000000000000000e+00':"speed", '0.000000000000000000e+00.1':'control torques'})
#print(list(table_ff.columns.values))

t = table_ff['time']
angle = table_ff['angle']
speed = table_ff['speed']

plt.plot(t, angle, label='$\\theta, rad$')
plt.plot(t, speed, label='$\\dot \\theta, \\frac{rad}{s}$')
plt.title("Experimental data (Free Fall)")
plt.xlabel("time, sec")
plt.ylabel("Angle and speed, rad, rad/s")
plt.grid()
plt.legend()

plt.show()