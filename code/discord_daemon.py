import requests
import os
import time
import subprocess
import argparse
import select
import re


webhook = "https://discord.com/api/webhooks/1194324788932517938/TzRqn74MayBeMN_Zs893tejRNKE2Q4UH6FdzJpfqlfnox-wkztAXMRA3gfQ8WlJgdeoS"
filename = "./code/discord.log"

def sneezyIsRunning():
    plist = [x.rstrip('\n') for x in os.popen("ps -a | grep 'sneezy'")]
    for process in plist:
        if re.search("^\W+\d+\W+\S+\W+\d\d:\d\d:\d\d\W+(sneezy)$",process): 
            #print("sneezy is running...")
            return True
    return False

def sendMessage(msg):
    data = {
        "content" : msg,
        "username" : "Sneezy"
    }
    msg_sent = False
    while not msg_sent:
        try:
            result = requests.post(webhook, json = data)

            try:
                result.raise_for_status()
            except requests.exceptions.HTTPError as err:
                print(err)
            else:
                print(f"Payload delivered successfully, code {result.status_code}.")
        except: 
            print("Exception posting request, backing off a moment...")
            time.sleep(10)
        else:
            msg_sent = True
        


def discordDaemon():
    # f = subprocess.Popen(['tail','-F',filename], stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    # p = select.poll()
    # p.register(f.stdout)
    last_msg_number = 0
    msg_number = 0
    logfile = open(filename,"r")
    loglines = follow(logfile)

    for line in loglines:
        print(line)
        msg = line.rstrip('\n').split(',',2)
        sendMessage(msg[1])

                
        time.sleep(0.1)

    
    sendMessage("Sneezy is no longer running.  Shutting down.")

def follow(file):
    while sneezyIsRunning():
        line = file.readline()
        if not line or not line.endswith('\n'):
            time.sleep(0.1)
            continue
        yield line

if __name__ == "__main__":
    # a = sys.argv[1]
    # b = sys.argv[2]
    discordDaemon()