'''
    @file           main.py
    @brief          Reads ADC pin on Nucleo and saves data in queue
    @details        This file instantiates the output and analog read out pins.
                    The ADC pin value is read every millisecond then the 
                    corresponding data entry gets added to the queue. 

    @author         Jeremy Baechler
    @author         Kendall Chappell
    @author         Matthew Wimberley
    @date           16-Feb-2022
    '''
    
import pyb, utime, task_share
import micropython
micropython.alloc_emergency_exception_buf(100)


pinPC1 = pyb.Pin (pyb.Pin.board.PC1, pyb.Pin.OUT_PP)
tim1 = pyb.Timer (1, freq=1000)
ADCP0 = pyb.Pin (pyb.Pin.board.PC0, pyb.Pin.ANALOG)
adc = pyb.ADC(ADCP0)

q0 = task_share.Queue('h', 1000)
count = 0

def ISR_ADC(IRQ_src):
    '''
    @brief      sets interrupt every millisecond where ADC value is read
    @details    Once data is collected for one second, "Stop Transmission" line
                is sent where CTRL-C and CTRL-D commands are sent over serial
                communication. 
    @param      IRQ_src         The cause of the interrupt
    '''
    
    global count
    if count < 1000:
        q0.put(adc.read())
        count += 1
    elif count >= 1000:
        tim1.callback(None)
        print('Stop Transmission')
        pinPC1.low()
    

tim1.callback(ISR_ADC) # runs when interrupt is called


while True:
    '''
    @brief      sets pin low and high and retrieves ADC value each time
    @details    This loop is just for our testing needs.
    '''
    
    pinPC1.low()
#   utime.sleep_us(100)
    pinPC1.high()
    print(q0.get()) 
    

# We used this to test runs on first order response.
        
# while True: 

#     pinPC1.low()
#     utime.sleep_ms(2000)
#     pinPC1.high()
#     utime.sleep_ms(2000)
