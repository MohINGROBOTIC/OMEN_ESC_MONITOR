# -*- coding:utf-8 -*-
import RPi.GPIO as GPIO
import serial
import time
import math # Required for temp calcs
import mysql.connector


#Constants
SERIESRESISTOR = 10000
NOMINAL_RESISTANCE = 10000
NOMINAL_TEMPERATURE = 25
BCOEFFICIENT = 3455

# Data buffer format
# 0: Voltage Low 
# 1: Voltage High
# 2: Temperature Low 
# 3: Temperature High
# 4: Bus Current Low
# 5: Bus Current High
# 6: Reserved (Not Used)
# 7: Reserved (Not Used)
# 8: ERPM 1
# 9: ERPM 2
# 10: ERPM 3
# 11: ERPM 4
# 12: Throttle Duty Low
# 13: Throttle Duty High
# 14: Motor Duty Low
# 15: Motor Duty High
# 16: Status Flags
# 17: Reserved (Not Used)
# 18: Fletcher Checksum Low
# 19: Fletcher Checksum High
# 20: Stop Byte Low
# 21: Stop Byte High

# Process data from given input array
def ReadDataBuffer(buffer, esc):
    # connect to the database named ESC_OMEN using credentials
    cnx = mysql.connector.connect(user='mabus', password='seren1ty',
                                  host='localhost',
                                  database='ESC_OMEN')

    if len(buffer) != 22: #Size check
        print("malformed")
        return #Ignore malformed data packets

    if ((buffer[20] != 255) or (buffer[21] != 255)):
        print("stop")
        return; #Stop byte of 65535 not received

    int_packet_fletcher = ((buffer[19] << 8) | buffer[18]) # Fletcher received from packet
    int_calculated_fletcher = CheckFletcherChecksum(buffer) 
    if int_packet_fletcher != int_calculated_fletcher:
        return #Ignore failed fletcher check packets

    # Process Input Voltage    
    flt_voltage = float(((buffer[1] << 8) + buffer[0]) / 100) #Voltage

    # Process Input Temperature
    flt_temp_raw = float((buffer[3] << 8) + buffer[2]) 
    flt_Rntc = float(4096 / flt_temp_raw) - 1
    flt_Rntc = SERIESRESISTOR / flt_Rntc
    flt_temperature = float(flt_Rntc / NOMINAL_RESISTANCE) # (R/Ro)
    flt_temperature = float(math.log(flt_temperature)) #ln(R/Ro)
    flt_temperature /= BCOEFFICIENT #1/B * ln(R/Ro)

    flt_temperature += float(1.0) / (NOMINAL_TEMPERATURE + float(273.15)) # (1/To)
    flt_temperature = float(1.0) / flt_temperature #Invert
    flt_temperature -= float(273.15) #convert to Celcius

    # filter bad values
    if (flt_temperature < 0 or flt_temperature > 200):
        flt_temperature = 0

    # Process Bus Current
    flt_bus_current = float(((buffer[5] << 8) + buffer[4]) / 12.5) #Bus current

    # Process ERPM and RPM
    int_eRPM = int((buffer[11] << 24) + (buffer[10] << 16) + (buffer[9] << 8) + (buffer[8] << 0)) # ERPM
    int_pole_count = 2 #Change this to motor pole count, default is 2 for ERPM
    int_RPM = int_eRPM / int_pole_count #RPM

    # Process Throttle Duty Cycle
    int_throttle_duty = int(((buffer[13] << 8) + buffer[12]) / 100) # Throttle Duty Cycle

    # Process Motor Duty Cycle
    int_motor_duty = int(((buffer[15] << 8) + buffer[14]) / 100) # Motor Duty Cycle

    # Calculate Power
    flt_power = float(flt_voltage * flt_bus_current) #Input Power

    # Calculate phase current
    # Note, values under 25% should be discarded due to high amounts of noise
    #flt_phase_current = float(flt_bus_current / int_motor_duty)

    print("Voltage: ")
    print(flt_voltage)
    print("Amperage: ")
    print(flt_bus_current)
    print("Temperature: ")
    print(flt_temperature)


    # Status Flags
    # Bit position in byte indicates flag set, 1 is set, 0 is default
    # Bit 0: Motor Started, set when motor is running as expected
    # Bit 1: Motor Saturation Event, set when saturation detected and power is reduced for desync protection
    # Bit 2: ESC Over temperature event occuring, shut down method as per configuration
    # Bit 3: ESC Overvoltage event occuring, shut down method as per configuration
    # Bit 4: ESC Undervoltage event occuring, shut down method as per configuration
    # Bit 5: Startup error detected, motor stall detected upon trying to start
    int_status_flags = int(buffer[16])
    print("status:")
    print(int_status_flags)

    query = WriteDataBase(esc)
    cursor = cnx.cursor()

    data = (flt_voltage, flt_bus_current, flt_temperature)
    cursor.execute(query, data)
    cnx.commit()
    cursor.close()
    cnx.close()

def WriteDataBase(ESC):
    #Match the esc value with the table to insert into
    if (ESC == 1):
        add_data = ("INSERT INTO esc1 "
                    "(VOLT, AMP, TEMP) "
                    "VALUES (%s, %s, %s)")
    elif (ESC == 2):
        add_data = ("INSERT INTO esc2 "
                    "(VOLT, AMP, TEMP) "
                    "VALUES (%s, %s, %s)")
    elif (ESC == 3):
        add_data = ("INSERT INTO esc3 "
                    "(VOLT, AMP, TEMP) "
                    "VALUES (%s, %s, %s)")
    elif (ESC == 4):
        add_data = ("INSERT INTO esc4 "
                    "(VOLT, AMP, TEMP) "
                    "VALUES (%s, %s, %s)")
    elif (ESC == 5):
        add_data = ("INSERT INTO esc5 "
                    "(VOLT, AMP, TEMP) "
                    "VALUES (%s, %s, %s)")
    elif (ESC == 6):
        add_data = ("INSERT INTO esc6 "
                    "(VOLT, AMP, TEMP) "
                    "VALUES (%s, %s, %s)")
    elif (ESC == 7):
        add_data = ("INSERT INTO esc7 "
                    "(VOLT, AMP, TEMP) "
                    "VALUES (%s, %s, %s)")
    elif (ESC == 8):
        add_data = ("INSERT INTO esc8 "
                    "(VOLT, AMP, TEMP) "
                    "VALUES (%s, %s, %s)")

    return add_data



#Calculate Fletcher Checksum
def CheckFletcherChecksum(buffer):
    int_fCCRC16 = 0
    i = 0
    int_c0 = 0
    int_c1 = 0

    for i in range(18): # Buffer Length - 2, ignore fletcher bits in calculation
        int_c0 = int(int_c0 + (buffer[i])) % 255
        int_c1 = int(int_c1 + int_c0) % 255

    # Assemble the 16-bit checksum value
    int_fCCRC16 = (int_c1 << 8) | int_c0
    return int_fCCRC16



esc8 = serial.Serial("/dev/ttySC7",115200,timeout=1)
esc7 = serial.Serial("/dev/ttySC6",115200,timeout=1)
esc6 = serial.Serial("/dev/ttySC5",115200,timeout=1)
esc5 = serial.Serial("/dev/ttySC4",115200,timeout=1)
esc4 = serial.Serial("/dev/ttySC3",115200,timeout=1)
esc3 = serial.Serial("/dev/ttySC2",115200,timeout=1)
esc2 = serial.Serial("/dev/ttySC1",115200,timeout=1)
esc1 = serial.Serial("/dev/ttySC0",115200,timeout=1)

esc8.flushInput()
esc7.flushInput()
esc6.flushInput()
esc5.flushInput()
esc4.flushInput()
esc3.flushInput()
esc2.flushInput()
esc1.flushInput()


while 1:
    print("Listening")
    while esc1.inWaiting() > 0 or esc2.inWaiting() > 0  or esc3.inWaiting() > 0  or esc4.inWaiting() > 0  or esc5.inWaiting() > 0   or esc6.inWaiting() > 0  or esc7.inWaiting() > 0  or esc8.inWaiting() > 0 :
        #check to see which serial port is reading data (avoid sending null array)
        if esc1.inWaiting() > 0:
            print("reading ESC 1")
            ReadDataBuffer(esc1.read_until(b'\xff\xff'), 1)
            esc1.flushInput()
        if esc2.inWaiting() > 0:
            print("reading ESC 2")
            ReadDataBuffer(esc2.read_until(b'\xff\xff'), 2)
            esc2.flushInput()
        if esc3.inWaiting() > 0:
            print("reading ESC 3")
            ReadDataBuffer(esc3.read_until(b'\xff\xff'), 3)
            esc3.flushInput()
        if esc4.inWaiting() > 0:
            print("reading ESC 4")
            ReadDataBuffer(esc4.read_until(b'\xff\xff'), 4)
            esc4.flushInput()
        if esc5.inWaiting() > 0:
            print("reading ESC 5")
            ReadDataBuffer(esc5.read_until(b'\xff\xff'), 5)
            esc5.flushInput()
        if esc6.inWaiting() > 0:
            print("reading ESC 6")
            ReadDataBuffer(esc6.read_until(b'\xff\xff'), 6)
            esc6.flushInput()
        if esc7.inWaiting() > 0:
            print("reading ESC 7")
            ReadDataBuffer(esc7.read_until(b'\xff\xff'), 7)
            esc7.flushInput()
        if esc8.inWaiting() > 0:
            print("reading ESC 8")
            ReadDataBuffer(esc8.read_until(b'\xff\xff'), 8)
            esc8.flushInput()
        time.sleep(0.5)

    

