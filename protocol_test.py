import serial
from PIL import Image
import numpy as np
from communication import communication as comm

com = comm.Communication('$', '#', "COM6", 9600)

com.send_packet(com.build_packet("CAMSTATUS"))

com.wait_for_response()

