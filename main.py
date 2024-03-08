import pydivert
import datetime


def find_ip():
    with pydivert.WinDivert(
            "udp.DstPort >= 30000 and udp.DstPort <= 31000") as w:
        while True:
            packet = w.recv()
            if packet:
                ip = str(packet.ipv4.dst_addr) + ":" + str(packet.udp.dst_port);
                break

            w.send(packet)
    return ip


def log(text):
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log_message = f"{timestamp} - {text}"
    print(log_message)


log('===============================================')
log('============Insane Simple IP Finder...=========')
log('===============================================\n')

log('Please connect to a game... Finding ip...')

ip = find_ip()

log('Ip found: ' + str(ip))
