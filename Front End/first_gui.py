"""
First try: Matlab-like UI with Multiple Graphs and subplots.
"""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fig = plt.figure()
fig.canvas.set_window_title('Processed Signal Information')
# Divide up ui into sections for each graph
gs = gridspec.GridSpec(3, 2)
ax1 = plt.subplot(gs[0, :])
ax2 = plt.subplot(gs[1,0:1])
ax3 = plt.subplot(gs[1,1:2])
ax4 = plt.subplot(gs[2,0:1])
ax5 = plt.subplot(gs[2,1:2])

# Sample data for now, use data from signal analysis later
x1 = np.linspace(0.0, 5.0)
x2 = np.linspace(0.0, 2.0)
x3 = np.arange(0.0, 2.0, 0.01)
x4 = np.arange(-8., 8., .01)
x5 = np.linspace(0,2*np.pi,100)
# yhat = savitzky_golay(y, 51, 3) # window size 51, polynomial order 3

y1 = np.cos(2 * np.pi * x1) * np.exp(-x1)
y2 = np.cos(2 * np.pi * x2)
y3 = 1 + np.sin(2*np.pi*x3)
y4 = np.sin(x4) + np.random.random(1600) * 0.3
y5 = np.sin(x5) + np.random.random(100) * 0.2

ax1.plot(x1, y1, 'o-')
ax1.set_title('Complete Signal After Noise Reduction')
ax1.set_ylabel('Damped oscillation')
ax1.set_xlabel('time (s)')

ax2.plot(x2, y2, 'r-')
ax2.set_title('Respiration Signal')
ax2.set_ylabel('Volts (V)')
ax2.set_xlabel('time (s)')

ax3.plot(x3, y3, '.-')
ax3.set_title('Heart Rate Signal')
ax3.set_ylabel('Volts (V)')
ax3.set_xlabel('time (s)')

ax4.plot(x4, y4, 'y-')
ax4.set_title('Transient Respiration Signal')
ax4.set_ylabel('Volts (V)')
ax4.set_xlabel('time (s)')

ax5.plot(x4, y4, 'g-')
ax5.set_title('Transient Heart Rate Signal')
ax5.set_ylabel('Volts (V)')
ax5.set_xlabel('time (s)')

plt.tight_layout()
plt.figtext(0, .015, 'Sampling Rate: XXX samples/s, Upper Frequency Limit: XXXX Hz, Lower Frequency Limit: XXXX Hz', va='center', fontsize=9)
plt.show()