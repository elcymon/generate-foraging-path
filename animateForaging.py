# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animateForaging(robotsDF,littersDF,nestDF,robots,worldXlength = 50, worldYlength = 50):
    colors = plt.cm.inferno(np.linspace(0,0.9,5))
    fig = plt.figure(figsize=(4,4))
    
    ax = fig.add_subplot(111,aspect='equal',autoscale_on=False,\
                         xlim=(-worldXlength/2.0,worldYlength/2.0),\
                         ylim=(-worldXlength/2.0,worldYlength/2.0))
    searching_particles, = ax.plot([],[],'o',color=colors[4],markersize=5)
    homing_particles, = ax.plot([],[],'o',color=colors[1],markersize=5)
    nest_particle, = ax.plot([],[],'+',color=colors[0],markersize=10)
    litter_particles, = ax.plot([],[],'o',color=colors[2],markersize=2)
    
    time_text = ax.text(0.02, 1.01, '', transform=ax.transAxes)

    rect = plt.Rectangle((-worldXlength/2.0,-worldYlength/2.0),worldXlength,worldYlength,ec='none',lw=2,fc='none')
    ax.add_patch(rect)
    def init():
        searching_particles.set_data([],[])
        homing_particles.set_data([],[])
        nest_particle.set_data([],[])
        litter_particles.set_data([],[])
        time_text.set_text('')
        
        rect.set_edgecolor('none')
        return searching_particles,homing_particles,time_text,nest_particle,rect
    
    def animationStep(i):
        print(i)
        sx = []
        sy = []
        hx = []
        hy = []
#        print(i)
        for r in robots:
            if robotsDF.loc[i,(r,'litterCount')] == 5:
                hx.append(robotsDF.loc[i,(r,'x')])
                hy.append(robotsDF.loc[i,(r,'y')])
            else:
                sx.append(robotsDF.loc[i,(r,'x')])
                sy.append(robotsDF.loc[i,(r,'y')])
        
        
        litterObjects = littersDF.loc[littersDF[i],['x','y']]
        litter_particles.set_data(litterObjects['x'],litterObjects['y'])
        litter_particles.set_markersize(2)
        
        time_text.set_text('{} seconds'.format(i))
        
#        print(x)
#        print(y)
        searching_particles.set_data(sx,sy)
        searching_particles.set_markersize(5)
        
        homing_particles.set_data(hx,hy)
        homing_particles.set_markersize(5)
        
        nest_particle.set_data([0],[0])
        nest_particle.set_markersize(10)
        
        rect.set_edgecolor('k')
        return searching_particles,homing_particles,time_text,nest_particle,rect
    ani = animation.FuncAnimation(fig,animationStep,frames=robotsDF.index,blit=True,init_func=init)
    plt.close()
    return ani
        
#animateForaging(robotsDF,littersDF,nestDF,foragingWayPointsDF.keys())
