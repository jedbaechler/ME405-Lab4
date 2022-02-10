'''
    @file           reader_lab3.py
    @brief          Reads serial inputs and puts 2 columns in lists
    @details        This file decodes the csv data written through the 
                    serial port and instantiates them as two lists. These two
                    lists are converted to floats, where each row is then 
                    appended. With these two lists we are able to instantly
                    print the step response.

    @author         Jeremy Baechler
    @author         Kendall Chappell
    @author         Matthew Wimberley
    @date           7-Feb-2022
    '''
    
import serial
from matplotlib import pyplot as plot

time = 0
x = []
y = []

with serial.Serial ('COM3', 115200) as s_port:
    s_port.write(b'\x03\x04')
    while True:
        data_line = s_port.readline().strip().decode()
        print(data_line)
        if data_line == 'Stop Transmission':
            s_port.write(b'\x03\x04')
            break
        try:
            data = int(data_line)
        except ValueError:
            print('ValueError has been caught! Data cannot be converted to int')
        else:
            x.append(time)
            y.append(data)
            time += 1

plot.plot(x,y)
plot.xlabel('Time (ms)')
plot.ylabel('ADC Reading')
    
