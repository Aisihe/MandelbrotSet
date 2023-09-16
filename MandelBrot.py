import numpy as np
import matplotlib.pyplot as plt
from mpl_interactions import ioff, panhandler, zoom_factory
import warnings
import time
warnings.filterwarnings("ignore")  # For the overflow and invalid exponent runtime warnings

################################

#impacts level of 'infinite zoom;' higher means more zoom; recc is 64:
zoom_level = 64
# Length and Width of the image
b = 512

################################




xlims = (b//-2, b//2)
ylims = (b//-2, b//2)

# Scroll zoom handler
def on_scroll(event_ax):
    global xlims, ylims
    xlims = event_ax.get_xlim()
    ylims = event_ax.get_ylim()
    print(f"{xlims} \n {ylims}")
    update_plot(xlims, ylims)
    reattach_callbacks()

def reattach_callbacks():
    global scroll_cid
    scroll_cid = ax.callbacks.connect('ylim_changed', on_scroll)

# Calculate Mandelbrot set with updated grid size
def calculate_mandelbrot(xmin, xmax, ymin, ymax):
    st = time.time()
    broadcast = np.zeros([b, b])
    X = np.linspace(xmin, xmax, num=b, endpoint=False) + broadcast
    temp = (np.linspace(ymin, ymax, num=b, endpoint=False) + broadcast)
    Y = np.copy(temp).T
    del temp
    c = (X + Y * 1j) * (4 / b)  # Complex numbers array
    c = c.astype(np.complex64)  # Save memory
    a = np.zeros_like(c)
    a = (a ** 2 + c)
    for k in range(zoom_level):
        #(a ** 2 + c)
        #((((((a ** 2 + c) ** 2 + c) ** 2 + c) ** 2 + c) ** 2 + c) ** 2 + c) ** 2 + c
        a = (a ** 2 + c) 

    a[a <= 1] = 1  # Filter divergents out
    print(time.time() - st)
    return np.real(a)  


# Update the plot with the new Mandelbrot set
def update_plot(xlims, ylims):
    a_zoomed = calculate_mandelbrot(xlims[0], xlims[1], ylims[0], ylims[1])
    ax.callbacks.disconnect(scroll_cid)
    ax.cla()
    ax.imshow(a_zoomed, cmap="gray", extent=(xlims[0], xlims[1], ylims[0], ylims[1]))


a = calculate_mandelbrot(xlims[0], xlims[1], ylims[0], ylims[1])
#### Scroll wheel zoom ####
with plt.ioff():
    fig, ax = plt.subplots()

ax.imshow(a, cmap="gray", extent=(-b//2, b//2, -b//2, b//2))
disconnect_zoom = zoom_factory(ax)

scroll_cid = ax.callbacks.connect('ylim_changed', on_scroll)
pan_handler = panhandler(fig)

plt.show()

