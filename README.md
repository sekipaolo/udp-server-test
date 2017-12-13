# Description

Simmple service for converting a datetime based log message  into a timestamp based json dictionary 
INPUT:   [DD/MM/YYYY HH:MM] MESSAGE BODY
OUTPUT:  {"timestamp": EPOCH, "message": "MESSAGE BODY"}

# Run

Make sure you have installed docker

Run:

´´´sh
make run
´´´

and test with

´´´sh
echo -n '[17/06/2016 12:30] Time to move' | nc -u 127.0.0.1 1234
´´´

you should get this output:

´´´sh
{"timestamp": "1466116200", "message": "Time to move"}
´´´
