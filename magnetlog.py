import os
import time, datetime
import xmlrpc.client
import re

max_lines = 10000 # n. of samples after which to create new log file

odir = "log"
ofname = "log"
os.makedirs(odir, exist_ok=True)

def new_log_file():
    # find last log file opened
    logfiles = os.listdir(odir)
    logfiles = sorted([ f for f in logfiles if re.match(f"{ofname}-\d+.csv", f) ])
    if len(logfiles)==0: log_index = 0
    else: # create new log file increasing index by 1
        last_match = re.match(f"{ofname}-(\d+).csv", logfiles[-1])
        last_index = int(last_match.group(1))
        log_index = last_index+1
    log_file = f"{odir}/{ofname}-{log_index:09d}.csv"
    with open(log_file, "w") as log_stream:
        log_stream.write("time;x;y;z\n")
    print(f"Log continues from {log_file}...")
    return log_file

def save_log_file(log_file, fields):
    line = f"{datetime.datetime.now().timestamp()};" + ";".join(fields)
    with open(log_file, "a") as log_stream:
        log_stream.write(line+"\n")

def main():
    log_file = new_log_file()
    with xmlrpc.client.ServerProxy("http://localhost:8000/") as magnetrpc:
        n_lines = 0
        while True:
            if n_lines>max_lines:
                log_file = new_log_file()
                n_lines = 0
            fields = magnetrpc.read_fields()
            save_log_file(log_file, fields)
            n_lines += 1
            time.sleep(.1)

if __name__=='__main__': main()