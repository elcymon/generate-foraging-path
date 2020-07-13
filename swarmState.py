import matplotlib.patches as mpatches
import matplotlib.pyplot as plt
from glob import glob
import pandas as pd
import ntpath
from matplotlib import gridspec

def name_image(filename):
    basename = ntpath.basename(filename)
    folder = filename.replace(basename,'')
    basename = basename.replace('_littersFile.csv','')
    if '100m' in filename:
        sz = '100m'
    else:
        sz = '50m'
    if 'Uniform' in filename:
        world='Uniform'
    elif 'OneCluster' in filename:
        world='OneCluster'
    elif 'TwoClusters' in filename:
        world = 'TwoClusters'
    elif 'FourClusters' in filename:
        world = 'FourClusters'
    elif 'HalfCluster' in filename: 
        world = 'HalfCluster'
        
    return f'{folder}{world}{sz}-{basename}'

def plotModelPose(filename,robotsdf,nestdf,littersdf,worldXlength,worldYlength,
                  pickedlitter=None,times=None):
    cmap = plt.get_cmap('inferno')
    fig = plt.figure(figsize=(12,12))
    n = 1
    if times is None:
        rows = pickedlitter
        col = 'pickedLitter'
    else:
        rows = times
        col = 'time'
    for r in rows:
        
#        plt.tight_layout(pad=0.1)
        if col == 'time':
            nlitter = nestdf.loc[nestdf.index >= r,:].head(1)
            p = nlitter.loc[r,'pickedLitter']
        else:
            nlitter = nestdf.loc[nestdf['pickedLitter']>=r,:].head(1)
            p = r
        
        t = nlitter.index[0]
        litters = littersdf.loc[['x','y',f'{t:.06f}'],:].dropna(axis=1)
#        litters  = litters.loc[:,litters.loc[f'{t:.06f}',:] > 0]
        robots = robotsdf.loc[t,:]
        robotstates = robots.xs('state',level=1)
        
        ax = fig.add_subplot(f'1{len(pickedlitter)}{n}',aspect='equal',autoscale_on=False,\
                         xlim=(-worldXlength/2.0,worldYlength/2.0),\
                         ylim=(-worldXlength/2.0,worldYlength/2.0))
        #plot litter
        ax.plot(litters.loc['x',:],litters.loc['y',:],'*',color=cmap(0.8),label='targets')
        
        #plot robots
        #SEARCHING
        ax.plot(robots.xs('x',level=1)[robotstates == 'searching'],
                robots.xs('y',level=1)[robotstates == 'searching'],
                'o',color=cmap(0.2),label='searching')
        #GO4LITTER
        ax.plot(robots.xs('x',level=1)[robotstates == 'go4litter'],
                robots.xs('y',level=1)[robotstates == 'go4litter'],
                's',color=cmap(0.4),label='acquiring')
        #HOMING
        ax.plot(robots.xs('x',level=1)[robotstates == 'homing'],
                robots.xs('y',level=1)[robotstates == 'homing'],
                'D',color=cmap(0.65),label='homing')
        #plot nest
        ax.plot([0],[0],'P',markersize=12,color=cmap(0),label='nest')
        ax.text(0.0,1.03,f'picked {p} in {round(t,-1):.0f}s',size=14,weight='bold',transform=ax.transAxes)
        
        n +=1
        ax.set_xticks([])
        ax.set_yticks([])
    plt.subplots_adjust(wspace=0.05,hspace=0)
    plt.legend(fontsize=14,loc='upper right',bbox_to_anchor=(1.79,1))
    figname = f'{name_image(filename)}'.replace('.','p') + '.pdf'
    fig.savefig(figname,bbox_inches='tight')
    plt.close(fig)

def swarmState():
#    folder = '/home/elcymon/containers/swarm_sim/results/alns-gazebo/*/*_001_*littersFile.csv'
    folder = '/media/elcymon/files/phd/swarm_sim/n0q1_scalability/try2/*/r*/*_001_*littersFile.csv'
    pickedlitters = [0,60,120,180]
    times = [49.975,99.975,149.975,199.975]
    for f in glob(folder):
        print(f)
        nestdf = pd.read_csv(f.replace('littersFile','nestFile'),index_col=0)
        robotsdf = pd.read_csv(f.replace('littersFile','robotsFile'),header=[0,1],index_col=0)
        littersdf = pd.read_csv(f,header=[0],index_col=0)
        if '100m' in f:
            worldXlength = 100
            worldYlength = 100
        else:
            worldXlength = 50
            worldYlength = 50
        plotModelPose(f,robotsdf,nestdf,littersdf,worldXlength,worldYlength,
                      pickedlitter=pickedlitters,times=times)
#        return
#        return nestdf,robotsdf,littersdf
if __name__ == '__main__':
    #nestdf,robotsdf,littersdf = \
    swarmState()