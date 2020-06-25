# A python script to hold the basic classes/functions used in this package

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
        self.start = start
        self.end = end
        self.t_coeff = t_coeff
        self.ref_idx = ref_idx

    def bound_line(self, start:list, end:list):
        """Defines the boundary lines of the material given its start and endpoints
        
        This method returns the equation of a line that defines the boundary

        Inputs: 
            start: [int, int] = starting point of the boundary
            end: [int, int]   = end of the boundary
        Returns: 
            x_boundary        = a range of x values defining the boundary
            y_boundary        = a range of y values defining the boundary
        """
        slope = (self.end[1]-self.start[1])/(self.end[0]-self.start[0])
        intercept = self.end[1]-slope*end[0]
        x_boundary =  np.arange(self.start[0], self.end[0])
        y_boundary = [slope*x+intercept for x in x_boundary]

class Ray:
    """ This class defines a single ray of light
        For proper intersection at the boundary, let 0 < angle < np.pi

    Parameters:
        start: [int, int]     = the starting point of the ray
        angle: [float, float] = angle of the ray in radians
        brightness: float     = the brightness of the ray (as a fraction of the original power) 

    Methods:
        split = splits this ray at a given Boundary
    """

    def __init__(self, start:list, angle:float, brightness:float):
        """ Constructor for the Ray class """
        self.start = start
        self.angle = angle
        self.brightness = brightness

    def ray_coords(self, start:list, angle:float):
        """ Defines lists of x,y coordinates for the ray

            Inputs: 
                start: [int, int]     = the starting point of the ray
                angle:  float         = angle of the ray in radians
            Returns:
                x_ray: list           = a range of x values defining the ray path
                y_ray: list           = a range of y values defining the ray path

        """
        x_ray = np.arange(self.start[0], 101)
        slope = np.tan(self.angle)
        intercept = self.start[0] - (slope * self.start[1])
        y_ray = [slope * x + intercept for x in x_ray]
        return x_ray, y_ray


    def split(self, b:Boundary, intersection:list):
        """ Splits this ray into two rays (one reflected, one refracted) at the given Boundary

        This method assumes that the given Boundary is intersected by this ray

        Inputs:
            b            = the boundary for this ray to split at
            intersection = the point at which ray, boundary intersdect and reflection/refraction happens
        Returns:
            ray_refl = the refracted ray
            ray_refr = the reflected ray
        """
        import numpy as np
        refl_angle = self.angle + np.pi
        refr_angle = np.pi - np.arcsin(np.sin(self.angle)*(1/b.ref_idx))
        #refl/refr angles are measured up from b, 
        #incoming angle is currently defined up in the opposite direction
        ray_refl = Ray(intersection,refl_angle, self.brightness*(1-b.t_coeff))
        ray_refr = Ray(intersection,refr_angle, self.brightness*b.t_coeff)
        return ray_refl, ray_refr

def intersection(ray, boundary):
    """This function determines when a propogating ray intersects with a given boundary

    Inputs:
        ray             = ray propoagtaing through the space
        boundary        = boundary that ray will encounter
    Returns:
        int_x, int_y: int, int = the point of intersection

    """
    x_ray , y_ray = Ray.ray_coords(ray)
    x_bound, y_bound = Boundary.bound_line(boundary)
    for i in range(len(x_ray)+1):
        if x_ray[i]==x_bound[i]:
            if y_ray[i]==y_bound[i]:
                int_x=x_ray[i]
                int_y=y_ray[i]
                return [int_x, int_y]
    end


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