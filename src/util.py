# Utility functions

import numpy as np
from PIL import Image

def norm_homo_fn(pos):
    """
    Calculates the normalised positions for the homogeneous coordinates
    
    Args:
        pos: positions in homogeneous coordinates
    Returns:
        pos: normalised positions with k = 1
    """
    if (pos[2]!=0):
        pos = pos/pos[2]
    return(pos)

def distance_fn(P_1, P_2):
    """
    Calculates the distance between two points

    Args:
        P_1 : point [x_1,y_1]
        P_2 : point [x_2,y_2]
    Retuns:
        distance: eucledean distance
    """
    return np.sqrt((P_1[0] - P_2[0])**2  + (P_1[1] - P_2[1])**2)

def particle_samples(nparticles, low, high):
    """
    Random uniform sampling of particles across the map

    Args:
        nparticles: Number of particles for particle filter
        low: lower bound of map
        high: upper bound of map
    Returns:
        particle positions: 2D positions of particles
    """
    return np.random.uniform(low, high, size=(nparticles,2))

def resample_fn(missing_part, new_particles, particles_move, sample_idx, distribution):
    """
    Resample the particles

    Args:
        keep_part: Number of missing particles
        new_particles: Array of new particles
        particles_move: particle positions
        sample_idx: Particles id to sample
        distribution: type of distribution 'random_uniform' or 'normal'
    Returns:
        resampled particle: Positions of resamples particles
    """
    for i in range(missing_part):
        x, y = particles_move[sample_idx[i]]
        if distribution == 'random_uniform':
            low_p = np.array([ x - 1e-2, y - 1e-2])
            high_p = np.array([ x + 1e-2, y + 1e-2])
            new_particles[i] = particle_samples(1, low_p, high_p)
        elif distribution == 'normal':
            mean = np.array([x, y])
            covariance = np.diag([1e-4,1e-4])
            new_particles[i] = np.random.multivariate_normal(mean, covariance, size=1)
    return new_particles

def plot_particle_samples(R, ax, size=2, limits=False, grid=False, axis=True):
  """Helper function to plot partilce samples"""
  ax.scatter(R[:, 0], R[:, 1], alpha=0.3, s=size * 20, c='blue')
  
  if limits:

    minRx = np.min(R[:, 0]); minRy = np.min(R[:, 1]);
    maxRx = np.max(R[:, 0]); maxRy = np.max(R[:, 1]);
    
    totalx = maxRx - minRy
    totaly = maxRy - minRy

    ax.set_xlim([minRx - totalx / 10, maxRx + totalx / 10])
    ax.set_ylim([minRy - totaly / 10, maxRy + totaly / 10])
  
  if grid:
    ax.grid(grid)

  if not axis:
    ax.axis("off")

def save_gif_PIL(outfile, files, fps=5, loop=0):
    "Helper function for saving GIFs"
    imgs = [Image.open(file) for file in files]
    imgs[0].save(fp=outfile, format='GIF', append_images=imgs[1:], save_all=True, duration=int(1000/fps), loop=loop)