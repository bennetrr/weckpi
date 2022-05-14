# Project History

## Idea

I don't really know when I got the idea of building my own alarm clock, but I know that I had many other ideas like this before (like building a drone or an RC Car with the RPi) from which none of them was ever completed or even started.

I only know that I started to experiment with Raspberry Pi, an LCD and a small speaker round about in spring of 2020. There were many reasons why I wanted to build my own alarm clock, but here are the three main reasons:

1. The alarm clock I had at this time had a technical defect that caused the time to go forward faster than it should. After a few weeks, my clock was about 10 minutes earlier than the real time.  The alarm clock also didn't have a radio link to set the time automatically, so I had to constantly reset the time manually.
2. The display was very bright and could not be turned off, which bothered me when I was falling asleep.
3. The alarm clock only supports analog radio, which comes with a lower quality and fewer stations.

## WeckPi v1

The current version (at this point of writing) is v1.2.1.

### Hardware

The main part of the hardware of WeckPi v1 is a [Raspberry Pi 3B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/).

As the display, I use a [HD44780 2x16 LCD with an I2C converter](https://www.az-delivery.de/products/lcd-display-16x2-mit-blauem-hintergrund-und-i2c-converter-bundle). Because the GPIO driver can only handle 3V3, but the display operates on 5V, I also needed an [I2C LLC](https://www.amazon.de/ARCELI-Converter-Bidirektionales-Shifter-Arduino/dp/B07RDHR315).

For sound playback, a small portable speaker is used ([X-Mini II](https://www.amazon.com/gp/product/B004SNDC7I)) that we got some time ago as an advertising gift. The battery was replaced with a cable to one of the GPIO pins, so the WeckPi can turn on and off the speaker.

All the parts are connected together with jumper cables on a breadboard, also using a few resistors, LEDs and buttons.

### Software
The software is seperated into two parts: WeckPi Core (or WeckPi Base) and WeckPi Web. You can view the code for both parts in the [`archive/v1` branch](https://github.com/bennetrr/weckpi/tree/archive/v1) on the WeckPi GitHub repository.

WeckPi Core is the main part of the software that handles the important functions like displaying the time on the LCD, watching for the buttons, triggering the alarm, playing the music and so on. It's written in Python 3 and uses `systemd` to run as a background service, which is also integrated in the code. WeckPi Core also comes with the `weckpictl`, a small CLI tool which allows you to control WeckPi Core from the command line. For music playback, `python-vlc` is used.

WeckPi Web is a web interface to configure the WeckPi. In v1, you can only set the alarm times and the music in the web interface, but the original plan was to support many more settings. The frontend is written in react.js (my first React App actually :D), the backend is written in PHP. 

### Problems
The v1 version has many problems, which are not fixed and because of which I'm completely rewriting / rebuilding the WeckPi in v2.

First, the connections on the breadboard are really unstable and often lose the connection.