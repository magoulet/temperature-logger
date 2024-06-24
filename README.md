# Temperature Logger

This project logs temperature and humidity data from a AHT20 (or AM2301B) sensor connected to a Raspberry Pi and stores the data in a MariaDB database. The data is collected every 10 minutes using a cron job.

## Requirements

- Raspberry Pi with I²C enabled
- Python 3.7+
- Virtual environment (`venv`)
- MariaDB server
- Required Python packages:
  - `adafruit-circuitpython-ahtx0`
  - `pymysql`

## Setup

1. Clone the Repository

```bash
git clone https://github.com/magoulet/temperature-logger.git
cd temperature-logger
```

2. Create and Activate a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate
```

3. Install Required Packages

```bash
pip install adafruit-circuitpython-ahtx0 pymysql
```

## Configuration

Copy `config.py.example` to `config.py` and update according to your needs.

## Running the Script

1. Create the Shell Script

Copy `run_script.sh.example` to `run_script.sh` and update according to your setup details.


2. Make the Shell Script Executable


```bash
chmod +x run_script.sh
```

3. Test the Script Manually

```bash
run_script.sh
```

## Setting Up Cron Job

1. Open the crontab configuration:

```bash
crontab -e
```

2. Add the following line to run the script every 10 minutes:

```bash
*/10 * * * * /home/user/projects/temperature-logger/run_script.sh | logger -t temperature-logger
```
making sure to update the path based on your local setup.

## Viewing Logs

### Using `journalctl` on Systemd

- View logs:

```bash
journalctl -t temperature-logger
```

- Follow logs in real-time:

```bash
journalctl -t temperature-logger -f
```

### Using `syslog`

- View logs:

```bash
grep "temperature-logger" /var/log/syslog
```

- Follow logs in real-time:

```bash
tail -f /var/log/syslog | grep "temperature-logger"
```

## License

This project is licensed under the MIT License.
