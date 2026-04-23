"""
mohrcircleplotter: Mohr circle construction and stress transformation utilities.

Copyright (c) 2026 Earl Magsipoc
Licensed under the MIT License. See LICENSE for details.

DISCLAIMER: For educational and research use only. The author accepts no
liability for use of this software in engineering design or decision-making.
Verify all results independently before use in practice.
"""

from __future__ import annotations

import numpy as np
import numpy.typing as npt

class Circle:
    def __init__(self, **kwargs: float | None) -> None:
        """Initialize a Mohr circle from principal or plane stress values.

        Parameters are expected as keyword arguments. Use either principal
        stresses (``p1``, ``p3`` and optionally ``p2``) or oriented plane-stress
        values (``sigma_x``, ``sigma_y``, ``tau_xy``).

        Args:
            **kwargs: Numeric stress values used to define the circle.
        """
        if 'p1' in kwargs:
            self.p1 = kwargs['p1']
            self.p3 = kwargs['p3']
        
        if 'p2' in kwargs:
            if kwargs['p2'] is not None:
                self.p2 = kwargs['p2']
        
        if 'sigma_x' in kwargs:
            self.sx = kwargs['sigma_x']
            self.sy = kwargs['sigma_y']
            self.tauxy = kwargs['tau_xy']
            r = np.sqrt(((self.sx - self.sy) / 2) ** 2 + self.tauxy ** 2)
            c = (self.sx + self.sy) / 2
            self.p1 = c + r
            self.p3 = c - r
            self.x_plane_angle = np.arccos((self.sx - c) / r) / 2

    @property
    def C(self) -> float:
        """Return the center of the principal stress circle.

        Returns:
            float: Circle center on the normal-stress axis.
        """
        return (self.p1 + self.p3) / 2
    
    @property
    def R(self) -> float:
        """Return the radius of the principal stress circle.

        Returns:
            float: Circle radius.
        """
        return (self.p1 - self.p3) / 2
    
    @property
    def R12(self) -> float:
        """Return the radius for the circle between ``p1`` and ``p2``.

        Returns:
            float: Radius of the ``p1``-``p2`` circle.
        """
        return (self.p1 - self.p2) / 2
    
    @property
    def R23(self) -> float:
        """Return the radius for the circle between ``p2`` and ``p3``.

        Returns:
            float: Radius of the ``p2``-``p3`` circle.
        """
        return (self.p2 - self.p3) / 2
    
    def get_circle_points(
        self,
        num_points: int = 100,
        half_circle: bool = False,
        pstress: int = 13,
    ) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """Generate x/y coordinates on the Mohr circle perimeter.

        Args:
            num_points: Number of sample points along the perimeter.
            half_circle: If ``True``, generate only the upper half circle.
            pstress: Reserved argument kept for backward compatibility.

        Returns:
            tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
                Tuple of x and y arrays for plotting.
        """
        if half_circle:
            theta = np.linspace(0, np.pi, num_points)
        else:
            theta = np.linspace(0, 2 * np.pi, num_points)
        x = self.C + self.R * np.cos(theta)
        y = self.R * np.sin(theta)
        return x, y
    
    def get_plane(self, orientation: float) -> tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
        """Return the stress-state line for a plane orientation.

        Args:
            orientation: Plane angle in radians.

        Returns:
            tuple[npt.NDArray[np.float64], npt.NDArray[np.float64]]:
                Two-point x and y arrays defining the plane line.
        """
        x = np.array([self.C, self.C + self.R * np.cos(2*orientation)])
        y = np.array([0, self.R * np.sin(2*orientation)])
        return x, y
    