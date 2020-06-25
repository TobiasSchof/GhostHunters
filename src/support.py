# A python script to hold the basic classes used in this package

class Ray:
    """ This class defines a single ray of light

    Parameters:
        start: [float, float] = the starting point of the ray
        anlge: [float, float] = angle of the ray in radians
        brightness: float     = the brightness of the ray (as a fraction of the original power) 

    Methods:
        split = splits this ray at a given Boundary
    """

    def __init__(self, start:list, angle:float, brightness:float):
        """ Constructor for the Ray class """
        
    def split(self, b:Boundary) -> (Ray, Ray):
        """ Splits this ray into two rays (one reflected, one refracted) at the given Boundary

        This method assumes that the given Boundary is intersected by this ray

        Inputs:
            b = the boundary for this ray to split at
        Returns:
            ray_refl = the refracted ray
            ray_refr = the reflected ray
        """
        import numpy as np
        refl_angle = self.angle + np.pi
        refr_angle = np.pi - np.asin(np.sin(self.angle)*(ref_idx_in/ref_index_out)
        #refl/refr angles are measured up from b, 
        #incoming angle is currently defiend up in the opposite direction
        ray_refl = Ray(b.start,refl_angle, self.brightness*(1-b.t_coeff))
        ray_refr = Ray(b.start,refr_angle, self.brightness*b.t_coeff)
        return ray_refl, ray_refr


class Boundary:
    """ This class defines a Boundary between air and another medium

    Parameters:
        start:     [float, float] = the start of the line segment defining this barrier
        end:       [float, float] = the end of the line segment defining this barrier
        t_coeff:   float          = the transmission coefficient of the barrier
        ref_idx:   float          = the refractive index of the other medium
        norm:      [float, float] = the direction of the norm towards the air side
    """

    def __init__(self, start:list, end:list, t_coeff:float, ref_idx:float):
        """Constructor for the Boundary class"""
    def bound_line(self, start:list, end:list):
        """Defines the boundary lines of the material given its start and endpoints
        
        This method returns the equation of a line that defines the boundary
        """
        slope = (self.end[1]-self.start[1])/(self.end[0]-self.start[0])
        intercept = self.end[1]-slope*end[0]

        """



        This is a test commit
        
        
        """


def intersection(ray, boundary):
    """This function determines when a propogating ray intersects with a given boundary

    Inputs:
        ray             = 
        boundary        = 
    Returns:
        intersect: list = the point of intersection


    """

def prop(ray, threshold):
    """This function applies split on a ray while the brightness is still greater than threshold value

    Inputs:
        ray = incident ray on a surface that will be reflected and refracted
        threshold = minimum brightness value that will stop prop
    Returns:

    """
    ray_list=[];
    if ray.brightness <= threshold:
        return
    ray_list.append(ray)