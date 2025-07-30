# ARP Cache Poisoner with Scapy
An awesome python tool for learning about ARP cache poisoning using scapy module. 

> ⚠**Disclaimer:** This project is for **educational and ethical testing** purposes **only**. Unauthorized network tampering is illegal and unethical. Use it **only on networks you own or have explicit permission to test**.

---

## Description

This Python script demonstrates **ARP cache poisoning** using the `scapy` library. It can intercept traffic between a target machine and the gateway by sending forged ARP responses to both, effectively placing the attacker in a **Man-in-the-Middle (MITM)** position.

---

## Features

- Retrieves MAC addresses of gateway and target.
- Sends continuous spoofed ARP responses.
- Restores ARP tables on exit.
- Sniffs and saves network packets using `scapy`.

---

## Requirements

- Python 3.x
- [Scapy](https://scapy.readthedocs.io/en/latest/)
- Root privileges (`sudo`)
- Linux-based OS (Tested on Kali Linux)

Install dependencies:
bash
sudo apt install python3-pip
pip3 install scapy


## Usage
Edit the Script:

Change interface, target_ip, and gateway_ip as per your setup.

Run the Script with Sudo:

bash
Copy
Edit
sudo python3 arp_poisoner.py
Stop Execution:
Press CTRL+C to stop the attack. The script will automatically restore ARP tables.

🧪 Sample Configuration
python
Copy
Edit
interface = 'eth0'
target_ip = '192.168.1.180'
gateway_ip = '192.168.1.1'
📁 Output
Captured packets will be saved to a .pcap file:

bash
Copy
Edit
arper.pcap
You can open it with Wireshark or similar tools.
