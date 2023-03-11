import sys
import schedule
import subprocess


def function_subprocess():
    process = subprocess.Popen([sys.executable, "pars_and_write.py"], shell=True)
    process.communicate()


def function_write_data():
    schedule.every(1).to(60).minutes.do(function_subprocess)
    while True:
        schedule.run_pending()



