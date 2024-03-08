import pydivert
import datetime
import requests

USERNAME = "Insane"
DISCORD_WEBHOOK_URL = "YOUR_WEBHOOK"


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


def send_to_discord(message):
    payload = {"content": message}
    headers = {"Content-Type": "application/json"}

    try:
        response = requests.post(DISCORD_WEBHOOK_URL, json=payload, headers=headers)
        response.raise_for_status()
        log(f"Discord webhook sent!\n")
    except requests.exceptions.RequestException as e:
        log(f"Failed to send Discord webhook. Error: {e}")


def log(text):
    timestamp = datetime.datetime.now().strftime("%d-%m-%Y %H:%M:%S")
    log_message = f"{timestamp} - {text}"
    print(log_message)


log('===============================================')
log('============Insane Simple IP Finder...=========')
log('===============================================\n')

log('Please connect to a game.\n')
log('Finding ip...\n')

ip = find_ip()

log('Ip found: ' + str(ip) + '\n')
send_to_discord(USERNAME + ':' + str(ip))
