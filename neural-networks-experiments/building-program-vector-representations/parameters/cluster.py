# -*- coding: utf-8 -*-
"""
Created on Mon Sep 08 22:07:44 2014

@author: limu
"""

from scipy.linalg import norm
from PIL import Image, ImageDraw,ImageFont
import scipy
#import pyparsing
import pylab
#import scipy.cluster.hierarchy as sch
ll = 105


def llf(id):
    return str(id)
def make_list(obj):
    if isinstance(obj, list):
        return obj
    return [obj]
 
class Node(object):
    def __init__(self, fea, gnd, left=None, right=None, children_dist=1, name=''):
        self.__name = name
        self.__fea = make_list(fea)
        self.__gnd = make_list(gnd)
        self.left = left
        self.right = right
        self.children_dist = children_dist
 
        self.depth = self.__calc_depth()
        self.height = self.__calc_height()
 
    def to_dendrogram(self, filename):
        
        height_factor = 20
        depth_factor = 20
        total_height = int(self.height*height_factor+20)
        total_depth = int(self.depth*depth_factor+50) + depth_factor
        im = Image.new('RGBA', (total_depth, total_height),(255,255,255))
        draw = ImageDraw.Draw(im)
        self.draw_dendrogram(draw, 15, total_height/2,
                             depth_factor, height_factor, total_depth,top = 1)
        #im.save(filename)
        #ttFont = ImageFont.truetype ('Cambria.ttc', 30)
        #draw.text ((10,10),'Token Clustering',fill=(0,0,0),font=ttFont)
        im.convert('P').save(filename)
        
    def my_to_dendrogram(self):
               
        fig = pylab.figure(figsize=(10,10))
        Y = sch.linkage(self, method='single')
        Z1 = sch.dendrogram(Y,leaf_label_func=llf,leaf_rotation=90)
        fig.show()
        fig.savefig('dendrogram.jpg')
         
 
    def draw_dendrogram(self,draw,x,y,depth_factor,height_factor,total_depth,top = 0):
        if self.is_terminal():
            #color_self = ((0,0,0), (0,0,0), (0,0,0))[int(self.__gnd[0])]
            color_self = ((0,0,0), (0,0,0), (0,0,0))[int(self.__gnd[0])]
            draw.line((x-ll, y, total_depth-150, y), fill=color_self,width = 2)
            # N.B. changing font is not working in my Linux 
            #ttFont = ImageFont.truetype ('Cambria.ttc', 18)
            #draw.text ((total_depth-140, y-11),self.__name,fill=(0,0,0) ,font=ttFont)
            draw.text ((total_depth-140, y-11),self.__name,fill=(0,0,0) )
            #draw.text ((total_depth-90, y-5),self.__name,fill=(0,0,0))
            return color_self
        else:
            
            y1 = int(y-self.right.height*height_factor/2)
            y2 = int(y+self.left.height*height_factor/2)
            xc = int(x + self.children_dist*depth_factor)
            color_left = self.left.draw_dendrogram(draw, xc, y1, depth_factor,
                                                   height_factor, total_depth)
            color_right = self.right.draw_dendrogram(draw, xc, y2, depth_factor,
                                                     height_factor, total_depth)
 
            left_depth = self.left.depth
            right_depth = self.right.depth
            sum_depth = left_depth + right_depth
            if sum_depth == 0:
                sum_depth = 1
                left_depth = 0.5
                right_depth = 0.5
            color_self = tuple([int((a*left_depth+b*right_depth)/sum_depth)
                                for a, b in zip(color_left, color_right)])
            draw.line((xc-ll, y1, xc-ll, y2), fill=color_self,width = 2)
            if top != 1:
                draw.line((x-ll, y, xc-ll, y), fill=color_self,width = 2)
            else:
                draw.line((5, y, xc-ll, y), fill=color_self,width = 3)
            return color_self
 
 
    # use Group Average to calculate distance
    def distance(self, other):
        return sum([norm(x1-x2)
                    for x1 in self.__fea
                    for x2 in other.__fea]) \
                / (len(self.__fea)*len(other.__fea))
 
    def is_terminal(self):
        return self.left is None and self.right is None
 
    def __calc_depth(self):
        if self.is_terminal():
            return 0
        return max(self.left.depth, self.right.depth) + self.children_dist
 
    def __calc_height(self):
        if self.is_terminal():
            return 1
        return self.left.height + self.right.height
 
    def merge(self, other, distance):
        return Node(self.__fea + other.__fea,
                    self.__gnd + other.__gnd,
                    self, other, distance)
 
 
def do_clustering(nodes):
    # make a copy, do not touch the original list
    nodes = nodes[:]
    while len(nodes) > 1:
        print "Clustering [%d]..." % len(nodes)
        min_distance = float('inf')
        min_pair = (-1, -1)
        for i in range(len(nodes)):
            for j in range(i+1, len(nodes)):
                distance = nodes[i].distance(nodes[j])
                if distance < min_distance:
                    min_distance = distance
                    min_pair = (i, j)
        i, j = min_pair
        node1 = nodes[i]
        node2 = nodes[j]
        del nodes[j] # note should del j first (j > i)
        del nodes[i]
        nodes.append(node1.merge(node2, min_distance))
    return nodes[0]
 
