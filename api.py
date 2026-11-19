from flask import Flask, render_template, jsonify
from netmiko import ConnectHandler

app = Flask(__name__)


# Router connection settings
router_device = {
    "device_type": "cisco_ios_telnet",
    "ip": "192.168.10.111",
    "port": 32770,
    "username": "admin",
    "password": "eve123",
    "secret": "eve123",
}


# Commands to execute
commands = [
    "show version",
    "show ip interface brief",
    "show running-config",
    "show ip route"
]


# Display the main HTML page
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


# Connect to router and run commands
@app.route("/connect", methods=["POST"])
def connect_router():

    results = {}
    net_connect = None

    try:
        print("Connecting to Cisco router...")

        # Establish router connection
        net_connect = ConnectHandler(**router_device)

        # Enter enable mode
        net_connect.enable()

        print("Router connected successfully!")

        # Run each command
        for command in commands:

            print("Executing:", command)

            output = net_connect.send_command(command)

            results[command] = output

        print("All commands completed!")

        # Return results to HTML as JSON
        return jsonify({
            "success": True,
            "results": results
        })

    except Exception as e:

        print("Connection error:", str(e))

        return jsonify({
            "success": False,
            "error": str(e),
            "results": results
        }), 502

    finally:

        # Close router connection
        if net_connect is not None:
            net_connect.disconnect()
            print("Router disconnected.")


# Start Flask server
if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )