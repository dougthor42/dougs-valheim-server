# Doug's Valheim Server Utility


## Installation

Requires Python3.6 or higher.

```shell
git clone git@github.com/dougthor42/dougs-valheim-server.git
cd dougs-valheim-server
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
pip install -e .
```

Create `secrets.json` in the repository root.

```json
{
    "aws_access_key": "foo",
    "aws_secret_access_key": "bar"
}
```

As this point you should be good to go.


## Usage

(Note: the virtual environment made above must be active.)

```
dougs_valheim_server --help
```


### Examples:

```
$ dougs_valheim_server status
The server is UP with an IP address of: 33.99.24.590

$ dougs_valheim_server stop
Stopping server...
Stopped

$ dougs_valheim_server status
The server is STOPPED. Run `dougs_valheim_server start` to start it.

$ dougs_valheim_server start
Starting server...
The server has been started. IP address: 94.123.57.999

$ dougs_valheim_server status
The server is RUNNING with an IP address of: 94.123.57.999
```
