import serial


def readPins():
    ser = serial.Serial('/dev/ttyACM0', 230400)
    while 1:
        print(ser.readline().decode("utf-8").strip("\n"))  # decode because serial monitor returns byte stream

readPins()
