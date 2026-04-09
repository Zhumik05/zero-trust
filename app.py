from flask import Flask, render_template, redirect
import subprocess

app = Flask(__name__)

def get_clients():
    output = subprocess.getoutput("ip neigh")
    clients = []
 
    for line in output.split("\n"):
        parts = line.split()
        if len(parts) >= 5:
            clients.append({ "ip": parts[0], "mac": parts[4] })
    return clients


def get_logs():
    return subprocess.getoutput("sudo iptables -L")

@app.route("/block/<ip>")
def block_ip(ip):
    subprocess.call("sudo iptables -A INPUT -s {ip} -j DROP", shell=True)
    return redirect("/")

@app.route("/allow/<ip>")
def allow_ip(ip):
    subprocess.call("sudo iptables -A INPUT -s {ip} -j ACCEPT", shell=True)
    return redirect("/")

@app.route("/")
def dashboard():
    clients = get_clients()
    logs = get_logs()
  
    return render_template("index2.html", clients=clients, logs=logs, blocked=blocked)

def get_blocked_count():
    rules = subprocess.getoutput("sudo iptables -L")
    return rules.count("DROP")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

