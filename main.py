import tkinter as tk
from tkinter import messagebox, filedialog
import ipaddress
import math

def calculate():
    try:
        hosts_needed = int(entry_hosts.get())
        ip_input = entry_ip.get()

        if hosts_needed <= 0:
            raise ValueError("Host number must be greater than 0.")

        host_bits = math.ceil(math.log2(hosts_needed + 2))  # Add 2 for network + broadcast
        cidr = 32 - host_bits
        usable_hosts = (2 ** host_bits) - 2

        network = ipaddress.ip_network(f"{ip_input}/{cidr}", strict=False)
        first_usable = list(network.hosts())[0]
        last_usable = list(network.hosts())[-1]

        reserved_ips = list(network.hosts())[:5]
        reserved_str = '\n'.join([f"- {ip} → Reserved" for ip in reserved_ips])

        result_text.set(
            f"📡 CIDR Notation: /{cidr}\n"
            f"🟢 Subnet Mask: {network.netmask}\n"
            f"🔵 Wildcard Mask: {network.hostmask}\n"
            f"🌐 Network Address: {network.network_address}\n"
            f"📣 Broadcast Address: {network.broadcast_address}\n"
            f"✅ First Usable IP: {first_usable}\n"
            f"✅ Last Usable IP: {last_usable}\n"
            f"👥 Usable Hosts: {usable_hosts}\n\n"
            f"📌 Reserved IPs (first 5):\n{reserved_str}\n\n"
            f"🔒 Reserved by Mustafa Ali"
        )

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")

def export_to_file():
    content = result_text.get()
    if not content:
        messagebox.showwarning("Export", "No result to export.")
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".txt",
                                             filetypes=[("Text files", "*.txt")])
    if file_path:
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(content)
        messagebox.showinfo("Export", f"Result saved to {file_path}")

# GUI Setup
window = tk.Tk()
window.title("Subnet Calculator")
window.geometry("500x500")
window.resizable(False, False)

result_text = tk.StringVar()

# Input Fields
tk.Label(window, text="Enter Required Hosts:").pack(pady=5)
entry_hosts = tk.Entry(window)
entry_hosts.pack(pady=5)

tk.Label(window, text="Enter Base IP Address:").pack(pady=5)
entry_ip = tk.Entry(window)
entry_ip.pack(pady=5)

# Buttons
tk.Button(window, text="Calculate Subnet", command=calculate).pack(pady=10)
tk.Button(window, text="Export to File", command=export_to_file).pack(pady=5)

# Output Area
tk.Label(window, textvariable=result_text, justify="left", font=("Courier", 10)).pack(pady=10)

window.mainloop()
