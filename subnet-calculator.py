"""
Filename: subnet-calculator.py
Description: An application for network administrators and engineers to calculator network subnets.
Author: Hunter R.
Date: 2025-07-27
"""

import argparse
import logging
import sys
import time
import ipaddress
import tkinter as tk
from tkinter import ttk, scrolledtext

# ️ Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.StreamHandler(sys.stdout)],
    level=logging.INFO,
)

def configure_style(theRoot):
    style = ttk.Style(theRoot)
    style.theme_use("clam")
    # Base font
    default_font = ("Segoe UI", 10)
    heading_font = ("Segoe UI", 11, "bold")

    # Frame backgrounds
    style.configure("TFrame", background="#F5F5F5")
    style.configure("TLabelFrame", background="#F5F5F5", font=heading_font)
    style.configure("TLabel", background="#F5F5F5", font=default_font, foreground="#333")
    style.configure("TEntry", font=default_font)
    style.configure("TButton", font=default_font, padding=6)
    style.map("TButton",
              foreground=[("pressed", "#fff"), ("!pressed", "#fff")],
              background=[("pressed", "#006400"), ("!pressed", "#228B22")])
    return style

def showResults(parent, resultData):
    win = tk.Toplevel(parent)
    win.title("Network Results")
    win.geometry("450x500")
    win.tk.eval(f'tk::PlaceWindow {str(win)} center')

    win.configure(background="#F5F5F5")
    win.resizable(False, False)

    content = ttk.Frame(win, padding=15)
    content.grid(sticky="NSEW")
    content.columnconfigure(1, weight=1)

    # Display summary info
    row = 0
    for key, val in resultData.items():
        if key != "Available Hosts":
            ttk.Label(content, text=f"{key}:").grid(row=row, column=0, sticky="W", pady=2)
            ttk.Label(content, text=val).grid(row=row, column=1, sticky="W", pady=2)
            row += 1

    # Hosts label
    ttk.Label(content, text="Available Hosts:", font=("Segoe UI", 10, "bold")) \
        .grid(row=row, column=0, sticky="W", pady=(10,2))
    row += 1

    # Host list display
    host_display = scrolledtext.ScrolledText(
        content, height=10, wrap="none", state="disabled", font=("Consolas", 9)
    )
    host_display.grid(row=row, column=0, columnspan=2, sticky="NSEW")
    row += 1

    # Paging controls
    hosts = resultData["Available Hosts"]
    page_size = 10
    current_page = [0]

    def update_page():
        start = current_page[0] * page_size
        end = start + page_size
        text = "\n".join(hosts[start:end]) or "— none —"
        host_display.config(state="normal")
        host_display.delete("1.0", tk.END)
        host_display.insert(tk.END, text)
        host_display.config(state="disabled")

    def prev_page():
        if current_page[0] > 0:
            current_page[0] -= 1
            update_page()

    def next_page():
        if (current_page[0] + 1) * page_size < len(hosts):
            current_page[0] += 1
            update_page()

    update_page()
    ctrl_frame = ttk.Frame(content, padding=(0,10))
    ctrl_frame.grid(row=row, column=0, columnspan=2)
    ttk.Button(ctrl_frame, text="⟨ Prev", command=prev_page).pack(side="left", padx=5)
    ttk.Button(ctrl_frame, text="Next ⟩", command=next_page).pack(side="left", padx=5)
    row += 1

    # Close button
    ttk.Button(content, text="Close", command=win.destroy) \
        .grid(row=row, column=0, columnspan=2, pady=(10,0))

def networkEval(networkBoth):
    iface = ipaddress.ip_interface(networkBoth)
    net = iface.network

    hosts = [str(ip) for idx, ip in enumerate(net.hosts()) if idx < 512]
    return {
        "Network Address": str(net.network_address),
        "Broadcast Address": str(net.broadcast_address),
        "Subnet Mask": str(iface.netmask),
        "Wildcard Mask": str(iface.hostmask),
        "Private Network Space": str(iface.is_private),
        "Public Network Space": str(iface.is_global),
        "Total Number of Hosts": str(net.num_addresses),
        "Number of Usable Hosts": str(max(net.num_addresses - 2, 0)),
        "Available Hosts": hosts
    }

def windowCreation():
    root = tk.Tk()
    configure_style(root)
    root.title("Subnet Calculator")
    root.geometry("420x150")
    root.eval('tk::PlaceWindow . center')
    root.configure(background="#F5F5F5")
    root.resizable(False, False)

    # Main container
    main = ttk.Frame(root, padding=20)
    main.grid(sticky="NSEW")
    main.columnconfigure(1, weight=1)

    # Input
    ttk.Label(main, text="Enter IP/Subnet (e.g. 10.1.1.1/24):") \
        .grid(row=0, column=0, sticky="W", pady=5)
    net_entry = ttk.Entry(main, width=30)
    net_entry.insert(0, "10.1.1.1/24")
    net_entry.grid(row=0, column=1, sticky="EW", pady=5, padx=(5,0))

    # Buttons
    btn_frame = ttk.Frame(main, padding=(0,10))
    btn_frame.grid(row=1, column=0, columnspan=2)
    ttk.Button(btn_frame, text="Run",
               command=lambda: showResults(root, networkEval(net_entry.get()))) \
        .pack(side="left", padx=10)
    ttk.Button(btn_frame, text="Quit", command=root.destroy) \
        .pack(side="left", padx=10)

    root.mainloop()

def main():
    start = time.perf_counter()

    logging.info("Starting GUI...")

    setup_complete = time.perf_counter()
    logging.info(f'Init in {setup_complete - start:.4f}s')

    windowCreation()

    logging.info("Program finished.")
    logging.shutdown()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logging.warning("Interrupted by user.")
        sys.exit(0)
    except Exception as e:
        logging.exception(f"Unexpected error: {e}")
        sys.exit(1)
