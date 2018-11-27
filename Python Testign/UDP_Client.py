import socket
import sys
import serial

# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('localhost', 10000)
ser = serial.Serial('/dev/ttyACM0', 230400)

def readPins():
    while 1:
        print(ser.readline().decode("utf-8").strip("\n"))  # decode because serial monitor returns byte stream

def sendToServer():
   while 1:
        try:
            # Send data
            pinnumber = ser.readline()
            print('sending "%s"' % pinnumber.decode('utf-8'))
            sent = sock.sendto(pinnumber, server_address)

            # Receive response
            data, server = sock.recvfrom(4096)

        finally:
            print('closing socket (not actually)')

sendToServer()