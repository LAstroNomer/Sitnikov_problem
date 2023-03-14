from scipy.integrate import solve_ivp
from matplotlib import pyplot as plt
from pathlib import Path
#from nolds import lyap_r
from tqdm import tqdm
from time import time

import multiprocessing
import numpy as np
import subprocess
import warnings
import argparse
import json
import os


def kepler_solve(t, n=1, t0=0.0,  eps=10**(-14)):

    M = n*(t-t0)
    E   = M
    E_1 = E + 1
    
    while (E_1 - E) > eps:
        E_1 = E
        E = M + _e*np.sin(E_1)
        
    return E


#--------------------------------------------------------------------------------
def motion(E, y):
    z = y[0]
    v = y[1]

    r = 0.5*(1 - _e*np.cos(E))

    dz = 2*r*v

    dv = -2*r*z/((r**2 + z**2)**(3/2))
    return np.array([dz, dv])


#--------------------------------------------------------------------------------
def solve_array(h, v, e0, t_eval, atol=10**(-13), rtol=10**(-13), method='DOP853'):
    e = e0
    y0 = [h, v]

    sol = solve_ivp(motion,[0, np.max(t_eval)], y0, method=method,
    rtol=rtol, atol=atol, t_eval=t_eval)

    return sol


#--------------------------------------------------------------------------------
# def draw_lay(args):    
#    file = args[0]
#    path = args[1]
#    color = args[2]
#    print(file)
#    with open(path+'/'+file,'r') as inp:
#            for line in inp.readlines()[2:]:
#                x, y = map(float, line.split())
#                plt.plot(x, y,'o', markersize=0.2, color=color)
#
#--------------------------------------------------------------------------------
class Sitnikov():

    def __init__(self, e, h, n_rot=100, atol=10**(-5), rtol=10**(-5), method='DOP853'):
    
        self.e = e
        if abs(e) >= 1:
            print('Wrong e')
            os._exit(1)
        global _e
        _e = e
        self.h = h
        self.v = 0.0
        self.nrot = n_rot
        self.atol = atol
        self.rtol = rtol
        self.method = method
        self.sol = None

    #--------------------------------------------------------
    def solve(self, tmax, step):
        t = np.arange(0, tmax, step)
        
        t_eval = list(map(kepler_solve, t))
        sol = solve_array(self.h, self.v, self.e, t_eval, self.atol, self.rtol, self.method)
        E = sol.t
        Z = sol.y[0]
        dZ = sol.y[1] 
        r = 0.5*(1 - self.e*np.cos(E))
        return t, Z, dZ/r
    #----------------------------------------------------

    def solve_phase_portrait(self, h_):
        h = h_
    
        t_eval = np.arange(0, self.nrot*2*np.pi, 2*np.pi)
        #print(np.max(t_eval)/2/np.pi)
        sol = solve_array(h, self.v, self.e, t_eval, atol=self.atol,
                                         rtol=self.rtol, method=self.method)
        E = sol.t
        Z = sol.y[0]
        dZ = sol.y[1] 
        r = 0.5*(1 - self.e*np.cos(E))
    
        return Z, dZ/r/2


    #---------------------------------------------------

    def plot_phase_portrait(self, path,  files, name, io_key, out_dir, xlim=(-3,3), ylim=(-2,2), color='r'): 
        
        e_val = name.split('e')[1]
        plt.title('e = %s' %e_val)
        good = []
        for file in files:
            if file.__contains__(name+'_'+io_key):
                 good.append(file)

        for i in tqdm(range(len(good))):
            file = good[i]
            #with open(path+'/'+file,'r') as inp:
            with open(Path(path,file),'r') as inp:
                for line in inp.readlines()[2:]:
                    x, y = map(float, line.split())
                    plt.plot(x, y,'o', markersize=0.2, color=color)
        #with multiprocessing.Pool(1) as pool:
        #pool.map(draw_lay, list(product(good, [path], [color])))


        plt.xlabel(r'$Z$')
        plt.ylabel(r'$V_z$')
        #plt.gca().axis('equal')
        plt.xlim(xlim)
        plt.ylim(ylim)
        plt.tight_layout()        
        plt.savefig(Path(out_dir, name+'.png'))
        plt.close()
        #plt.show()
        return
    #---------------------------------------------------

    '''
    def plot_stroboscopic_map(self, file=None, ylim=(-2,2)): 
        plt.figure()
        t_eval = np.arange(0, self.nrot*2*np.pi, 0.1)
        sol = solve_array(self.h, self.v, self.e, t_eval, atol=self.atol,
                                             rtol=self.rtol, method=self.method)
        plt.plot([x%(2*np.pi) for x in sol.t], sol.y[0], 'gs', markersize = 2)
        plt.xlabel(r'$E$')
        plt.ylabel(r'$Z$')
        #plt.xlim((0, 2*np.pi))
        #plt.ylim(ylim)
        plt.tight_layout()
        
        if file is None:
            plt.savefig('strob.png')
            plt.show()
        else:
            plt.savefig(file)
        return
    '''

    #---------------------------------------------------
    #def plot_lyap_map(self):
    #    
    #    t = np.arange(0, 200*2*np.pi, 0.1)
    #    t_eval = list(map(kepler_solve, t))
    #    len_e = np.arange(0, 0.9, 0.01)
    #    len_h = np.arange(1, 4, 0.01)
    #    maps = np.zeros((len(len_e), len(len_h)))
    #    for i in range(len(len_e)):
    #        for j in range(len(len_h)):
    #            #print(i, j)
    #            sol = solve_array(len_h[j], self.v, len_e[i], t_eval, atol=self.atol,
    #                                         rtol=self.rtol, method=self.method)


    #            with warnings.catch_warnings():
    #                warnings.simplefilter("ignore")
    #                l = lyap_r(sol.y[0])
    #            #print(l)
    #            maps[i, j] = np.log(l)
    #    
    #    plt.figure()
    #    plt.imshow(maps, origin='lower')
    #    plt.colorbar()
    #    plt.xlabel("Z")
    #    plt.ylabel("e")
    #    plt.savefig("map.png")
    #    return 
    #---------------------------------------------------
#---------------------------------------------------------------------------------------


