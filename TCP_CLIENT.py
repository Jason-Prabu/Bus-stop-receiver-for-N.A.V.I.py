#!usr/bin/python3

import serial
from serial import SerialException
import socket

bus_300 = '192.168.1.5'
num_300 = 1
bus_301 = '192.168.1.7', '192.168.1.2'
num_301 = 2
bus_500 = '111', '12', '193', '19.16.1.2', '11.5', '12.18.1.6'
num_500 = 6

serial_available = 0

TCP_PORT = 1234
message = 'BUS STOP A'


def get_ip(bus_number):

    if bus_number == "300":
        bus_ip = bus_300
        num_of_bus = num_300
        return bus_ip, num_of_bus, True

    elif bus_number == "301":
        bus_ip = bus_301
        num_of_bus = num_301
        return bus_ip, num_of_bus, True

    elif bus_number == "500":
        bus_ip = bus_500
        num_of_bus = num_500
        return bus_ip, num_of_bus, True

    else:
        return 0, 0, False


# MAIN()

while 1:
    if serial_available == 0:                           # BLOCKING FOR SERIAL PORT
        try:
            Arduino = serial.Serial("COM6", 9600)        #open serial port at 9600 bps
        except SerialException:                          #WAIT TILL SERIAL PORT AVAILABLE
            # print("a")
            serial_available = 0
        else:                                          # IF SERIAL PORT AVAILABLE CONTINUE
            # print("b")
            serial_available = 1

    elif serial_available == 1:
        # print("asba")
        try:
            bus_number = Arduino.readline()                                     #read from serial port
        except SerialException:
            serial_available = 0
        else:
            if isinstance(bus_number,bytes):                                    #convert from byte to str
                bus_number = bus_number.rstrip()                                #strip carriage return n newline
                bus_number = str(bus_number,'utf-8')
    #bus_number = int(input("ENTER THE BUS NUMBER"))                    #TO SIMULATE READING FROM ARDUINO
            print(bus_number)
            TCP_IP, number_of_buses, condition = get_ip(bus_number)           #call func to get server ip address ann number of buses

            if condition:
                print(number_of_buses)
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)         # create tcp socket with ipv4 packet
                s.settimeout(5.0)                                             # 1 second timeout....will block thread for 1s...change accordingly

                if number_of_buses == 1:
                    print(TCP_IP)
                    try:
                        s.connect((TCP_IP, TCP_PORT))                       # open socket
                    except OSError or AttributeError:                       #PREVENT CRASH
                        s.close()
                        s = None
                    if s is None:
                        print("ERROR")
                    else:
                        s.sendall(message.encode('utf-8'))                  #   send bus stop name
                        s.shutdown(socket.SHUT_WR)
                        s.close()  # shutdown n close socket
                        print("MESSAGE SENT")

                else:
                    for i in range(number_of_buses):
                        print(TCP_IP[i])
                        try:
                            s.connect((TCP_IP[i], TCP_PORT))                #open socket
                        except OSError or AttributeError:                    #PREVENT CRASH
                            print("ERROR")
                            s.close()
                        else:
                            s.sendall(message.encode('utf-8'))              # send bus stop name
                            s.shutdown(socket.SHUT_WR)
                            s.close()                                       # shutdown n close socket
                            print("MESSAGE SENT")


