import datetime
import subprocess


# get_leap_week_dn calculates GPS week and dn as if leap was
# scheduled for yesterday's night. The offset allows to move it
# forwards or backwards by days
def get_leap_week_dn(offset=0):
    start_time_gps = datetime.datetime(
        1980, 1, 6,
        hour=0, minute=0, second=0, microsecond=0)
    now = datetime.datetime.now(datetime.UTC)
    leap = datetime.datetime(
        now.year, now.month, now.day, hour=0, minute=0, second=0,
        microsecond=0) + datetime.timedelta(days=offset)
    diff = leap - start_time_gps
    weeks = diff.days // 7
    dn = diff.days % 7
    return now, weeks, dn


def play_samples(path):
    command = [
        '/usr/local/bin/hackrf_transfer',
        '-t',
        f'{path}',
        '-f',
        '1575420000',
        '-s',
        '2600000',
        '-a',
        '1',
        '-x',
        '0'
    ]
    result = subprocess.run(command, check=True)
    if result.returncode != 0:
        print("error playing samples")
        exit(1)


# Generates gps simulator samples for leap tonight:
def generate_samples(start, weeks, dn, file, ls):
    commands = [[
        '/usr/local/bin/gps-sdr-sim',
        '-e',
        '/brdc1240.24n',
        '-l',
        '42.3569048,-71.2564075,0',
        '-b',
        '8',
        '-d',
        '1800',
        '-T',
        f"{start.year}/{start.month}/{start.day},{start.hour}:{start.minute}",
        '-L',
        f'{weeks},{dn},{ls}',
        '-o',
        file
    ]]
    for command in commands:
        run_gen(command)


def run_gen(cmd):
    result = subprocess.run(cmd, check=True)
    if result.returncode != 0:
        print("error generating samples")
        exit(1)
