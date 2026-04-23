"""
mohrcircleplotter: Mohr circle construction and stress transformation utilities.

Copyright (c) 2026 Earl Magsipoc
Licensed under the MIT License. See LICENSE for details.

DISCLAIMER: For educational and research use only. The author accepts no
liability for use of this software in engineering design or decision-making.
Verify all results independently before use in practice.
"""

from __future__ import annotations

from .circle import Circle
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib.axes import Axes
import numpy as np
from typing import Any, Sequence

class MohrPlot:

    def __init__(self, **kwargs: Any) -> None:
        """Create a Mohr circle plotting helper.

        Keyword arguments are forwarded to ``matplotlib.pyplot.figure`` after
        consuming ``halfplot`` and ``show_tension``.

        Args:
            **kwargs: Figure options and plot behavior flags.
        """

        self.halfplot = kwargs['halfplot'] if 'halfplot' in kwargs else False
        if 'halfplot' in kwargs:
            del kwargs['halfplot']
        self.show_tension = kwargs['show_tension'] if 'show_tension' in kwargs else False
        if 'show_tension' in kwargs:
            del kwargs['show_tension']


        self.units = kwargs['units'] if 'units' in kwargs else ''
        if 'units' in kwargs:
            del kwargs['units']

        self.figure: Figure = plt.figure(**kwargs)
        self.ax: Axes = self.figure.add_subplot(111)

        self.circles: list[Circle] = []
        self.mohrcoulomb_envelopes: list[tuple[float, float]] = []
        self.figure.axes[0].set_aspect('equal')
        self.ax.set_xlabel('Normal Stress' if self.units == '' else f'Normal Stress ({self.units})')
        self.ax.set_ylabel('Shear Stress' if self.units == '' else f'Shear Stress ({self.units})')
        self.ax.spines['top'].set_visible(False)
        self.ax.spines['right'].set_visible(False)
        self.ax.spines['bottom'].set_position('zero')
        self.ax.spines['left'].set_position('zero')

    def _set_axes(self) -> None:
        """Update axis limits and grid from current circles and envelopes."""
        max_stress = self.max_stress
        self.ax.set_xlim(0 if not self.show_tension else self.tension_cutoff*1.05, max_stress*1.05)

        self.ax.grid(True)
        max_ylim = self._max_shear * 1.05

        if self.halfplot:
            self.ax.set_ylim(0, max_ylim)
        else:
            self.ax.set_ylim(-max_ylim, max_ylim)

    @property
    def tension_cutoff(self) -> float:
        """Return the minimum normal stress shown when tension is enabled.

        Returns:
            float: Minimum normal-stress value across circles/envelopes.
        """
        circle_min = min([c.C - c.R for c in self.circles]) if self.circles else 0
        min_env = 0
        if self.mohrcoulomb_envelopes:
            min_env = min((-c / np.tan(phi) for c,phi in self.mohrcoulomb_envelopes), default=0)

        return min(circle_min, min_env)

    @property
    def max_stress(self) -> float:
        """Return the maximum normal stress represented in the plot.

        Returns:
            float: Largest circle right-most x value.
        """
        return max([c.C + c.R for c in self.circles]) if self.circles else 0

    @property
    def _max_shear(self) -> float:
        """Return the highest shear stress used to scale y-limits.

        Returns:
            float: Maximum shear from circles and envelopes.
        """
        circle_max = max([c.R for c in self.circles]) if self.circles else 0
        max_tau = 0
        if self.mohrcoulomb_envelopes:
            max_tau = max((c + self.max_stress * np.tan(phi) for c,phi in self.mohrcoulomb_envelopes), default=0)

        return max(circle_max, max_tau)

    def principal_stress_circle(
        self,
        p1: float | None = None,
        p3: float | None = None,
        p2: float | None = None,
        label: str | None = None,
        num_points: int = 100,
    ) -> int:
        """Add a circle defined by principal stresses.

        Args:
            p1: Maximum principal stress.
            p3: Minimum principal stress.
            p2: Intermediate principal stress (optional).
            label: Optional legend label.
            num_points: Number of perimeter points for plotting.

        Returns:
            int: Index of the newly stored circle.
        """
        circle = Circle(p1=p1, p3=p3, p2=p2)
        x, y = circle.get_circle_points(num_points=num_points)
        self.ax.plot(x, y, label=label)
        self.circles.append(circle)
        self._set_axes()
        return len(self.circles) - 1
    
    def oriented_circle(
        self,
        sigma_x: float,
        sigma_y: float,
        tau_xy: float,
        label: str | None = None,
        num_points: int = 100,
    ) -> int:
        """Add a circle from a 2D stress tensor.

        Args:
            sigma_x: Normal stress in x direction.
            sigma_y: Normal stress in y direction.
            tau_xy: In-plane shear stress.
            label: Optional legend label.
            num_points: Number of perimeter points for plotting.

        Returns:
            int: Index of the newly stored circle.
        """
        circle = Circle(sigma_x=sigma_x, sigma_y=sigma_y, tau_xy=tau_xy)
        x, y = circle.get_circle_points(num_points=num_points)
        self.ax.plot(x, y, label=label)
        self.circles.append(circle)

        self.oriented_plane(circle.x_plane_angle, circle_index=len(self.circles)-1)
        self._set_axes()
        return len(self.circles) - 1

    def oriented_plane(self, plane_angle: float, circle_index: int = 0) -> None:
        """Plot a plane-orientation line on an existing circle.

        Args:
            plane_angle: Plane angle in radians.
            label: Optional label for the plane.
            circle_index: Index of the target stored circle.
        """
        if circle_index < len(self.circles):
            circle = self.circles[circle_index]
            x, y = circle.get_plane(plane_angle)
            self.ax.plot(x, y, 'r--')
        
            # if label:
            #     self.ax.annotate(label, xy=(x[-1], y[-1]), xytext=(10, 10), textcoords='offset points', color='r')

        self._set_axes()

    def estimated_mc_envelope(
        self,
        circles: Sequence[int] | None = None,
        label_line: bool = False,
    ) -> None:
        """Estimate and plot a linear Mohr-Coulomb envelope from circles.

        Args:
            circles: Optional indices of circles to include in the fit.
            label_line: Whether to annotate the envelope parameters.
            plot_tension_cutoff: Reserved compatibility parameter.
        """
        if circles is None:
            selected_circles = self.circles
        else:
            selected_circles = [self.circles[i] for i in circles if i < len(self.circles)]
        p = [c.C for c in selected_circles]
        q = [c.R for c in selected_circles]
        tan_alpha, m = np.polyfit(p, q, 1)
        phi = np.arcsin(tan_alpha)
        c = m / np.cos(phi)
        self.mc_envelope(c, phi, label_line=label_line)

    def mc_envelope(
        self,
        c: float,
        phi: float,
        label_line: bool = False
    ) -> None:
        """Plot a Mohr-Coulomb failure envelope.

        Args:
            c: Cohesion intercept.
            phi: Friction angle in radians.
            label_line: Whether to annotate the line endpoint.
        """
        self.mohrcoulomb_envelopes.append((c, phi))
        p_coulomb = np.linspace(0 if not self.show_tension else -c/np.tan(phi), self.max_stress*1.05, 100)
        q_coulomb = c + p_coulomb * np.tan(phi)
        self.ax.plot(p_coulomb, q_coulomb, 'k--', label=f'Mohr-Coulomb Envelope (φ={np.degrees(phi):.2f}°, c={c:.2f})')
        if label_line:
            label = f'c={c:.2f}\nφ={np.degrees(phi):.2f}°'
            self.ax.annotate(label, xy=(p_coulomb[-1], q_coulomb[-1]), xytext=(10, 10), textcoords='offset points')
        self._set_axes()
