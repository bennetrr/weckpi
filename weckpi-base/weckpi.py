#! /bin/env python3
import atexit
import logging
import os
import signal
import subprocess
import sys
import threading
import time
import sd_notify
import yaml

from bUtils import day_time, display, gpio, vlcplayer


##################
# Initialisation #
##################

# exit handlers
@atexit.register
def cleanup():
    global exit_threads, devmode
    try:
        logging.info('Stopping...')
        # TODO Exception beim abschalten wegen GPIO
        if not exit_threads:
            devmode = True
            exit_threads = True
            stopmusic()
            wlan_on()
            disp.close()
            gpio.clean()
            time.sleep(5)
    except Exception as exc:
        logging.warning('An exception that occurred on exit was ignored:\n' + str(exc))


def sighandler(signo, frame):
    logging.info('SIGTERM signal (' + str(signo) + ') intercepted')
    cleanup()


signal.signal(signal.SIGTERM, sighandler)

# Systemd
notify = sd_notify.Notifier()
if not notify.enabled():
    logging.critical('Systemd watchdog is not enabled')
    sys.exit(1)

# Logging
VERSION = 'WeckPi v1.2.1'
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.DEBUG)
logging.info(VERSION)

# Settings
CONFIG_FILE = '/etc/weckpi/config.yaml'
SETTINGS_CHANGED_FILE = '/etc/weckpi/settings-changed'
# TODO Config evtl. in Klasse abbilden
config = {}
alarm_stat = False


def parseconfig():
    global config
    logging.debug('Parsing settings')
    config = {}
    try:
        with open(CONFIG_FILE) as f:
            config = yaml.load(f, Loader=yaml.FullLoader)
            f.close()
    except Exception as exc:
        logging.error('Failed to parse settings:\n' + str(exc))
    # logging.debug('Devmode is ' + str(config['debugging']['devmode']))
    check_alarmtimes()


def checkforparse():
    if os.path.exists(SETTINGS_CHANGED_FILE):
        logging.info('Settings reparsing needed')
        parseconfig()
        try:
            os.remove(SETTINGS_CHANGED_FILE)
        except Exception as exc:
            logging.error('Failed to remove settings-changed-indicator-file:\n' + str(exc))


alarmtime = ''
alarmday = ''
override = False
music_type = ""
music_url = ""


def check_alarmtimes():
    global alarmtime, alarmday, override, music_type, music_url
    if config['alarmtimes']['override']['active']:
        if day_time.comparetimes(day_time.timenow(), config['alarmtimes']['override']['time']) >= 2:
            alarmday = day_time.nextday(day_time.daynow())
        else:
            alarmday = day_time.daynow()
        alarmtime = config['alarmtimes']['override']['time']
        override = True
    else:
        day = day_time.daynow()

        if day_time.comparetimes(day_time.timenow(), config['alarmtimes'][day]["time"]) == 3:
            to_late = True
        else:
            to_late = False

        while not config["alarmtimes"][day]["active"] or to_late:
            to_late = False
            day = day_time.nextday(day)
            if day == day_time.daynow():
                alarmtime = ''
                alarmday = ''
                return
        alarmday = day
        alarmtime = config["alarmtimes"][day]["time"]
        music_type = config["alarmtimes"][day]["music"]["type"]
        music_url = config["alarmtimes"][day]["music"]["url"]
        initmusic()


# Display
display_stat = False
last_time = ''
try:
    disp = display.I2CDisplay(16, 2, "A00", "PCF8574", 0x3f, 1)
    # TODO Config benutzen (splashscreen)
    if True:
        disp.write(VERSION)
        disp.newline()
        disp.write('Initializing...')
        time.sleep(5)
except Exception as ex:
    logging.critical('Failed to initialize display:\n' + str(ex))
    sys.exit(2)


def display_on():
    logging.debug('Display on')
    global last_time, display_stat
    last_time = ''
    display_stat = True
    try:
        disp.backlight(True)
    except Exception as exc:
        logging.error('Failed to set backlight state of the display:\n' + str(exc))


def display_off():
    logging.debug('Display off')
    global display_stat
    display_stat = False
    try:
        disp.backlight(False)
        disp.clear()
    except Exception as exc:
        logging.error('Failed to set backlight state and clear the display:\n' + str(exc))


# LEDs and buttons
try:
    wlanled = gpio.LED(22, True)
except Exception as ex:
    logging.error('Failed to initialize leds:\n' + str(ex))

try:
    button_red = gpio.Button(16)
    button_green = gpio.Button(18)
except Exception as ex:
    logging.critical('Failed to initialize buttons:\n' + str(ex))
    sys.exit(1)

# WLAN
wlan_stat = True
devmode = False


def wlan_on():
    logging.debug('WLAN on')
    try:
        wlanled.flash_bg(100, 0.5)
    except Exception as exc:
        logging.error('Failed to turn on the wlan led' + str(exc))

    global wlan_stat
    rfkill = subprocess.run(['rfkill', 'unblock', 'wlan'], capture_output=True)
    try:
        rfkill.check_returncode()
    except subprocess.CalledProcessError:
        logging.error('Failed to enable wlan:\n' + str(rfkill.stderr))

    i = 0
    while subprocess.run(['ping', '-c 1', 'fritz.box'], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT).returncode != 0:
        i += 1
        time.sleep(0.5)

    wlan_stat = True

    try:
        wlanled.stop_flash_bg()
        wlanled.setledstate(True)
    except Exception as exc:
        logging.error('Failed to turn on the wlan led' + str(exc))


def wlan_off():
    if False or devmode:
        logging.warning('Disabling wlan is not allowed in devmode')
    else:
        logging.debug('WLAN off')
        global wlan_stat
        rfkill = subprocess.run(['rfkill', 'block', 'wlan'], capture_output=True)
        try:
            rfkill.check_returncode()
        except subprocess.CalledProcessError:
            logging.error('Failed to disable wlan:\n' + str(rfkill.stderr))
        wlan_stat = False
        try:
            wlanled.setledstate(False)
        except Exception as exc:
            logging.error('Failed to turn off the wlan led' + str(exc))


# Sound
try:
    speaker = gpio.Output(11)
    speaker.setstate(False)
except Exception as ex:
    logging.critical('Failed to initialize speaker power control:\n' + str(ex))
    sys.exit(1)

music = None
radio_stat = False


def initmusic():
    global music
    stopmusic()
    try:
        if music_type == 'playlist-random':
            music = vlcplayer.RandomPlaylist(music_url)
        elif music_type == 'playlist':
            music = vlcplayer.Playlist(music_url)
        elif music_type == 'internetradio':
            music = vlcplayer.InternetRadio(music_url)
        else:
            raise Exception('Unknown media type ' + str(music_type))
    except Exception as exc:
        logging.critical('Failed to initialize vlc:\n' + str(exc))
        sys.exit(1)


def playmusic():
    logging.debug('Music on')
    global radio_stat
    if not radio_stat:
        wlan_on()
        time.sleep(15)
        try:
            speaker.setstate(True)
        except Exception as exc:
            logging.error('Failed to turn on the speakers power:\n' + str(exc))
        try:
            music.play()
        except Exception as exc:
            logging.error('Failed to play music:\n' + str(exc))
        radio_stat = True
        # TODO Config benutzen
        stoptimer = threading.Timer(3600, stopmusic)
        stoptimer.start()


def stopmusic():
    logging.debug('Music off')
    global radio_stat, alarm_stat
    try:
        music.stop()
    except Exception as exc:
        logging.error('Failed to stop music:\n' + str(exc))
    wlan_off()
    try:
        speaker.setstate(False)
    except Exception as exc:
        logging.error('Failed to turn on the speakers power:\n' + str(exc))
    if alarm_stat:
        alarm_stat = False
        if override:
            parseconfig()
            config['alarmtimes']['override']['active'] = False
            with open(CONFIG_FILE, 'w') as file:
                yaml.dump(config, file)
                file.close()
        check_alarmtimes()
    radio_stat = False


def nextsong():
    logging.debug('Next music track')
    try:
        music.next()
    except Exception as exc:
        logging.error('Failed to play next track:\n' + str(exc))


parseconfig()


# Threads
def t_disp():
    global last_time
    while True:
        if exit_threads:
            return
        if display_stat:
            time_now = day_time.timenow()
            try:
                if last_time != time_now:
                    disp.clear()
                    disp.write('Zeit: ' + time_now)
                    disp.newline()
                    if alarm_stat:
                        disp.write('Wecker klingelt!')
                    else:
                        disp.write('     ' + alarmtime + ' (' + alarmday + ')')
                    last_time = time_now
            except Exception as exc:
                logging.error('Failed to write to display:\n' + str(exc))


def t_alarm():
    global alarm_stat
    while True:
        if exit_threads:
            return
        if day_time.timenow() == alarmtime and alarmday == day_time.daynow() and not alarm_stat:
            alarm_stat = True
            try:
                music.set_volume(20)
            except Exception as exc:
                logging.error('Failed to set volume of the music:\n' + str(exc))
            playmusic()
            # TODO Config benutzen
            # if settings('misc', 'autoDisplayOn'):
            #     display_on()
            try:
                time.sleep(2)
                music.set_volume(40)
                time.sleep(2)
                music.set_volume(60)
                time.sleep(2)
                music.set_volume(80)
                time.sleep(2)
                music.set_volume(100)
            except Exception as exc:
                logging.error('Failed to set volume of the music:\n' + str(exc))


wlan_off()

# Start threads
threads = []
exit_threads = False
try:
    thread_disp = threading.Thread(target=t_disp)
    threads.append(thread_disp)
    thread_alarm = threading.Thread(target=t_alarm)
    threads.append(thread_alarm)

    for thread in threads:
        thread.start()

except Exception as ex:
    logging.critical('Failed to start threads:\n' + str(ex))
    sys.exit(1)

logging.info('Started threads')

display_off()
notify.ready()
logging.info('Initialisation finished')

while True:
    if exit_threads:
        break
    checkforparse()

    if button_red.getstate():
        time.sleep(0.5)
        if button_red.getstate():
            time.sleep(2)
            if button_red.getstate():
                logging.info('Application restart called by user')
                subprocess.run(['weckpictl', 'restart'])
                continue
        try:
            display_on()
            # TODO Config benutzen
            time.sleep(10)
            display_off()
            time.sleep(2)
        except Exception as ex:
            logging.error('Failed to toggle display:\n' + str(ex))

    if button_green.getstate():
        time.sleep(0.5)
        if button_green.getstate():
            time.sleep(2)
            if button_green.getstate():
                if radio_stat:
                    nextsong()
                else:
                    if wlan_stat:
                        wlan_off()
                    else:
                        wlan_on()
                time.sleep(2)
                continue
        if radio_stat:
            stopmusic()
        else:
            playmusic()
        time.sleep(2)
