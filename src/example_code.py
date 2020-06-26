#import the necessary modules
from core import Ray, Boundary, intersection, prop 
import numpy as np
import math

#establish the ray, boundary with desired info
#for now, the start points must be <= the endpoints, directionality of the code is an unsolved issue
#horizontal lines are not yet supported for boundary!
#to see results, pick ray/boundary so that they will intersect

ray = Ray([0,0], np.pi/6, 10)
boundary = Boundary([-10, -10], [10, 10], .75, 2)

#find out where the ray and boundary intersect
x_int, y_int = intersection(ray, boundary)

#split the ray after collision with the boundary
reflected_ray, refracted_ray = ray.split(boundary, [x_int, y_int])

print(reflected_ray.brightness)

#this will give you the corresponding ray info for the reflected & refracted rays after interaction with the first boundary
#required info can be accessed through the ray class, ex: reflected_ray.brightness()

#this is an unfinished build of core.py
#the finished version would ideally require the definition of parameters for ray/boundary, 
#and the rest would be automated through prop(ray)


