import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation

fig = plt.figure()
fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
ax = fig.add_subplot(111, aspect='equal', autoscale_on=False,
                     xlim=(-80, 80), ylim=(-80, 80))

# particles holds the locations of the particles
swarm_agents, = ax.plot([], [], 'bo', ms=6)
control_agents, = ax.plot([],[], 'ro', ms=6)

datax = pd.read_csv('sim1_time_500_10_10_100_X.txt',sep=' ',header=None)
datay = pd.read_csv('sim1_time_500_10_10_100_Y.txt',sep=' ',header=None)

i = 0

def init():
    """initialize animation"""
    global swarm_agents, control_agents
    swarm_agents.set_data([], [])
    control_agents.set_data([], [])
    return swarm_agents, control_agents

def animate(i):
    """perform animation step"""
    global datax, datay
    
    # update pieces of the animation
    swarm_agents.set_data(datax.iloc[i,0:49],datay.iloc[i,0:49])
    control_agents.set_data(datax.iloc[i,50],datay.iloc[i,50])
    return swarm_agents, control_agents



ani = animation.FuncAnimation(fig, animate, frames=5000,
                              interval=10, blit=True, init_func=init)

#ani.save('greater.mp4', fps=30, extra_args=['-vcodec', 'libx264'])

plt.show()
