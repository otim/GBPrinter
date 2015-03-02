#!/usr/bin/env python

import time
import serial

class PrinterInterface :
    
    def __init__(self, port, baudrate, timeout = 3) :
        # open serial port
        self.ser = serial.Serial(port, baudrate, timeout=timeout)
        print 'trying to connect to port', self.ser.name, 'with baudrate', self.ser.baudrate

        if not self.ser.isOpen() :
            self.ser.open()
            if not self.ser.isOpen() :
                print 'error connecting to port', self.ser.name
                
        # wait for first signal from Arduino
        response = ''
        while True :
            response = self.ser.readline()
            myline = "Gameboy Printer for Arduino\r\n"
            # it seems that the first character received by arduino is empty?
            if response[1:] == myline :
                print response
                print "successfully connected to the Arduino"
                break
            print 'waiting for Arduino to wake up'
            
        # check connection to printer
        self.connected = self.checkConnection()
    
    def serialRequest(self, req) :
        self.ser.write(req)
        return self.ser.readline()
    
    def checkConnection(self) :
        response = self.serialRequest('?')
        if response == '1\r\n' :
            print 'printer is connected'
            print 'reponse', response
            return True
        else :
            print 'printer not detected, check connection and wiring'
            print 'response', response
            return False
        



printerface = PrinterInterface('/dev/tty.usbmodem1411', 9600, 3)

#print ser.inWaiting()
#print ser.read(ser.inWaiting())

response = ''
response = printerface.serialRequest('send_data_start')
print 'response', response

#time.sleep(0.1)

while True :
    print printerface.ser.readline()

#print ser.inWaiting()
#print ser.readLine()

#while True:
#    print ser.read()
