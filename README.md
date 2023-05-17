# Autoplusnik

Autoplusnik Copyright (C) 2023 Igor Samsonov

Autoplusnik - system for downloading stepik reports and upload it to google sheets.

## Running Autoplusnik

Create a virtual environment (if not already exists):

```bash
$ python3 -m ./.venv/
$ source ./.venv/bin/activate
```

Install libraries:

```bash
$ pip install -r ./requirements.txt
```

And run:

```bash
$ python3 ./Main.py
```

To stop, use Ctrl+C two times.

## Configuring autoplusnik

Open config:

```yaml
debug: false

web-site:
  host: "0.0.0.0"
  port: 17500

plusnik:
  updater:
    path: "./Plusnik/stepik_token.json"
  loader:
    path: "./Plusnik/google_token.json"
```

You can edit debug state (true/false), edit host, edit port.
