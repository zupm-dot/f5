import paramiko
import re
import datetime
import getpass
import json

USERNAME = "root"
PASSWORD = getpass.getpass("Enter password for all F5 devices: ")
EXPIRY_THRESHOLD_DAYS = 45
GRACE_PERIOD_DAYS = 5  # Include recently expired
HOSTS_FILE = "f5_hosts.txt"

def load_f5_hosts(filename=HOSTS_FILE):
    with open(filename, "r") as file:
        return [line.strip() for line in file if line.strip()]

def get_ssh_connection(host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(host, username=USERNAME, password=PASSWORD, timeout=10)
    return ssh

def parse_cert_blocks(output, today, label):
    certs = []
    current_item = None

    for line in output.splitlines():
        if line.startswith(f"sys crypto {label}"):
            current_item = line.strip()
        elif "expiration" in line and current_item:
            match = re.search(r"expiration\s+([A-Za-z]{3})\s+(\d{1,2})\s+(\d{2}:\d{2}:\d{2})\s+(\d{4})", line)
            if match:
                month, day, time_str, year = match.groups()
                date_str = f"{month} {int(day)} {time_str} {year}"
                try:
                    expiry = datetime.datetime.strptime(date_str, "%b %d %H:%M:%S %Y")
                    delta = (expiry - today).days
                    if -GRACE_PERIOD_DAYS <= delta <= EXPIRY_THRESHOLD_DAYS:
                        certs.append({
                            "type": label.upper(),
                            "name": current_item,
                            "expires_on": expiry.strftime("%Y-%m-%d %H:%M:%S"),
                            "days_until_expiry": delta
                        })
                except ValueError:
                    continue
    return certs

def scan_f5_certificates(host):
    try:
        ssh = get_ssh_connection(host)
        today = datetime.datetime.utcnow()

        cmd_cert = "tmsh -q -c 'cd /; list sys crypto recursive cert' | grep '^sys\\|expiration'"
        cmd_bundle = "tmsh -q -c 'cd /; list sys crypto recursive cert-bundle' | grep '^sys\\|expiration'"

        stdin, stdout, _ = ssh.exec_command(cmd_cert)
        output_cert = stdout.read().decode()

        stdin, stdout, _ = ssh.exec_command(cmd_bundle)
        output_bundle = stdout.read().decode()
        ssh.close()

        results = []
        results += parse_cert_blocks(output_cert, today, "cert")
        results += parse_cert_blocks(output_bundle, today, "cert-bundle")
        return {"host": host, "expiring_items": results}

    except Exception as e:
        return {"host": host, "error": str(e)}

def main():
    hosts = load_f5_hosts()
    if not hosts:
        print("No hosts found in f5_hosts.txt.")
        return

    print("Available F5 Hosts:")
    for h in hosts:
        print(f" - {h}")

    selected = input("\nEnter a hostname to scan one device, or press Enter to scan all: ").strip()

    if selected:
        if selected not in hosts:
            print(f"\n'{selected}' not found in host list.")
            return
        hosts = [selected]

    results = []
    for host in hosts:
        result = scan_f5_certificates(host)
        if result.get("expiring_items"):
            print(f"\n🔍 Scanning {host}...")
            results.append(result)

    print("\nJSON Output:")
    print(json.dumps(results, indent=2))


if __name__ == "__main__":
    main()
