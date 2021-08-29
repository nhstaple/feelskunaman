from helpers.affect.scherer import Scherer
import matplotlib.pyplot as plt
import random
import seaborn as sns
import mplcursors
sns.set_theme(style="darkgrid")

ALPHA_SONG = 0.66
ALPHA_CENTER = 0.80
ALPHA_RINGS = 0.33

SIZE_SONG = 33
SIZE_CENTER = 66

def DrawVectors(title: str, vectors: list, data: list):
    X: list = []
    Y: list = []
    n = len(vectors)
    # arrows first
    if n == 1:
        for i in range(0, len(vectors)):
            v = vectors[i]
            vector:float = v.getVector()
            plt.arrow(
                x=0, y=0, dx=vector.item(0), dy=vector.item(1),
                color='black', alpha=0.33,
                width=7.5e-3, length_includes_head=True,
                label=''
            )

    # plot individual songs
    center = [0, 0]
    ax = 0
    for i in range(0, n):
        v = vectors[i]
        x, y = v.getComponents()
        X.append(x) ; Y.append(y)
        center[0] = center[0] + x
        center[1] = center[1] + y
        
        angle = v.getDeg()

        song = data[i]
        artist:str = song['artist']
        name:str = song['name']
        label = '{0:s}\n{1:s}\nvalence: {3:5.2f}\narousal: {4:5.2f}\n{2:5.2f}°'.format(name, artist, angle, x, y)
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

    # mean
    if n > 1:
        center = Scherer(center[0] / n, center[1] / n)
        mean_x, mean_y = center.getComponents()
        ax = sns.scatterplot(
            x=[ mean_x ],
            y=[ mean_y ],
            label='center\nvalence: {0:5.2f}\narousal: {1:5.2f}\n{2:5.2f}°'.format(mean_x, mean_y, center.getDeg()),
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
    plt.title(title, loc='center')

    # resizing
    plt.rcParams["figure.figsize"] = (20, 20)
    pos = ax.get_position() 
    pos = [pos.x0, pos.y0 - 0.05,  pos.width, pos.height] 
    ax.set_position(pos)
    ax.set_aspect('equal')
    
    # figure labels
    ax.set_xlabel(xlabel='valence')
    plt.annotate('happy', xy=(1.15, 0))
    plt.annotate('sad', xy=(-1.15, 0))
    ax.set_ylabel(ylabel='arousal')
    plt.annotate('awake', xy=(0, 1.15))
    plt.annotate('asleep', xy=(0, -1.15))

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

    plt.show()
    return

