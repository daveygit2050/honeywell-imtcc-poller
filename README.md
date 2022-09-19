# Honeywell IMTCC Poller

Tool for polling heating data from [Honeywell International My Total Connect Comfort](https://international.mytotalconnectcomfort.com/Account/Login) and presenting it as [Prometheus](https://prometheus.io/) metrics.

## Installation

This is not yet packaged. To run, you will need to clone the repo with `git` and install the required prerequisites:

* [Python 3.10.4](https://www.python.org/downloads/) or above
* [Poetry 1.2.0](https://python-poetry.org/docs/#installation) or above

You can then run `poetry install` to install the required python libraries.

## Usage

Create environment variables containing your [login credetials](https://international.mytotalconnectcomfort.com/Account/Login):

```bash
$ export HONEYWELL_EMAIL_ADDRESS="foo@example.com"
$ export HONEYWELL_PASSWORD="ThisIsNotARealPassword"
```

You can then run the tool via poetry:

```bash
$ poetry run poll-honeywell
Kitchen: 20.0
Harrys Room: 20.5
Lounge: 19.5
Main Bedroom: 19.5
Hot Water: 48.0
```

The tool will authenticate with the Honeywell API using the login credentials supplied. It will make the calls every 60 seconds in order to get location and zone data.

The Prometheus metrics are made available for scraping on `https://localhost:8000` while the tool is running.

## Limitations

- Assumes you have one location
- Assumes you have zero or one hot water systems
- Limited error handling

## Developing

Running tests:

```bash
$ make test
```
## License

This project is licensed under the terms of the [MIT License](./LICENSE.md).
