# -*- coding: utf-8 -*-
"""
Created on Fri Jan  4 13:08:01 2019

@author: yuxinlin
"""
import numpy as np
import scipy.spatial
#3PCF (Takada & Jain 2008)


#NFW density profile

def nfw_rho_profile(r, rhos, ct, rvir, alpha=1):
    
    return rhos/((ct*r/rvir)**alpha*(1+ct*r/rvir)**(3-alpha))


def vec_length(vector):
    return np.linalg.norm(vector)


def unit_vector(vector):
    return vector / vec_length(vector)


def angle_between(v1, v2):
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))

def pairwise_angle(lines):
    angles = []
    for line in lines:
        a0, a1 = np.asarray(line[0])
        b0, b1 = np.asarray(line[1])
        angles.append(angle_between(a1-a0, b1-b0))
    return angles
    
class Image_statistic():
    def __init__(self, image, rms):
        
        self.data = image        
        self.noise_level = rms
        self.mean = np.nanmean(self.data[self.data>rms])
        self.index = np.where(self.data>rms)
        self.datalist = self.data[self.data>rms].ravel()
        self.tree = scipy.spatial.KDTree(zip(self.index[0].ravel(),self.index[1].ravel()))
        self.samples = {}
        self.twopt = {}
        self.threept_eqr_lines = {}
        
    def __len__(self):
        return len(self.data[self.data>self.noise_level])
        
    def all_pairs_rdr(self, rmin, rmax, dr):
        for r in np.arange(rmin, rmax, dr):
            lower = self.tree.query_pairs(r,)
            upper = self.tree.query_pairs(r+dr,)
            self.samples[r] = list(upper-lower)
            
    def twopt_simple(self):
        for pair in self.samples.iteritems():
            pair_sum = 0
            pair_num = len(pair[1])
            if pair_num > 0:
                for i in range(pair_num):
                    pair_sum += (self.datalist[pair[1][i][1]]/self.mean-1)*(self.datalist[pair[1][i][0]]/self.mean-1)
                self.twopt[pair[0]] = pair_sum/pair_num
    
    def threept_eqr(self, r, dr):
       triplets_all = []
       angles_all = []
       for ind in range(len(self.index[0])):
           lower = self.tree.query_ball_point((self.index[0][ind],self.index[1][ind]), r)
           upper = self.tree.query_ball_point((self.index[0][ind],self.index[1][ind]), r+dr)
           all_list = list(set(upper)-set(lower))
           if len(all_list)>2:
               triplets = np.hstack([np.asarray([(all_list[0],all_list[i+1],all_list[j]) for j in range(len(all_list))[i+2:]]).ravel() for i in range(len(all_list)-2)])
               triplets = triplets.reshape(-1,3)
               triplets_all.append(triplets)
               coords = [np.take(np.array(zip(self.index[0].ravel(),self.index[1].ravel())),trip_i,axis=0) for trip_i in triplets]
               print coords
               lines =  [[[coord[0],coord[i+1]] for i in range(len(coords[i])-1)] for coord in coords]
               angles = pairwise_angle(lines) #in radian unit
               angles_all.append(angles)
       self.triplets = np.concatenate(triplets_all)
       self.angles = np.concatenate(angles_all)
       triplets_groups = {}.fromkeys(np.unique(self.angles),[])
       for x,y in zip(self.angles,self.triplets):
           triplets_groups[x].append(y)
       return triplets_groups

        