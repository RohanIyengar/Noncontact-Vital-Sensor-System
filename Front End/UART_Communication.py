import serial, time
global ser
ser = None

def initializeSerial(in_port='COM4'):
    return serial.Serial(port=in_port,
        baudrate=115200,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS,
        timeout=1
    )

def send(ser=None, input='Hello World'):
    if ser == None:
        ser = initializeSerial()
    try:
        ser.open()
    except Exception as e:
        print "error opening serial port" + str(e)
        exit()
    if ser.isOpen():
        try:
            #write data to MCU
            ser.write(input)
            print("write data: " + input)
            time.sleep(0.1)  #give the serial port sometime to receive the data

            #Only receive 5 lines for now -- fix this based on scheme later
            numOfLines = 0
            exceededLines = True
            while exceededLines:
                bytesToRead = ser.inWaiting()
                response = ser.read(bytesToRead)
                print("read data: " + response)
                numOfLines = numOfLines + 1
                if (numOfLines >= 5):
                    exceededLines = False

            ser.close()
        except Exception as e1:
            print "error communicating...: " + str(e1)

    else:
        print "serial port is not open"

def receive(ser=None, input='Hello World'):
    if ser == None:
        ser = initializeSerial()
    #try:
    #    ser.close()
    #except Exception as e:
    #    print "error closing serial port" + str(e)
    try:
        ser.open()
    except Exception as e:
        print "error opening serial port" + str(e)
        exit()
    if ser.isOpen():
        try:
            #Only receive 5 lines for now -- fix this based on scheme later
            numOfLines = 0
            exceededLines = True
            print("Trying to read data")
            while exceededLines:
                bytesToRead = ser.inWaiting()
                response = ser.read(bytesToRead)
                print("read data: " + response)
                numOfLines = numOfLines + 1
                if (numOfLines >= 5):
                    exceededLines = False

            #write data to MCU
            ser.write(input)
            print("write data: " + input)
            time.sleep(0.1)  #give the serial port sometime to receive the data
            ser.close()
        except Exception as e1:
            print "error communicating...: " + str(e1)
    else:
        print "serial port is not open"

def recv_without_open():
    ser_obj = initializeSerial()
    print "Initialized object to " + ser.portstr
    done = False
    line = []
    while not done:
        for c in ser.read():
            line.append(c)
            if len(line) != 0:
                print "Got the line: " + line
                line = []
                done = True
# i = 0;
# while  i < 10000:
#     time.sleep(.1)
#     try:
#         receive()
#     except Exception as e1:
#         print("Error: ") + str(e1)
#         i = i + 1

try:
    recv_without_open()
except Exception as e1:
    print("Error: ") + str(e1)