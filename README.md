## Requirements

1. Set the python version to 3.8:
```bash
scl enable rh-python38 bash
```

2. [Install poetry](https://python-poetry.org/docs/#installation) to manage dependencies.

3. Install the required dependencies:
```bash
poetry install
```

## Usage

Set the environment: 
```bash
scl enable rh-python38 bash
poetry shell
```

Start the RPC server and leave it running:
```bash
python magnetrpc.py
```

Open in parallel the dash and the logging script:
```bash
python magnetdash.py &
python magnetlog.py &
```

The data will be saved in the `log` subfolder. Open [localhost:8080](http://localhost:8080) to visit the momitoring page.