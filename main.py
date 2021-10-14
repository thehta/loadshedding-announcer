from playsound import playsound
import json
import datetime
import time
import requests

CURR_STAGE = 0
CURRENT_ID = 8

def play_announcement(stage, time):
    playsound('TTS/chime.mp3')
    playsound('TTS/Imminent.wav')
    playsound('TTS/STAGE/'+str(stage) + '.wav')
    playsound('TTS/Time.wav')
    playsound('TTS/TIME/'+str(time) + '.wav')

def getWaitTime(current_time):
    schedule_today = schedule[int(current_time.strftime("%d"))-1]
    curr_hour = int(current_time.strftime("%H"))
    hour_int = 0
    for slot in schedule_today:
        keys = list(slot)
        hour_int = int(keys[0][0:2])
        if (curr_hour < hour_int):
            break
    return current_time.replace(hour=hour_int, minute=0,second=0) - current_time

def getStatus():
    stage_request = requests.get('https://loadshedding.eskom.co.za/LoadShedding/GetStatus')
    print(stage_request.status_code, stage_request.text)
    return stage_request.status_code, int(stage_request.text)

schedule_file = open('id_' + str(CURRENT_ID) + '.json',)
schedule_data = json.load(schedule_file)
schedule_file.close()
schedule = schedule_data['schedule']

while (True):
    wait_time = getWaitTime(datetime.datetime.now()).total_seconds()
    wait_time = 1
    print("waiting for {} seconds".format(wait_time))
    time.sleep(wait_time)
    response_code = 0
    while (response_code != 200):
        response_code = getStatus()[0]
        curr_stage = getStatus()[1]

    print(response_code, curr_stage)

    if (curr_stage != 0 and curr_stage != 1):
        play_announcement(curr_stage-1, bootstrapped_hour)
