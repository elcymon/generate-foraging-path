# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
import matplotlib.animation as animation

def animateForaging(robotsDF,littersDF,nestDF,robots):
    fig = plt.figure(figsize=(10,10))
    
    ax = fig.add_subplot(111,aspect='equal',autoscale_on=False,xlim=(-25,25),ylim=(-25,25))
    searching_particles, = ax.plot([],[],'bo',markersize=5)
    homing_particles, = ax.plot([],[],'go',markersize=5)
    litter_particles, = ax.plot([],[],'ro',markersize=2)
    time_text = ax.text(0.02, 1.10, '', transform=ax.transAxes)
    nest_text = ax.text(0.02, 1.05, '', transform=ax.transAxes)

    rect = plt.Rectangle((-25,-25),50,50,ec='none',lw=2,fc='none')
    ax.add_patch(rect)
    def init():
        searching_particles.set_data([],[])
        homing_particles.set_data([],[])
        litter_particles.set_data([],[])
        time_text.set_text('')
        nest_text.set_text('')
        
        rect.set_edgecolor('none')
        return searching_particles,homing_particles,time_text,nest_text,rect
    
    def animationStep(i):
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
        
        ms = 5
        litterObjects = littersDF.loc[littersDF[i],['x','y']]
        litter_particles.set_data(litterObjects['x'],litterObjects['y'])
        litter_particles.set_markersize(int(ms/2))
        
        time_text.set_text('time = {} seconds'.format(nestDF.loc[i,'tPlusProcessing']))
        nest_text.set_text('litter in nest = {}'.format(nestDF.loc[i,'litterCount']))
#        print(x)
#        print(y)
        searching_particles.set_data(sx,sy)
        searching_particles.set_markersize(ms)
        
        homing_particles.set_data(hx,hy)
        homing_particles.set_markersize(ms)
        
        rect.set_edgecolor('k')
        return searching_particles,homing_particles,time_text,nest_text,rect
    ani = animation.FuncAnimation(fig,animationStep,frames=robotsDF.index,blit=True,init_func=init)
    plt.close()
    return ani
        
#animateForaging(robotsDF,littersDF,nestDF,foragingWayPointsDF.keys())
