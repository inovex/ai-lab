import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as mc

def plot_values(V, title='State-Value Function'):
    V = np.reshape(V, (4,12))
    fig = plt.figure(figsize=(15,5))
    ax = fig.add_subplot(111)
    im = ax.imshow(V, cmap='cool')
    for (j,i),label in np.ndenumerate(V):
        ax.text(i, j, np.round(label,3), ha='center', va='center', fontsize=14)
    plt.tick_params(bottom='off', left='off', labelbottom='off', labelleft='off')
    plt.title(title)
    plt.show()

def visualize_samples(samples, discretized_samples, grid, low=None, high=None, x_label='', y_label=''):
    assert len(low) == len(high), 'Dimensions of low and high should be equal'
    
    fig, ax = plt.subplots(figsize=(10, 10))
    
    ax.xaxis.set_major_locator(plt.FixedLocator(grid[0]))
    ax.yaxis.set_major_locator(plt.FixedLocator(grid[1]))
    ax.grid(True)
    ax.set_xlabel(x_label)
    ax.set_ylabel(y_label)
    ax.set_title('Discretization')
    
    if low is not None and high is not None:
        ax.set_xlim(low[0], high[0])
        ax.set_ylim(low[1], high[1])
    else:
        low = [splits[0] for splits in grid]
        high = [splits[-1] for splits in grid]
        
    # Map discretized samples to corresponding grid cell
    grid_extended = np.hstack((np.array([low]).T, grid, np.array([high]).T))
    grid_centers = (grid_extended[:, 1:] + grid_extended[:, :-1]) / 2
    locs = np.stack(grid_centers[i, discretized_samples[:, i]] for i in range(len(grid))).T

    ax.plot(samples[:, 0], samples[:, 1], 'o') # plot original samples
    ax.plot(locs[:, 0], locs[:, 1], 's') # plot discretized samples in mapped locations
    ax.add_collection(mc.LineCollection(list(zip(samples, locs)), colors='orange'))
    ax.legend(['original', 'discretized'])

def plot_statistics(statistics, y_limits=None, open_window=False):
    x = [statistic['episode'] for statistic in statistics]
    y = [statistic['score'] for statistic in statistics]

    mean = np.mean(y)

    fig, ax = plt.subplots()
    if y_limits:
        ax.set_ylim(y_limits)

    ax.plot(x, y, label="scores")
    ax.plot(x, [mean] * len(x), label=f'mean {mean}')

    ax.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)

    plt.show(block=open_window)
    plt.close('all')
