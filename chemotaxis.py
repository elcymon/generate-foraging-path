import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
import pandas as pd

def animateChemotaxis(robotDF,xlength=50,ylength=50,tmin=0,tmax=20):
    colors = plt.cm.inferno(np.linspace(0,0.9,5))
    tmin = tmin
    tmax = tmax
    fig = plt.figure(figsize=(6,3))
    plt.tight_layout(pad=0)
    ax = fig.add_subplot(121,
                         xlim=(-xlength/2.0,xlength/2.0),\
                         ylim=(-ylength/2.0,ylength/2.0))
    
    turnProb_ax = fig.add_subplot(122,
                               xlim=(tmin,tmax),ylim=(0,0.03))
    turnProb_ax.set_xlabel('Time')
    turnProb_ax.set_ylabel('Turn Probability')
    turnProb_ax.set_xticks([])
    turnProb_ax.set_yticks([])
    
    ax.set_yticks([])
    ax.set_xticks([])
    
    turnProb, = turnProb_ax.plot([],[],color=colors[3])
    
    soundSourceParticle, = ax.plot([],[],'*',color=colors[2],markersize=5)
    robotParticle, = ax.plot([],[],'o',color=colors[1],markersize=5)
    rect = plt.Rectangle((-xlength/2.0,-ylength/2.0),
                         xlength,ylength,ec='none',lw=2,fc='none')
    ax.add_patch(rect)
    time_text = ax.text(0.02, 1.01, '', transform=ax.transAxes)
    
    def init():
        robotParticle.set_data([],[])
        soundSourceParticle.set_data([],[])
        time_text.set_text('')
        rect.set_edgecolor('none')
        
        turnProb.set_data([],[])
        return robotParticle,soundSourceParticle,rect,turnProb,time_text
    def animationStep(i):
        print(i)
        tmin,tmax = turnProb_ax.get_xlim()
        if i > 0.99 * (tmax - tmin):
            tmin += 1
            tmax += 1
            turnProb_ax.set_xlim(left=tmin,right=tmax)
        
        robotParticle.set_data([robotDF.loc[i,'x']],[robotDF.loc[i,'y']])
        robotParticle.set_markersize(5)
        
        turnProb.set_data([robotDF.loc[0:i,'t']],[robotDF.loc[0:i,'turnProb']])
        soundSourceParticle.set_data([-2],[0])
        rect.set_edgecolor('k')
        
        time_text.set_text('{} seconds'.format(i))
        return robotParticle,soundSourceParticle,rect,turnProb,time_text
    
    ani = animation.FuncAnimation(fig,animationStep,frames=robotDF.index,
                                  blit=True,init_func=init)
    plt.close()
    return ani
def loadDF(filename):
    df = pd.read_csv(filename,sep=',|:',engine='python')
    
    return df[['t','x','y','turnProb']]
if __name__ == '__main__':
    filename = 'icra2020/simVideos/attraction/42-RepAtt-Noise0pct-qsize1-2019-01-31--23-54-09_m_4wrobot1.txt'
    df = loadDF(filename)
    ani = animateChemotaxis(df,xlength=6,ylength=6,tmin=0,tmax=20)
    ani.save(filename[:-3] + 'mp4',fps=20,dpi=300)