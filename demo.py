from mohrcircleplotter import MohrPlot


if __name__ == "__main__":
    plot = MohrPlot()
    plot.principal_stress_circle(p1=380, p3=0)
    plot.principal_stress_circle(p1=401.4, p3=3)

    plot.estimated_mc_envelope()
    plot.ax.legend()
    plot.show()