# LabJack UDP Broadcast and Receiving

By Jack Stevenson, with contributions and revisions by Chris Romsos and references from LabJack Corporation

### This project offers a convenient method to send signals from a LabJack analog-to-digital converter over UDP to be written to a database or displayed live. It consists of two parts - a script to broadcast UDP from the LabJack and another to receive and write the data. These scripts can run on the same machine or on different ones, but they have to be run on the same network as the LabJack. 

### We used the LabJack T7 (https://labjack.com/products/t7), but this code will likely work with the T4 and maybe other models if the device type is changed in the code. This code uses the LabJack LJM library for functions directly involving the LabJack. You can learn more about LJM here - https://labjack.com/ljm. For examples of python code using LJM, visit https://labjack.com/support/software/examples/ljm/python.

### The broadcast script can be edited directly to change its functionality, but it is probably more useful if imported as a module. 

