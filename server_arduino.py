import requests
import threading
import random
from queue import Queue
import serial

import time

items = Queue()
ser = serial.Serial('/dev/cu.usbmodem1411', 230400)

#57600

# def loop_timer(call_func):
#
#     call_func()
#
#     t = threading.Timer(7, loop_timer, args=[update_frontend_randomly])
#     t.start()


def update_frontend_randomly():
    while True:
        time.sleep(5)
        print("Inserting random number into queue")
        items.put(random.randint(0, 11))


def update_frontend():

    print("Frontend updater started...")

    while True:
        try:
            a = items.get()
            b = items.get()

            url = "http://localhost:3000/update"

            payload = "{ \"a\": %d, \"b\": %d}" % (a, b)
            headers = {
                'content-type': "application/json",
                'cache-control': "no-cache"
            }

            print("Updating frontend with: %s" % payload)

            response = requests.request("POST", url, data=payload, headers=headers)

            print('Success: %d' % response.status_code)
        except Queue.empty():
            print("Still waiting for user to pick to cards")


# This would be the standard entry point to my app from the arduino serial output
# The n is equivalent to the serial number passed in
# This queues up selected items

def read_pins():
    data_str = ''

    while True:
        #rint("Info from serial port: " + ser.readline().decode("utf-8").strip("\n"))

        if (ser.inWaiting() > 0):  # if incoming bytes are waiting to be read from the serial input buffer
            data_str = ser.read(ser.inWaiting()).decode(
                'ascii').strip("\n")  # read the bytes and convert from binary array to ASCII
            print('Output:' + data_str)
        else:
            print("Placing an item in the queue: " + str(data_str))
            items.put(int(ser.readline().decode("utf-8").strip("\n")))
            print("Queue length is now: " + str(items.qsize()))

            print("Reached")

# Calls the Node.js backend every a pair of items are in the queue
t1 = threading.Thread(target=update_frontend)
t1.start()

# Whilst I don't have the touch board this simulates inputs randomly
t2 = threading.Thread(target=read_pins)
t2.start()





