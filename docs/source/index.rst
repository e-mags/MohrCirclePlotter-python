.. Mohr Circle Plotter documentation master file, created by
   sphinx-quickstart on Fri Apr 24 11:36:21 2026.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Mohr Circle Plotter documentation
=================================

This is the documentation for the Mohr Circle Plotter Python package, which provides tools for plotting basic Mohr's circle visualizations.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules

License
=======
This software is provided for **educational and research purposes only**. Results produced by this package should not be used as the sole basis for engineering design decisions without independent verification by a qualified professional engineer.

THE AUTHORS AND CONTRIBUTORS ACCEPT NO LIABILITY for any damages, losses, or consequences arising from the use or misuse of this software. See LICENSE file for full terms (MIT License).

Quickstart
==========

This quickstart guide will help you get up and running with the Mohr Circle Plotter package. For more detailed information, please refer to the :ref:`apidocs` section.

Installation
----------------
To install the Mohr Circle Plotter package, you can use pip:

.. code-block:: bash

   pip install mohrcircleplotter

Basic Usage
-----------------
Here's a simple example to create a Mohr's circle plot:

.. code-block:: python

    from mohrcircleplotter import MohrPlot

    # Create a plotter instance which contains a matplotlib figure and axis
    plot = MohrPlot(halfplot=True,show_tension=True, units='MPa')

    # Define some circles (sigma_x, sigma_y, tau_xy)
    circles = [
        (80, 30, 30),
        (60, 20, 20),
        (40, 10, 10)
    ]

    # Plot the circles with red dashed lines showing the orientation of sigma_x
    for sigma_x, sigma_y, tau_xy in circles:
        plot.oriented_circle(sigma_x, sigma_y, tau_xy)


This code will create a Mohr's circle plot with three circles corresponding to the specified stress states. The red dashed lines indicate the orientation of the :math:`\sigma_x` plane for each circle.

.. figure:: _static/oriented_circles.png
   :align: center
   :alt: Oriented Circles Example

Principal stresses can be input to the plotter using the `principal_stress_circle` method, which will automatically compute the corresponding circles and orientations.

.. code-block:: python

    from mohrcircleplotter import MohrPlot

    plot = MohrPlot(halfplot=True,show_tension=True, units='MPa')

    # Define principal stresses (sigma_1, sigma_2)
    principal_stresses = [
        (90, 50),
        (60, 30),
        (40, 10)
    ]

    # Plot circles from principal stresses
    for sigma_1, sigma_2 in principal_stresses:
        plot.principal_stress_circle(sigma_1, sigma_2)

.. figure:: _static/principal_stress_circles.png
   :align: center
   :alt: Principal Stress Circles Example

A Mohr-Coulomb failure envelope can be estimated from the plotted circles using the `estimated_mc_envelope` method, which will fit a line to the points of maximum shear stress and normal stress.


.. code-block:: python

    from mohrcircleplotter import MohrPlot

    plot = MohrPlot(halfplot=True,show_tension=True, units='MPa')

    # Define some circles (sigma_x, sigma_y, tau_xy)
    circles = [
        (80, 30, 30),
        (60, 20, 20),
        (40, 10, 10)
    ]

    for sigma_x, sigma_y, tau_xy in circles:
        plot.oriented_circle(sigma_x, sigma_y, tau_xy)

    # Estimate and plot the Mohr-Coulomb failure envelope
    plot.estimated_mc_envelope()

.. figure:: _static/estimate_mc_envelope.png

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

