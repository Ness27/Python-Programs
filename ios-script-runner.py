"""
Filename: ios-script-runner.py
Description: Run Commands on an IOS-XE Networking Device.
Author: Hunter R.
Date: 2025-07-28
"""
import tkinter as tk
from tkinter import ttk, scrolledtext, font
import netmiko, ipaddress, logging, time, sys


# ️ Configure logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

class IOSXEScriptRunner(tk.Tk):
    def __init__(self):
        startTime = time.perf_counter()
        logging.info("Starting IOS-XE Script Runner Program.")
        super().__init__()
        self.title("IOS-XE Script Runner")
        self._center_window(1200, 700)
        self._setup_style()
        setup_complete = time.perf_counter()
        logging.info(f'Init and Setup Completed in {setup_complete - startTime:.4f} seconds')
        logging.info('Starting Build for UI Interface...')
        self._build_ui()

    def _center_window(self, w, h):
        self.update_idletasks()
        sw, sh = self.winfo_screenwidth(), self.winfo_screenheight()
        x = (sw//2) - (w//2)
        y = (sh//2) - (h//2)
        self.geometry(f"{w}x{h}+{x}+{y}")

    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("clam")
        default = font.nametofont("TkDefaultFont")
        default.configure(size=11)
        self.option_add("*Font", default)
        style.configure("TFrame", background="#EFEFEF")
        style.configure("TLabel", background="#EFEFEF", foreground="#333")
        style.configure("TButton", padding=6)
        style.configure("TLabelframe", background="#EFEFEF")
        style.configure("TLabelframe.Label", font=("Helvetica", 12, "bold"))

    def _build_ui(self):
        startTime = time.perf_counter()
        # Main container
        container = ttk.Frame(self, padding=20)
        container.grid(sticky="NSEW")
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        # Inputs Frame
        inputs = ttk.Labelframe(container, text="Inputs", padding=15)
        inputs.grid(row=0, column=0, sticky="NSEW", padx=(0,10), pady=5)
        inputs.columnconfigure(1, weight=1)

        ttk.Label(inputs, text="Hosts (one per line):").grid(row=0, column=0, sticky="W")
        self.host_txt = tk.Text(inputs, height=8, width=30, bg="white")
        self.host_txt.grid(row=1, column=0, columnspan=2, sticky="EW", pady=5)

        ttk.Label(inputs, text="Commands (one per line):").grid(row=2, column=0, sticky="W", pady=(10,0))
        self.cmd_txt = tk.Text(inputs, height=5, width=30, bg="white")
        self.cmd_txt.grid(row=3, column=0, columnspan=2, sticky="EW", pady=5)

        ttk.Label(inputs, text="Username:").grid(row=4, column=0, sticky="W", pady=(10,0))
        self.user_entry = ttk.Entry(inputs)
        self.user_entry.grid(row=4, column=1, sticky="EW", pady=(10,0))

        ttk.Label(inputs, text="Password:").grid(row=5, column=0, sticky="W", pady=5)
        self.pw_entry = ttk.Entry(inputs, show="*")
        self.pw_entry.grid(row=5, column=1, sticky="EW", pady=5)

        # Buttons Frame
        btns = ttk.Frame(container, padding=(0,10))
        btns.grid(row=1, column=0, sticky="EW")
        btns.columnconfigure((0,1), weight=1)

        run_btn = ttk.Button(btns, text="Run", command=self._on_run)
        run_btn.grid(row=0, column=0, sticky="EW", padx=5)
        quit_btn = ttk.Button(btns, text="Quit", command=self.destroy)
        quit_btn.grid(row=0, column=1, sticky="EW", padx=5)

        # Log Frame
        log_frame = ttk.Labelframe(container, text="Log", padding=15)
        log_frame.grid(row=0, column=1, rowspan=2, sticky="NSEW", pady=5)
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)

        self.log_txt = scrolledtext.ScrolledText(
            log_frame, state="disabled", bg="#1e1e1e", fg="#dcdcdc"
        )
        self.log_txt.grid(sticky="NSEW")
        finishedTime = time.perf_counter()
        logging.info(f"Finished Building UI in {finishedTime - startTime:.4f} seconds")

    def _on_run(self):
        startTime = time.perf_counter()
        logging.info("Starting _on_run function to iterate over commands for each host given.")
        hosts   = self.host_txt.get("1.0", tk.END).strip().splitlines()
        cmds    = self.cmd_txt.get("1.0", tk.END).strip().splitlines()
        user    = self.user_entry.get()
        pwd     = self.pw_entry.get()

        for host in hosts:
            self._append_log(f"🔌 Connecting to {host} over port 22...")
            try:
                theIP = ipaddress.ip_address(host)
                conn = netmiko.ConnectHandler(
                    host=theIP, device_type="cisco_ios",
                    username=user, password=pwd
                )
                self._append_log(f"✅ Connected to {host}")
                for cmd in cmds:
                    self._append_log(f"📤 {cmd}")
                    out = conn.send_command(cmd)
                    self._append_log(f"📥 Output:\n{out}")
                conn.disconnect()
                self._append_log("🔒 Disconnected.\n")
                logging.info('Finished _on_run function for host: {}.'.format(host))
            except ValueError as val:
                self._append_log(f"❌ {val}")
                self._append_log("❌ Skipping {}\n".format(str(val).split(' ')[0]))
                logging.error('{}'.format(val))
                logging.error("Skipping {}".format(str(val).split(' ')[0]))
            except Exception as e:
                self._append_log(f"❌ {e}\n")
                logging.error('There was an error connecting to: {}.'.format(host))

        self._append_log("✅ Completed. Exiting.")
        finishedTime = time.perf_counter()
        logging.info(f"Finished _on_run function in {finishedTime - startTime:.4f} seconds")

    def _append_log(self, msg):
        self.log_txt.config(state="normal")
        self.log_txt.insert(tk.END, msg + "\n")
        self.log_txt.see(tk.END)
        self.log_txt.config(state="disabled")

if __name__ == "__main__":
    IOSXEScriptRunner().mainloop()
