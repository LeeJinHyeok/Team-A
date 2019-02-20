from btserver import BTServer
from bterror import BTError

import argparse
import asyncore
import json
from random import uniform
from threading import Thread
from time import sleep, time
from neo import Gpio

if __name__ == '__main__':
    # Create option parser
    usage = "usage: %prog [options] arg"
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", dest="output_format", default="csv", help="set output format: csv, json")

    args = parser.parse_args()

    # Create a BT server
    uuid = "94f39d29-7d6d-437d-973b-fba39e49d4ee"
    service_name = "GossipBTServer"
    server = BTServer(uuid, service_name)

    # Create the server thread and run it
    server_thread = Thread(target=asyncore.loop, name="Gossip BT Server Thread")
    server_thread.daemon = True
    server_thread.start()

    while True:
        for client_handler in server.active_client_handlers.copy():
            # Use a copy() to get the copy of the set, avoiding 'set change size during iteration' error
            # Create CSV message "'realtime', time, temp, SN1, SN2, SN3, SN4, PM25\n"

            epoch_time = int(time())    # epoch time
            neo = Gpio()

            S0 = 2  # pin to use
            S1 = 3
            S2 = 4
            S3 = 5

            pinNum = [S0, S1, S2, S3]

            num = [0, 0, 0, 0]

            # Blink example
            for i in range(4):
                neo.pinMode(pinNum[i], neo.OUTPUT)


            #Temperature sensor
            neo.digitalWrite(pinNum[0], 0)
            neo.digitalWrite(pinNum[1], 0)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)



            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c0 = raw * scale
            temp_celsius = (c0-590) / 10
            temp = (temp_celsius * 1.8) +32




            #Alphasense SN1
            neo.digitalWrite(pinNum[0], 0)
            neo.digitalWrite(pinNum[1], 1)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c2 = raw * scale

            neo.digitalWrite(pinNum[0], 1)
            neo.digitalWrite(pinNum[1], 1)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c3 = raw * scale

            SN1 = ((c2 - 286) - 0.75*(c3 - 292))*3.876
            SN1 = SN1 if (SN1 >= 0) else -SN1

            #Alphasense SN2
            neo.digitalWrite(pinNum[0], 0)
            neo.digitalWrite(pinNum[1], 0)
            neo.digitalWrite(pinNum[2], 1)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c4 = raw * scale

            neo.digitalWrite(pinNum[0], 1)
            neo.digitalWrite(pinNum[1], 0)
            neo.digitalWrite(pinNum[2], 1)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c5 = raw * scale

            SN2 = ((c4-417)- 0.5*(c5-402))* 2.5445
            SN2 = SN2 if (SN2 >= 0) else -SN2

            #Alphasense SN3
            neo.digitalWrite(pinNum[0], 0)
            neo.digitalWrite(pinNum[1], 1)
            neo.digitalWrite(pinNum[2], 1)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c6 = raw * scale

            neo.digitalWrite(pinNum[0], 1)
            neo.digitalWrite(pinNum[1], 1)
            neo.digitalWrite(pinNum[2], 1)
            neo.digitalWrite(pinNum[3], 0)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c7 = raw * scale

            SN3 = ((c6 -265)-0.44*(c7-281))*3.4246
            SN3 = SN3 if (SN3 >= 0) else -SN3


            #Alphasense SN4
            neo.digitalWrite(pinNum[0], 0)
            neo.digitalWrite(pinNum[1], 0)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 1)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c8 = raw * scale

            neo.digitalWrite(pinNum[0], 1)
            neo.digitalWrite(pinNum[1], 0)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 1)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c9 = raw * scale

            SN4 = ((c8 - 275)-0.6*(c9-295))*3.4722
            SN4 = SN4 if (SN4 >= 0) else -SN4


            #PM2.5
            neo.digitalWrite(pinNum[0], 1)
            neo.digitalWrite(pinNum[1], 1)
            neo.digitalWrite(pinNum[2], 0)
            neo.digitalWrite(pinNum[3], 1)
            sleep(0.05)

            raw = int(open("/sys/bus/iio/devices/iio:device0/in_voltage0_raw").read())
            scale = float(open("/sys/bus/iio/devices/iio:device0/in_voltage_scale").read())
            c11= (raw * scale) / 1000

            hppcf = (240.0 * pow(c11, 6) - 2491.3 * pow(c11, 5) + 9448.7 * pow(c11, 4) - 14840.0 * pow(c11, 3) + 10684.0 * pow(c11, 2) + 2211.8 * (c11) + 7.9623)
            PM25 = 0.518 + .00274 * hppcf

            #AQI Convesion for NO2_SN1
            if SN1>=0 and SN1<=53 :
                AQI_NO2 = ((50-0)*(SN1 - 0))/(53-0)+0
            elif SN1 >= 54 and SN1 <= 100 :
                AQI_NO2 = ((100-51)*(SN1-54))/(100-54) + 51
            elif SN1 >= 101 and SN1 <= 360 :
                AQI_NO2 = ((150-101)*(SN1-101))/(360-101) + 101
            elif SN1 >= 361 and SN1 <= 649 :
                AQI_NO2 = ((200-151)*(SN1-361))/(649-361) + 151
            elif SN1 >= 650 and SN1 <= 1249 :
                AQI_NO2 = ((300-201)*(SN1-650))/(1249-650) + 201
            elif SN1 >= 1250 and SN1 <= 1649 :
                AQI_NO2 = ((400-301)*(SN1-1250))/(1649-1250) + 301
            elif SN1 >= 1650 and SN1 <= 2049 :
                AQI_NO2 = ((500-401)*(SN1-1650))/(2049-1650) + 401
            else:
                AQI_NO2 = 500

            # AQI Convesion for O3_SN2
            if SN2 >= 0 and SN2 <= 53:
                AQI_NO2 = ((50 - 0) * (SN1 - 0)) / (53 - 0) + 0
            elif SN2 >= 54 and SN2 <= 100:
                AQI_NO2 = ((100 - 51) * (SN1 - 54)) / (100 - 54) + 51
            elif SN2 >= 101 and SN2 <= 360:
                AQI_NO2 = ((150 - 101) * (SN1 - 101)) / (360 - 101) + 101
            elif SN2 >= 361 and SN2 <= 649:
                AQI_NO2 = ((200 - 151) * (SN1 - 361)) / (649 - 361) + 151
            elif SN2 >= 650 and SN2 <= 1249:
                AQI_NO2 = ((300 - 201) * (SN1 - 650)) / (1249 - 650) + 201
            elif SN2 >= 1250 and SN2 <= 1649:
                AQI_NO2 = ((400 - 301) * (SN1 - 1250)) / (1649 - 1250) + 301
            elif SN2 >= 1650 and SN2 <= 2049:
                AQI_NO2 = ((500 - 401) * (SN1 - 1650)) / (2049 - 1650) + 401
            else:
                AQI_NO2 = 500

            # AQI Convesion for CO_SN3
            if SN3 >= 0 and SN3 <= 4.4:
                AQI_CO = ((50 - 0) * (SN3 - 0)) / (4.4 - 0) + 0
            elif SN3 > 4.4 and SN3 <= 9.4:
                AQI_CO = ((100 - 51) * (SN3 - 4.4)) / (9.4 - 4.5) + 51
            elif SN3 > 9.4 and SN3 <= 12.4:
                AQI_CO = ((150 - 101) * (SN3 - 9.4)) / (12.4 - 9.5) + 101
            elif SN3 > 12.4 and SN3 <= 649:
                AQI_CO = ((200 - 151) * (SN3 - 12.4)) / (15.4 - 12.5) + 151
            elif SN3 > 650 and SN3 <= 1249:
                AQI_CO = ((300 - 201) * (SN3 - )) / (1249 - 650) + 201
            elif SN3 > 1250 and SN3 <= 1649:
                AQI_CO = ((400 - 301) * (SN3 - 1250)) / (1649 - 1250) + 301
            elif SN3 > 1650 and SN3 <= 2049:
                AQI_CO = ((500 - 401) * (SN3 - 1650)) / (2049 - 1650) + 401
            else:
                AQI_CO = 500

            msg = ""
            if args.output_format == "csv":
                msg = "realtime, {}, {}, {}, {}, {}, {}, {}".format(epoch_time, temp, SN1, SN2, SN3, SN4, PM25)
            elif args.output_format == "json":
                output = {'type': 'realtime',
                          'time': epoch_time,
                          'temp': temp,
                          'NO2_AQI': AQI_NO2,
                          'O3_AQI': SN2,
                          'CO_AQI': SN3,
                          'SO2_AQI': SN4,
                          'PM25_AQI': PM25}
                msg = json.dumps(output)
            try:
                client_handler.send((msg + '\n').encode('ascii'))
            except Exception as e:
                BTError.print_error(handler=client_handler, error=BTError.ERR_WRITE, error_message=repr(e))
                client_handler.handle_close()

            # Sleep for 3 seconds
        sleep(2.5)

