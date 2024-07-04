from Timer import Timer

ALARM_SOUND_FILE = "./src/assets/alarm.mp3"

def app():
    timer = Timer()
    timer.load_alarm(ALARM_SOUND_FILE)
    timer.run()

if __name__ == '__main__':
    app()