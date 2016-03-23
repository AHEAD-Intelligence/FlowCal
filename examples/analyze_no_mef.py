#!/usr/bin/python
import os
import os.path

import numpy as np
import scipy
import matplotlib.pyplot as plt

import FlowCal

# Directories
directory = 'FCFiles'
gated_plot_dir = 'plot_samples'

# Plot options
plot_gated = True

# Files
data_files = ['data.{:03d}'.format(i) for i in range(1,6)]

if __name__ == "__main__":
    # Check that directories exists, create if it doesn't.
    if not os.path.exists(gated_plot_dir):
        os.makedirs(gated_plot_dir)

    # Process data files
    print("\nLoading data...")
    data = []
    for df in data_files:
        di = FlowCal.io.FCSData('{}/{}'.format(directory, df))
        data.append(di)

        dv = di.detector_voltage('FL1-H')
        print("{} ({} events, FL1-H voltage = {}).".format(str(di),
            di.shape[0], dv))

    # Basic gating/trimming
    ch_all = ['FSC-H', 'SSC-H', 'FL1-H', 'FL2-H', 'FL3-H']
    data = [FlowCal.gate.start_end(di, num_start=250, num_end=100)
            for di in data]
    data = [FlowCal.gate.high_low(di, ch_all) for di in data]

    # Transform to Relative Fluorescence Units (rfi), commonly known as
    # arbitrary units (a.u.)
    data_transf = [FlowCal.transform.to_rfi(di, ch_all) for di in data]

    # Ellipse gate
    print("\nRunning ellipse gate on data files...")
    data_gated = []
    data_gated_contour = []
    for di in data_transf:
        print("{}...".format(str(di)))
        di_gated, __, gate_contour = FlowCal.gate.ellipse(
            data=di,
            channels=['FSC-H', 'SSC-H'],
            center=np.log10([200, 70]),
            a=0.15,
            b=0.10,
            theta=np.pi/4,
            log=True,
            full_output=True)
        data_gated.append(di_gated)
        data_gated_contour.append(gate_contour)

    # Plot
    if plot_gated:
        print("\nPlotting density diagrams and histograms of data")
        for di, dig, dgc in zip(data_transf, data_gated, data_gated_contour):
            print("{}...".format(str(di)))
            # Plot
            FlowCal.plot.density_and_hist(
                di,
                gated_data=dig,
                figsize=(7,7),
                density_channels=['FSC-H', 'SSC-H'], 
                hist_channels=['FL1-H'],
                gate_contour=dgc, 
                density_params={'mode': 'scatter', 'xlog': True, 'ylog': True}, 
                hist_params={'div': 4, 'log': True},
                savefig='{}/{}.png'.format(gated_plot_dir, str(di)))
            plt.close()

    print("\nDone.")