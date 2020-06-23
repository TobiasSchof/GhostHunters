# A python script to hold the basic classes used in this package

class Ray:
    """ This class defines a singal ray of light

    Parameters:
        start: [float, float] = the starting point of the ray
        dir: [float, float]   = the two-dimensional direction of the ray
        brightness: float     = the brightness of the ray (as a fraction of the original power) 

    Functions:
        split = splits this ray at a given Boundary
    """

    def __init__(self, start:list, dir:list, brightness:float):
        """ Constructor for the Ray class """

    def split(self, b:Boundary) -> (Ray, Ray):
        """ Splits this ray into two rays (one reflected, one refracted) at the given Boundary

        This method assumes that the given Boundary is intersected by this ray

        Inputs:
            b = the boundary for this ray to split at
        Returns:
            Ray = the refracted ray
            Ray = the reflected ray
        """

        # You can copy your code from the previous file here (with the relevant modifications)

class Boundary:
    """ This class defines a Boundary between air and another medium

    Parameters:
        start:     [float, float] = the start of the line segment defining this barrier
        end:       [float, float] = the end of the line segment defining this barrier
        t_coeff:   float          = the transmission coefficient of the barrier
        ref_idx:   float          = the refractive index of the other medium
        norm:      [float, float] = the direction of the norm towards the air side
    """

    def __init__(self, start, end, t_coeff, ref_idx):
