from argparse import HelpFormatter
from helpers.affect.scherer import Emotive2D, EPosition, VALENCE_RIGHT, VALENCE_LEFT, AROUSAL_UP, AROUSAL_DOWN
import matplotlib.pyplot as plt
import random
from helpers.objects.track import Track
import seaborn as sns
import mplcursors
sns.set_theme(style="darkgrid")

ALPHA_SONG = 0.66
ALPHA_CENTER = 0.80
ALPHA_RINGS = 0.33

SIZE_SONG = 33
SIZE_CENTER = 66

def DrawVectors(title: str, vectors: list, data: list, normalize: bool):
    X: list = []
    Y: list = []
    n = len(vectors)
    instances = [0, 0, 0, 0]

    # plot individual songs
    center = [0, 0]
    ax = 0
    i = 0
    for v in vectors[0:n]:            
        quad: EPosition = v.getPosEncoding()
        if quad == EPosition.QUAD1:
            instances[0] = instances[0] + 1
        elif quad == EPosition.QUAD2:
            instances[1] = instances[1] + 1
        elif quad == EPosition.QUAD3:
            instances[2] = instances[2] + 1
        else:
            instances[3] = instances[3] + 1
        
        if normalize:
            v.normalize(set=True)
        
        x, y = v.getValues()
        strength = v.getIntensity()
        X.append(x) ; Y.append(y)
        center[0] = center[0] + x
        center[1] = center[1] + y
        
        angle = float(v.getDirection(rad=False))
        song:Track = data[i]
        artist:str = song.artist
        name:str = song.name
        label = '{0:s}\n{1:s}\nvalence: {3:5.2f}\narousal: {4:5.2f}\nintensity: {5:5.2f}\n{2:5.2f}°'.format(name, artist, angle, x, y, strength)
        ax = sns.scatterplot(
            x=[x],
            y=[y],
            label=label,
            legend=False,
            alpha=ALPHA_SONG,
            marker= random.sample(['v', '^'], 1)[0],
            s=SIZE_SONG,
            edgecolor='black'
        )
        i = i + 1
    # endfor

    # mean
    if n > 1:
        center = Emotive2D(center[0] / n, center[1] / n)
        if normalize: center.normalize(set = True)
        mean_x, mean_y = center.getValues()
        ax = sns.scatterplot(
            x=[ mean_x ],
            y=[ mean_y ],
            label='center\nvalence: {0:5.2f}\narousal: {1:5.2f}\nintensity: {3:5.2f}\n{2:5.2f}°'.format(mean_x, mean_y, center.getDirection(), center.getIntensity()),
            legend=False,
            alpha=ALPHA_CENTER,
            edgecolor='red',
            color='black',
            s=SIZE_CENTER
        )

    # unit circle
    ax.add_patch(plt.Circle((0, 0), radius=0.25, edgecolor='black', facecolor='None', alpha=ALPHA_RINGS, label='r=0.25'))
    ax.add_patch(plt.Circle((0, 0), radius=0.50, edgecolor='black', facecolor='None', alpha=ALPHA_RINGS, label='r=0.50'))
    ax.add_patch(plt.Circle((0, 0), radius=0.75, edgecolor='black', facecolor='None', alpha=ALPHA_RINGS, label='r=0.75'))
    ax.add_patch(plt.Circle((0, 0), radius=1.00, edgecolor='black', facecolor='None', alpha=ALPHA_RINGS, label='r=1.00'))

    # title
    plt.title(title + '\nN = {}'.format(n), loc='center')

    # axi
    plt.ylabel('valence')
    plt.xlabel('arousal')

    # resizing
    plt.rcParams["figure.figsize"] = (20, 20)
    pos = ax.get_position() 
    pos = [pos.x0, pos.y0 - 0.05,  pos.width, pos.height] 
    ax.set_position(pos)
    ax.set_aspect('equal')
    
    # figure labels
    plt.annotate(VALENCE_RIGHT, xy=(1.15, 0))
    plt.annotate(VALENCE_LEFT, xy=(-1.15, 0))
    plt.annotate(AROUSAL_UP, xy=(0, 1.15))
    plt.annotate(AROUSAL_DOWN, xy=(0, -1.15))

    # annotations
    def on_click(sel):
        label = sel.artist.get_label()
        if label: sel.annotation.set_text(label)
    mplcursors.cursor(highlight=True).connect('add', on_click)

    # tweak aesthetic
    plt.tick_params(
        axis='both',
        which='both',
        bottom=False,
        top=False,
        labelbottom=False,
        right=False,
        left=False,
        labelleft=False
    )
    ax.minorticks_off()
    ax.grid(False)

    # origin
    ax.axhline(y=0, color='k')
    ax.axvline(x=0, color='k') 

    # tweak bounds
    ax.set(xlim=(-1, 1))
    ax.set(ylim=(-1, 1))
    ax.set_xbound(lower=-1.30, upper=1.30)
    ax.set_ybound(lower=-1.30, upper=1.30)

    # class instances
    most_instances = instances.index(max(instances))
    weights = ['normal', 'normal', 'normal', 'normal']
    colors = ['grey', 'grey', 'grey', 'grey']
    weights[most_instances] = 'bold'
    colors[most_instances] = 'black'

    plt.text(1, 1, str(instances[0]), horizontalalignment='left', size='medium',
        color=colors[0], weight=weights[0])
    
    plt.text(-1, 1, str(instances[1]), horizontalalignment='left', size='medium',
        color=colors[1], weight=weights[1])
    
    plt.text(-1, -1, str(instances[2]), horizontalalignment='left', size='medium',
        color=colors[2], weight=weights[2])
    
    plt.text(1, -1, str(instances[3]), horizontalalignment='left', size='medium',
        color=colors[3], weight=weights[3])
    
    plt.show()
    
    return