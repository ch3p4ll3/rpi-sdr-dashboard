from flask import Flask, render_template, request
from os.path import exists
from execute_commands import ExecuteCommands
from json import load

app = Flask(
    __name__,
    static_url_path='/static',
    static_folder='www-data/static'
)

commands = ExecuteCommands()

if not exists("./config"):
    with open("./config", "w") as f:
        f.write("")
else:
    with open("./config", "r") as f:
        service_name = f.readline()

        if service_name:
            commands.start_service(service_name)


@app.route("/")
def index():
    active_config = None
    server_ip = request.base_url.removesuffix("/")
    with open("./config", "r") as f:
        active_config = f.readline()

    with open("./configurations.json", "r") as f:
        configs = load(f)

    return render_template(
        'index.html',
        active_config=active_config,
        json_configs=configs,
        server_ip=server_ip,
        hostapd_active=commands.check_hostapd_is_active()
    )


@app.route("/stop_all_services")
def stop_all_services():
    try:
        with open("./configurations.json", "r") as f:
            configs = load(f)

        for service in configs.get("services", []):
            commands.stop_service(service.get("name", ""))

        with open("./config", "w") as f:
            f.write("")

        return {
            "status": True,
            "description": ""
        }
    except Exception as e:
        print(e)
        return {
            "status": False,
            "description": str(e)
        }


@app.route("/stop_service/<service_name>")
def stop_service(service_name: str = None):
    try:
        commands.stop_service(service_name)

        with open("./config", "w") as f:
            f.write("")

        return {
            "status": True,
            "description": ""
        }
    except Exception as e:
        return {
            "status": False,
            "description": str(e)
        }


@app.route("/start_service/<service_name>")
def start_service(service_name: str = None):
    try:
        commands.start_service(service_name)

        with open("./config", "w") as f:
            f.write(service_name)
        return {
            "status": True,
            "description": ""
        }
    except Exception as e:
        return {
            "status": False,
            "description": str(e)
        }


@app.route("/execute_command/<command_name>")
def execute_command(command_name: str):
    print(command_name)
    commands.run_commands(command_name)

    return {
        "ok": "ok"
    }
