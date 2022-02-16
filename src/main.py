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
    global count
    if count < 1000:
        q0.put(adc.read())
        count += 1
    elif count >= 1000:
        tim1.callback(None)
        print('Stop Transmission')
        pinPC1.low()
    

tim1.callback(ISR_ADC)
# pinPC1.low()
# utime.sleep_us(500)
# pinPC1.high()
while True:
    pinPC1.low()
#     utime.sleep_us(100)
    pinPC1.high()
    print(q0.get())
    


# while True: 
        # Test runs on first order response
#     pinPC1.low()
#     utime.sleep_ms(2000)
#     pinPC1.high()
#     utime.sleep_ms(2000)
