import serial, time
global ser
ser = None

def initializeSerial(in_port='COM7'):
    return serial.serial(port=in_port,
        baudrate=9600,
        parity=serial.PARITY_ODD,
        stopbits=serial.STOPBITS_TWO,
        bytesize=serial.SEVENBITS
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

def receive():
    if ser == None:
        ser = initializeSerial()
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
