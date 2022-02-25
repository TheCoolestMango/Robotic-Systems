from numpy import array, zeros, sin, pi, linspace
import matplotlib.pyplot as plt
import pandas as pd

table_pd = pd.read_csv('pendulum_pd.csv')
table_pd =table_pd.rename(columns={'2.287950002937577665e-03': 'time', '-1.150485590914230877e-03':'angle', '0.000000000000000000e+00':"speed", '4.715840437157431952e-01':'control torques'})
print(list(table_pd.columns.values))

t = table_pd['time']
angle = table_pd['angle']
speed = table_pd['speed']
control = table_pd['control torques']

plt.plot(t, angle, label='$\\theta, rad$')
plt.plot(t, speed, label='$\\dot \\theta, \\frac{rad}{s}$')
plt.plot(t,control, label='torque')
plt.title("Experimental data (PD regulator)")
plt.xlabel("time, sec")
plt.grid()
plt.legend()

plt.show()