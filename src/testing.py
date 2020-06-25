from support import Ray, Boundary
import numpy as np
bound = Boundary([0,0],[3,3],.90, 1)
ray1 = Ray([0,0], np.pi/2, 1)

refl, refr = ray1.split(bound)
print(refl.brightness)
