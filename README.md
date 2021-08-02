# LabJack UDP Broadcast Code

By Jack Stevenson, with contributions and revisions by Chris Romsos and references from LabJack Corporation

## Objective: We want to use our LabJack T7 (https://labjack.com/products/t7) Pro to sample (digitize) an analog voltage signal, encapsulate that sampled voltage as a formatted (comma separated timestamp, voltage) message for broadcast (UDP) on our shipboard sensor network.  Labjack provides a cross-platform library (LJM) for working with the device (https://labjack.com/ljm).  See: https://labjack.com/support/software/examples/ljm/python for instructions on how to install the python ljm modules.

## Desired Product: For each sample of the analog voltage, we want to create an ASCII string of format 'timestamp_iso8601, voltage' and broadcast that message to the 172.20.30.0/24 netwwork on a user specified port (e.g. 30315 or 172.20.30.255:30315).  The user should be able to set the analog signal sampling rate (samples per second, or seconds between samples), the broadcast address (here we use 172.20.30.255 because it's the broadcast address for the sensor data subnet on the ship), and the broadcast port.  The module should log any errors or exceptions using the python logging module to /var/log/CORIOLIX_labjack.


