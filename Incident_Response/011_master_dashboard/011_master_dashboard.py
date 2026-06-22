import os
import sys
import subprocess

class CyberSecurityDashboard:

    def __init__(self):
        self.running = True

    @staticmethod
        def clear_screen():
        os.system('cls' if os.name == 'nt' else 'clear')

    def _execute_module(self, script_name, *args):
        if not os.path.exists(script_name):
            print(f"\n[-] Error: Module '{script_name}' not found in the current directory.")
            return
        
        try:
            print(f"\n[*] Handing over control to {script_name}...\n")
            command = [sys.executable, script_name] + list(args)
            subprocess.run(command)
        except Exception as e:
            print(f"\n[-] Module Execution Failure: {e}")

    def run_recon(self):
        self.clear_screen()
        print("[*] Launching Network Reconnaissance Module...")
        self._execute_module("flow_analyzer.py")

    def run_defense(self):
        self.clear_screen()
        print("[*] Launching Active System Defense Module...")
        self._execute_module("watchdog.py")

    def run_response(self):
        self.clear_screen()
        print("[*] Launching Incident Response Engine...")
        target = input("    Enter target directory for IR scan: ").strip()
        if target:
            self._execute_module("ir_engine.py", target)
        else:
            print("[-] Aborted: Target directory cannot be empty.")

    def run_alert(self):
        self.clear_screen()
        print("[*] Launching Cloud Log Alert System...")
        self._execute_module("cloud_alert.py")

    def display_menu(self):
        self.clear_screen()
        print("="*50)
        print("      CYBERSECURITY MASTER DASHBOARD - 2026")
        print("="*50)
        print("    1. Network Reconnaissance (flow_analyzer)")
        print("    2. Active System Defense (watchdog)")
        print("    3. Incident Response & Vaccine (ir_engine)")
        print("    4. Cloud Log Alert System (cloud_alert)")
        print("    0. Exit Dashboard")
        print("="*50)

    def start(self):
        while self.running:
            self.display_menu()
            try:
                option = input("\n    Select an action: ").strip()

                if option == "1":
                    self.run_recon()
                elif option == "2":
                    self.run_defense()
                elif option == "3":
                    self.run_response()
                elif option == "4":
                    self.run_alert()
                elif option == "0":
                    print("\n[+] Dashboard shut down. Finalizing logs...")
                    sys.exit(0)
                else:
                    print("\n[-] Invalid selection. Please try again.")

                input("\n[*] Press Enter to return to menu...")
            except KeyboardInterrupt:
                print("\n\n[!] Dashboard forcefully shut down by operator.")
                sys.exit(0)

if __name__ == "__main__":
    dashboard = CyberSecurityDashboard()
    dashboard.start()
