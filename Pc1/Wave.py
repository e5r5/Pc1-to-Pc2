#!/usr/bin/env python3
"""Plot the live microphone signal(s) with matplotlib."""
import argparse
from Queue import Queue, Empty


def int_or_str(text):
    """Helper function for argument parsing."""
    try:
        return int(text)
    except ValueError:
        return text


def audio_callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, True)
    # Fancy indexing with mapping creates a (necessary!) copy:
    queue.put(indata[::args.downsample, mapping])


def update_plot(frame):
    """This is called by matplot lib for each plot update.
    Typically, audio callbacks happen more frequently than plot updates,
    therefore the queue tends to contain multiple blocks of audio data.
    """
    global plotdata
    block = True  # The first read from the queue is blocking ...
    while True:##inf loof
        try:
            data = queue.get(block=block)
        except Empty:
            break
        shift = len(data)
        plotdata = np.roll(plotdata, -shift, axis=0)
        plotdata[-shift:, :] = data
        block = False  # ... all further reads are non-blocking
    for column, line in enumerate(lines):
        line.set_ydata(plotdata[:, column])
    return lines


parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('-l', '--list-devices', action='store_true')
parser.add_argument('-d', '--device', type=int_or_str)
parser.add_argument('-w', '--window', type=float, default=200, metavar='DURATION')
parser.add_argument('-i', '--interval', type=float, default=30)#len wava
parser.add_argument('-r', '--samplerate', type=float)
parser.add_argument('-n', '--downsample', type=int, default=10, metavar='N')#circal
parser.add_argument('channels', type=int, default=[1], nargs='*', metavar='CHANNEL')#min is mono
args = parser.parse_args()
if any(c < 1 for c in args.channels):#no less then mono CHANNEL
    parser.error('argument CHANNEL: must be >= 1')#do error
mapping = [c - 1 for c in args.channels]  # Channel numbers start with 1
queue = Queue()

try:
    from matplotlib.animation import FuncAnimation
    import matplotlib.pyplot as plt
    import numpy as np
    import sounddevice as sd

    if args.samplerate is None:
        device_info = sd.query_devices(args.device, 'input')
        args.samplerate = device_info['default_samplerate']

    length = int(args.window * args.samplerate / (1000 * args.downsample))
    plotdata = np.zeros((length, len(args.channels)))

    fig, ax = plt.subplots()
    lines = ax.plot(plotdata)

    ax.axis((2, len(plotdata), -1, 1))
    ax.set_yticks([0])
    ax.yaxis.grid(True)
    ax.tick_params(bottom='off', top='off', labelbottom='off',right='off', left='on', labelleft='on')
    fig.tight_layout(pad=10)

    stream = sd.InputStream(device=args.device, channels=max(args.channels),samplerate=args.samplerate, callback=audio_callback)
    ani = FuncAnimation(fig, update_plot, interval=args.interval, blit=True)
    with stream:
        plt.show()
except Exception as e:
    parser.exit(type(e).__name__ + ': ' + str(e))