from helpers.affect.scherer import Scherer2D
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

def DrawVectors(title: str, vectors: list, data: list, drawArrow: bool = False):
    X: list = []
    Y: list = []
    n = len(vectors)
    # arrows first
    if n == 1 and drawArrow:
        for i in range(0, len(vectors)):
            v:Scherer2D = vectors[i]
            valence, arousal = v.getValues()
            plt.arrow(
                x=0, y=0, dx=valence, dy=arousal,
                color='black', alpha=0.33,
                width=7.5e-3, length_includes_head=True,
                label=''
            )

    # plot individual songs
    center = [0, 0]
    ax = 0
    for i in range(0, n):
        v = vectors[i]
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

    # mean
    if n > 1:
        center = Scherer2D(center[0] / n, center[1] / n)
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
    plt.title(title, loc='center')

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
    plt.annotate('happy', xy=(1.15, 0))
    plt.annotate('sad', xy=(-1.15, 0))
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