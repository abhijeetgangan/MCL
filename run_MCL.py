import numpy as np
import matplotlib.pyplot as plt

from functools import partial
from src.util import particle_samples, plot_particle_samples, save_gif_PIL, resample_fn
from src.robot_motion import robot
from src.lidar import lidar_fn
from pathlib import Path

def MCL_event(map, r1, ax, nparticles, nlaserbeam, viz, files, low, high, fname, event):
    global particles, l

    particles_move = particles.copy()

    if event.key=="d":
        l += 1
        r1.move_fwd()
        particles_move[:,1] = particles_move[:,1] + 0.05

    elif event.key=="c":
        l += 1
        r1.move_back()
        particles_move[:,1] = particles_move[:,1] - 0.05

    elif event.key=="x":
        l += 1
        r1.move_left()
        particles_move[:,0] = particles_move[:,0] - 0.05

    elif event.key=="v":
        l += 1
        r1.move_right()
        particles_move[:,0] = particles_move[:,0] + 0.05

    pos = np.array([r1.x, r1.y, 1])
    ax.clear()
    lidardata = lidar_fn(map, pos, nlaserbeam, ax, viz)    

    lidardatapart = np.zeros((nparticles, nlaserbeam))
    for k in range(particles_move.shape[0]):
        if (particles_move[k,0] > 0 and particles_move[k,0] < 2 and particles_move[k,1] > 0 and particles_move[k,1] < 1):
            pos1 = np.array([particles_move[k,0],particles_move[k,1],1])
            lidardatapart[k,:] = lidar_fn(map, pos1, nlaserbeam, ax, False)
    
    rmse = np.zeros(nparticles)
    for j in range(particles_move.shape[0]):
        if (0 < particles_move[j,0] < 2) and (0 < particles_move[j,1] < 1):
            rmse[j] = np.sqrt(np.sum((lidardata[1:] - lidardatapart[j,1:]) ** 2) / lidardatapart.shape[1])
        else:
            rmse[j] = 1000

    plot_particle_samples(particles_move[rmse != 1000], ax, size=1, axis=True)
    plt.xlim(-0.1,2.1)
    plt.ylim(-0.1,1.1)
    file = fname+"%.8i.png"%(l+1)
    plt.savefig(file, bbox_inches='tight', pad_inches=0.1, dpi=100, facecolor="white")
    files.append(file)

    missing_part = np.count_nonzero(rmse == 1000)
    keep_part =  int(nparticles / 2)

    new_particles = np.zeros((missing_part + keep_part, 2))
    score = 1 / rmse

    sample_idx = np.argpartition(score,-(missing_part + keep_part))[-(missing_part + keep_part):]

    new_particles = resample_fn(missing_part + keep_part, new_particles, particles_move, sample_idx, 'normal')

    particles_move = np.concatenate((particles_move[sample_idx], new_particles), axis=0)

    if particles_move.shape != particles.shape:
        diff = particles.shape[0] - particles_move.shape[0]
        resampled_particles = particle_samples(diff, low, high)
        particles_move = np.concatenate((particles_move, resampled_particles), axis=0)
        particles = particles_move
    else:
        particles = particles_move
    
    plt.show()



#  Configuration variables
nlaserbeam = 15
nparticles = 300
particles = np.zeros((nparticles, 2))
    
# Map defined as lines in x1,y1,x2,y2 format
map = np.array([[0,0,0,1],
                [0,1,2,1],
                [0,0,2,0],
                [2,1,2,0],
                [0,0.75,0.75,0.75],
                [0.75,0.25,1.5,1.0],
                [1.5,0.5,2,0]])
    
fig, ax = plt.subplots()

low = np.array([0 + 0.05, 0 + 0.05])
high = np.array([2 - 0.05, 1 - 0.05])
files = []

particles = particle_samples(nparticles, low, high)
plot_particle_samples(particles, ax, size=1.0, axis=True)
plt.xlim(-0.1,2.1)
plt.ylim(-0.1,1.1)

r1 = robot(0.15,0.4)
pos = np.array([r1.x,r1.y,1])
l = 0 
viz = True
fname = "MCL"
lidardata = lidar_fn(map, pos, nlaserbeam ,ax ,viz)

on_move = partial(MCL_event, map, r1, ax, nparticles, nlaserbeam, viz, files, low, high, fname)
binding_id = plt.connect('key_press_event', on_move)
plt.show()

save_gif_PIL(fname+".gif", files, fps=10, loop=0)

# Delete png files after gif is created
for filename in Path(".").glob(fname+"*.png"):
    filename.unlink()