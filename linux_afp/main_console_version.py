import os
import subprocess
while True:
    option_choose = int(input("1. Port forward 2. Check iptables 3. Exit\nChoose an option: "))
    match option_choose:
        case 1:
            firewall_input = int(input("1. iptables 2. nftables\nChoose a firewall: "))
            address_line_edit = input("Enter IP address: ")
            port_line_edit = int(input("Enter port: "))
            match firewall_input:
                case 1:
                    command_firewall = f"sudo iptables -A INPUT -p tcp --dport {port_line_edit} -j ACCEPT"
                    os.system(command_firewall)
                    command_portproxy = f"sudo iptables -t nat -A PREROUTING -p tcp -d {address_line_edit} --dport {port_line_edit} -j DNAT --to-destination {address_line_edit}:{port_line_edit}"
                    os.system(command_portproxy)
                case 2:
                    command_nft = f"sudo nft add rule ip nat prerouting tcp dport {port_line_edit} dnat to {address_line_edit}:{port_line_edit}"
                    os.system(command_nft)
        case 2:
            command_update = "sudo iptables -t nat -L -n -v"
            result = subprocess.run(command_update, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                                    text=True)
            if result.returncode == 0:
                print(result.stdout)
            else:
                print("Error: " + result.stderr)
        case 3:
            print("Exiting...")
            break
        case _:
            print("Invalid option, please choose again.")
