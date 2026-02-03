#!/usr/bin/env python3
import subprocess
import time

MODES = {
    0: "6d b6 43 ce 97 fe 42 7c e5 15 7d",
    1: "6d b6 43 ce 97 fe 42 7c e4 9c 6c",
    2: "6d b6 43 ce 97 fe 42 7c e5 17 7f",
    3: "6d b6 43 ce 97 fe 42 7c e4 9e 6e",
    4: "6d b6 43 ce 97 fe 42 7c e5 11 79",
    5: "6d b6 43 ce 97 fe 42 7c e4 98 62",
    6: "6d b6 43 ce 97 fe 42 7c e5 13 7b",
    7: "6d b6 43 ce 97 fe 42 7c e4 9a 64",
    8: "6d b6 43 ce 97 fe 42 7c e5 15 7d",
    9: "6d b6 43 ce 97 fe 42 7c e4 9c 66",
}

def hci_cmd(opcode, params):
    cmd = ["/usr/bin/hcitool", "-i", "hci0", "cmd"] + opcode.split() + params.split()
    print(f"[DEBUG] {' '.join(cmd)}")
    subprocess.run(cmd, capture_output=True)

def setup_advertising():
    subprocess.run(["/usr/bin/hciconfig", "hci0", "down"], capture_output=True)
    time.sleep(0.5)
    subprocess.run(["/usr/bin/hciconfig", "hci0", "up"], capture_output=True)
    time.sleep(0.5)
    hci_cmd("0x08 0x0036", "00 13 00 a0 00 00 d2 00 00 07 01 00 00 00 00 00 00 00 00 01 01 00 01 00 00")
    hci_cmd("0x08 0x0035", "00 01 02 03 04 05 06")

def send_mode(mode):
    payload = MODES[mode]
    hci_cmd("0x08 0x0037", f"00 03 01 16 02 01 01 0e ff ff 00 {payload} 03 03 8f ae")
    hci_cmd("0x08 0x0039", "01 01 00 00 00 00 00 00 00 00")
    
    if mode == 0:
        time.sleep(0.5)
        hci_cmd("0x08 0x0039", "00 00 00 00 00 00 00 00 00 00")

def stop():
    time.sleep(0.5)
    hci_cmd("0x08 0x0039", "00 00 00 00 00 00 00 00 00 00")

def print_banner():
    print("=" * 50)
    print("      LOVE SPOUSE EGG CONTROLLER")
    print("=" * 50)
    print()
    print("Commands:")
    print("  0      - Turn OFF")
    print("  1-9    - Vibration modes")
    print("  quit   - Stop and exit")
    print()
    print("=" * 50)
    print()

if __name__ == "__main__":
    print_banner()
    setup_advertising()
    
    while True:
        try:
            cmd = input("\033[34m>>>\033[0m ").strip()
            
            if cmd == "quit":
                stop()
                break
            
            if cmd.isdigit():
                mode = int(cmd)
                if 0 <= mode <= 9:
                    send_mode(mode)
                else:
                    print("[!] Please enter an order between 0 and 9")
            else:
                print("[!] Please enter an order between 0 and 9")
        
        except (KeyboardInterrupt, EOFError):
            print()
            hci_cmd("0x08 0x0037", f"00 03 01 16 02 01 01 0e ff ff 00 6d b6 43 ce 97 fe 42 7c e5 15 7d 03 03 8f ae")
            hci_cmd("0x08 0x0039", "01 01 00 00 00 00 00 00 00 00")
            time.sleep(0.5)
            stop()
            break