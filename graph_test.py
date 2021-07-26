import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation
import psutil
import collections

cpu = collections.deque(np.zeros(10))
ram = collections.deque(np.zeros(10))

print(f"CPU: {cpu}")
print(f"Memory: {ram}")


def update():
    cpu.popleft()
    cpu.append(psutil.cpu_percent(interval=1))
    plt.ax.plot(cpu)

    ram.popleft()
    ram.append(psutil.cpu_percent(interval=1))
    plt.ax.plot(ram)


cpu = collections.deque(np.zeros(10))
ram = collections.deque(np.zeros(10))

update()
update()
update()

print(f"CPU: {cpu}")
print(f"Memory: {ram}")

