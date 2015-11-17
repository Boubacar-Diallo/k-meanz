#!/usr/bin/env python
###############################################################################
#
# k_means.py - Implement k-means clustering on image data!
#
###############################################################################
# #
# This program is free software: you can redistribute it and/or modify #
# it under the terms of the GNU General Public License as published by #
# the Free Software Foundation, either version 3 of the License, or #
# (at your option) any later version. #
# #
# This program is distributed in the hope that it will be useful, #
# but WITHOUT ANY WARRANTY; without even the implied warranty of #
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the #
# GNU General Public License for more details. #
# #
# You should have received a copy of the GNU General Public License #
# along with this program. If not, see <http://www.gnu.org/licenses/>. #
# #
###############################################################################

__author__ = "Miriam Shiffman"
__copyright__ = "Copyright 2015"
__credits__ = ["Miriam Shiffman"]
__license__ = "GPL3"
__version__ = "0.0.1"
__maintainer__ = "Miriam Shiffman"
__email__ = ""
__status__ = "Development"

###############################################################################

import numpy as np
from PIL import Image
import random
from itertools import chain, izip
import code

###############################################################################
###############################################################################
###############################################################################
###############################################################################

class kmeans():
    """Cluster pixels by k means algorithm"""
    def __init__(self, filepath, k = 10):
        self.img = Image.open(filepath)
        self.img.show()
        self.k = k
        self.arr = np.array(self.img)
        #TODO: figure out how to sample from generator/iterable
        # pixel map is m x n array (row by column rather than x & y)
        # randint includes top end of range, so subtract 1
        self.k_lst = [ ( random.randint(0, self.arr.shape[0]-1), random.randint(0, self.arr.shape[1]-1) ) \
                       for _ in xrange(self.k) ]
        # check to see that two random k points are not identical
        while len(set(self.k_lst)) < self.k:
            self.k_lst.append( (random.randint(0, self.arr.shape[0]-1), random.randint(0, self.arr.shape[1]-1)) )
        self.__initialize_k_dict__(self.k_lst)


    def __initialize_k_dict__(self, k_vals):
        """Generate dictionary of k clusters based on list of (x,y) tuples for k means"""
        # Initialize k clusters with pixels in group, starting with points representing k clusters themselves
        # must convert np array to hashable type (tuple) for key
        self.d_k_clusters = { tuple(self.mn2mnrgb(t_mn)): [ self.mn2mnrgb(t_mn) ] for t_mn in k_vals }


    def minimize_distance(self, pixel, metric):
        """Given tuple representing pixel in image, return k group that minimizes distance by given metric"""
        dists = [ (k, metric(np.array(pixel), np.array(k))) for k in self.d_k_clusters.iterkeys() ]
        # find tuple representing best k group by minimizing distance
        best_k, _ = sorted( dists, key = lambda t: t[1] )[0]
        return best_k


    def mn2mnrgb(self, t_mn):
        """Given (m,n) of pixel, returns np array of [ m, n, R, G, B ]"""
        return np.append(t_mn, self.arr[t_mn[0], t_mn[1]])


    def assign_pixels(self, metric):
        """Assign all pixels in image to closest matching group in self.d_k_groups, according to given distance metric"""
        print 'assigning pixels'

        #for i,t in enumerate(( (m,n) for m in xrange(0, self.arr.shape[0]) for n in xrange(0, self.arr.shape[1]) )):
            ## convert (m, n) of pixel location to ((m, n), (r, g, b))
            #tval = self.mn2mnrgb(t)
            ## append to dictionary value list corresponding to key of k-mean that minimizes distance by given metric
            #self.d_k_clusters[ self.minimize_distance( tval, metric ) ].append(tval)
            #print '{}/{}'.format(i, self.arr.shape[0]*self.arr.shape[1])

        #TODO: implement itertools.groupby before appending to dictionary ??
        #clusters = []
        #data = sorted()

        # try iterating over numpy array by adding multi-index to nditer
        it = np.nditer(self.arr, flags=['multi_index'])
        tval = []
        while not it.finished:
            # it.multi_index yields (i, j, index of RGB val) - where index is 0,1,2
            # it[0] at that index yields array(value, dtype=uint8)
            # tval = [m,n] + [R,G,B]
            # tval = [i for i in it.multi_index] + [v for v in it[0]]
            i, j, rgb_i = it.multi_index
            # initialize tval with i,j position in array
            if rgb_i == 0:
                tval = [i, j]
            tval.append(int(it[0]))
            # end of R,G,B values corresponding to that position i,j in array
            if rgb_i == 2:
                # update cluster dictionary with tval and clear for next value
                self.d_k_clusters[ self.minimize_distance( tval, metric ) ].append(tval)
                tval = []
            it.iternext()


    def generate_image(self, warholize=False):
        """Once all pixels have been assigned to k clusters, use d_k_clusters to generate image data, with new pixel values determined by mean RGB of the cluster, or random color palette if warholize=True"""
        self.new_arr = np.empty(self.arr.shape)

        def mean_rgb(k):
            """Given key value in self.d_k_clusters, return k mean by averaging (r,g,b) value over all values in group"""
            val_arr = np.array(self.d_k_clusters[k])
            print "val_arr is {}".format(val_arr)
            return tuple(int(val) for val in np.mean(val_arr, axis=0))

        if warholize:
            random_colors = random_color_palette(self.k)

        print 'putting pixels'

        for i, (k, v_list) in enumerate(self.d_k_clusters.iteritems()):
            print '.'
            pixelval = ( random_colors[i] if warholize else mean_rgb(k) )

            for t_mn, _ in v_list:
                self.new_arr[t_mn[0], t_mn[1]] = pixelval

        self.new_img = Image.fromarray(self.new_arr)
        self.new_img.show()


###############################################################################
###############################################################################
###############################################################################
###############################################################################


def euclidean_dist_np(p1,p2):
     """Compute Euclidean distance between 2 pts (np arrays) of any (equal) dimensions
     using numpy's Linear Alg norm
    IN: two np arrays
    OUT: float"""
     return np.linalg.norm(p1-p2)


# inspired by http://martin.ankerl.com/2009/12/09/how-to-create-random-colors-programmatically/
def random_color_palette(n, RGB=True):
    """Generates a random, aesthetically pleasing set of n colors (list of RGB tuples if RGB; else HSV)"""
    SATURATION = 0.6
    VALUE = 0.95
    GOLDEN_RATIO_INVERSE = 0.618033988749895

    # see: https://en.wikipedia.org/wiki/HSL_and_HSV#Converting_to_RGB
    def hsv2rgb(hsv):
        h, s, v = hsv
        # compute chroma
        c = v*s
        h_prime = h*6.0
        x = c*( 1 - abs(h_prime %2 - 1) )
        if h_prime >= 5: rgb = (c,0,x)
        elif h_prime >= 4: rgb = (x,0,c)
        elif h_prime >= 3: rgb = (0,x,c)
        elif h_prime >= 2: rgb = (0,c,x)
        elif h_prime >= 1: rgb = (x,c,0)
        else: rgb = (c,x,0)
        m = v-c
        return tuple( int(255*(val+m)) for val in rgb )

    # random float in [0.0, 1.0)
    hue = random.random()
    l_hues = [hue]

    for i in xrange(n-1):
        # generate evenly distributed hues by random walk using the golden ratio!
        # (mod 1, to stay within hue space)
        hue += GOLDEN_RATIO_INVERSE
        hue %= 1
        l_hues.append(hue)

    if not RGB:
        return [ (h, SATURATION, VALUE) for h in l_hues ]

    return [ hsv2rgb((h, SATURATION, VALUE)) for h in l_hues ]


#@profile
def implement(infile, k, warholize=False):
    x = kmeans(infile, k=k)
    x.assign_pixels(metric=euclidean_dist_np)
    x.generate_image(warholize=warholize)

FILE_IN = '/Users/miriamshiffman/Desktop/Pics/Art/sc236393.jpg'
K=40

if __name__ == "__main__":
    implement(FILE_IN, K)
