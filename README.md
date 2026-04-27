# MohrCirclePlotter
A Python library to plot Mohr's circle

## ⚠️ Disclaimer

This software is provided for **educational and research purposes only**. Results produced by this package should not be used as the sole basis for engineering design decisions without independent verification by a qualified professional engineer.

THE AUTHORS AND CONTRIBUTORS ACCEPT NO LIABILITY for any damages, losses, or consequences arising from the use or misuse of this software. See [`LICENSE`](LICENSE) for full terms.

## Installation

```bash
pip install mohrcircleplotter
```

## Documentation
Mohr's circles are plotted on a matplotlib plot. If these circles are stresses at failure, a Mohr-Coulomb failure envelope can be estimated. More details can be found in [https://e-mags.github.io/MohrCirclePlotter/](https://e-mags.github.io/MohrCirclePlotter/)

```python
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
```
![Graph showing MC envelope estimated over Mohr's circles](https://github.com/e-mags/MohrCirclePlotter/raw/main/docs/source/_static/estimate_mc_envelope.png)


