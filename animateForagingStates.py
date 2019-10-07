# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np

def animateForagingStates(robotsDF,littersDF,nestDF,robots,worldXlength = 50, worldYlength = 50):
    colors = plt.cm.inferno(np.linspace(0,0.9,5))
    
    fig = plt.figure(figsize=(4,4))
    plt.tight_layout(pad=0.5)
    ax = fig.add_subplot(111,aspect='equal',autoscale_on=False,\
                         xlim=(-worldXlength/2.0,worldYlength/2.0),\
                         ylim=(-worldXlength/2.0,worldYlength/2.0))
    searching_particles, = ax.plot([],[],'o',color=colors[3],markersize=5)
    go4litter_particles, = ax.plot([],[],'o',color=colors[4],markersize=5)
    homing_particles, = ax.plot([],[],'o',color=colors[1],markersize=5)
    
    nest_particle, = ax.plot([],[],'+',color=colors[0],markersize=10)
    
    litter_particles, = ax.plot([],[],'*',color=colors[2],markersize=2)
    
    time_text = ax.text(0.02, 1.01, '', transform=ax.transAxes)

    rect = plt.Rectangle((-worldXlength/2.0,-worldYlength/2.0),worldXlength,worldYlength,ec='none',lw=2,fc='none')
    ax.add_patch(rect)
    
    def init():
        searching_particles.set_data([],[])
        go4litter_particles.set_data([],[])
        homing_particles.set_data([],[])
        
        nest_particle.set_data([],[])
        
        litter_particles.set_data([],[])
        
        time_text.set_text('')
        
        rect.set_edgecolor('none')
        
        return searching_particles,go4litter_particles,homing_particles,nest_particle,time_text,rect
    
    def animationStep(i):
        sx = []
        sy = []
        gx = []
        gy = []
        hx = []
        hy = []
        
#        print(i)
        for r in robots:
            if robotsDF.loc[i,(r,'state')] == 'homing':
                hx.append(robotsDF.loc[i,(r,'x')])
                hy.append(robotsDF.loc[i,(r,'y')])
            elif robotsDF.loc[i,(r,'state')] == 'searching':
                sx.append(robotsDF.loc[i,(r,'x')])
                sy.append(robotsDF.loc[i,(r,'y')])
            elif robotsDF.loc[i,(r,'state')] == 'go4litter':
                gx.append(robotsDF.loc[i,(r,'x')])
                gy.append(robotsDF.loc[i,(r,'y')])
        
#        print(littersDF[i])
        litterObjects = littersDF.loc[littersDF[i],['x','y']]
        litter_particles.set_data(litterObjects['x'],litterObjects['y'])
        litter_particles.set_markersize(2)
        
        time_text.set_text('{} seconds'.format(i))
        
        searching_particles.set_data(sx,sy)
        searching_particles.set_markersize(5)
        
        go4litter_particles.set_data(gx,gy)
        go4litter_particles.set_markersize(5)
        
        homing_particles.set_data(hx,hy)
        homing_particles.set_markersize(5)
        
        nest_particle.set_data([0],[0])
        nest_particle.set_markersize(10)
        
        rect.set_edgecolor('k')
        return searching_particles,go4litter_particles,homing_particles,nest_particle,time_text,rect
    
    ani = animation.FuncAnimation(fig,animationStep,frames=robotsDF.index,blit=True,init_func=init)
    plt.close()
    return ani


#animateForaging(robotsDF,littersDF,nestDF,foragingWayPointsDF.keys())
