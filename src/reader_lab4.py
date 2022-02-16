'''
    @file           reader_lab4.py
    @brief          Reads serial inputs and puts 2 columns in lists
    @details        This file decodes the csv data written through the 
                    serial port and instantiates them as two lists. These two
                    lists are converted to floats, where each row is then 
                    appended. With these two lists we are able to instantly
                    print the step response. This program is adapted from our 
                    plotter for lab 2.

    @author         Jeremy Baechler
    @author         Kendall Chappell
    @author         Matthew Wimberley
    @date           16-Feb-2022
    '''
    
import serial
from matplotlib import pyplot as plot

time = 0 # instantiate time and list objects
x = []
y = []

with serial.Serial ('COM3', 115200) as s_port:
    s_port.write(b'\x03\x04') # CTRL-C & CTRL-D upon restart
    # very nice to get the motor to stop running
    
    while True:
        data_line = s_port.readline().strip().decode()
        print(data_line)
        if data_line == 'Stop Transmission': # given from main.py file
            s_port.write(b'\x03\x04')
            break
        try:
            data = int(data_line) # may not always get good data
        except ValueError:
            print('ValueError has been caught! Data cannot be converted to int')
            # throws nonsense data away
        else:
            x.append(time) # appends data then goes to top of loop
            y.append(data)
            time += 1

plot.plot(x,y) #plots x vs. y
plot.xlabel('Time (ms)')
plot.ylabel('ADC Reading') #axis labels
    
