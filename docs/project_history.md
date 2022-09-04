# Project History

## Idea

I don't really know when I got the idea of building my own alarm clock,
but I know that I had many other ideas like this before (like building a drone or an RC Car with the Raspberry Pi)
from which none of them was ever completed or even started.

I only know that I started to experiment with the Raspberry Pi,
an LCD and a small speaker round about in spring of 2020.
There were many reasons why I wanted to build my own alarm clock, but here are the three main reasons:

1. The alarm clock I had at this time had a technical defect that caused the time to go forward faster than it should.
   After a few weeks, my clock was about 10 minutes earlier than the real time.
   The alarm clock also didn't have a radio link to set the time automatically,
   so I had to constantly reset the time manually.
2. The display was very bright and could not be turned off, which bothered me when I was falling asleep.
3. The alarm clock only supports analog radio, which comes with a lower quality and fewer stations.

## WeckPi v1

The current version is v1.2.1.

### Hardware

<img alt="A picture of the WeckPi v1 from the top" height="30%" src="https://raw.githubusercontent.com/bennetrr/weckpi/main/docs/assets/weckpi-v1/P1000895.jpg" title="WeckPi v1 top view" width="30%"/>
<img alt="A picture of the WeckPi v1 from the front" height="30%" src="https://raw.githubusercontent.com/bennetrr/weckpi/main/docs/assets/weckpi-v1/P1000916.jpg" title="WeckPi v1 front view" width="30%"/>
<img alt="The circuit plan of the WeckPi v1" height="30%" src="https://raw.githubusercontent.com/bennetrr/weckpi/main/docs/assets/weckpi-v1/WeckPi_Steckplatine.png" title="WeckPi v1 circuit plan" width="30%"/>

The main part of the hardware of WeckPi v1 is a [Raspberry Pi 3B+](https://www.raspberrypi.com/products/raspberry-pi-3-model-b-plus/).

As the display,
I used a [HD44780 2x16 LCD with an I2C converter](https://www.az-delivery.de/products/lcd-display-16x2-mit-blauem-hintergrund-und-i2c-converter-bundle).
Because the GPIO driver can only handle 3V3,
but the display operates on 5V,
I also needed an [I2C LLC](https://www.amazon.de/ARCELI-Converter-Bidirektionales-Shifter-Arduino/dp/B07RDHR315).

For sound playback,
a small portable speaker is used ([X-Mini II](https://www.amazon.com/gp/product/B004SNDC7I))
that we got some time ago as an advertising gift.
The battery was replaced with a cable to one of the GPIO pins, so WeckPi Core can turn on and off the speaker.

All the parts are connected together with jumper cables on a breadboard, also using a few resistors, LEDs and buttons.

### Software

The software is seperated into two parts: WeckPi Core (formerly WeckPi Base) and WeckPi Web.
You can view the code for both parts in the [`archive/v1` branch](https://github.com/bennetrr/weckpi/tree/archive/v1) on the WeckPi GitHub repository.

WeckPi Core is the main part of the software that handles the important functions like displaying the time on the LCD,
watching for the buttons, triggering the alarm, playing the music and so on.
It's written in Python and uses `systemd` to run as a background service, which is also integrated in the code.
WeckPi Core also comes with the `weckpictl`,
a small CLI tool which allows you to control WeckPi Core from the command line.
For music playback, [`python-vlc`](https://pypi.org/project/python-vlc/) is used.

WeckPi Web is a web interface to configure the WeckPi.
In v1, you can only set the alarm times and the music in the web interface,
but the original plan was to support many more settings.
The frontend is written in React.js (my first React App actually :D), the backend is written in PHP.

### Problems

The v1 version has many problems, because of which I'm completely rewriting / rebuilding the WeckPi in v2.

The connections on the breadboard are partly very unstable.
Also, some parts are quite old (like the buttons from a 20-year-old PC).
This leads to the buttons sometimes activating themselves.
Furthermore, the display's power supply sometimes just aborts,
which makes the display "forget" all its configurations.
In the most cases, the display is no longer able to communicate with WeckPi Core,
which leads to weird symbols on the LCD.

When the display is broken,
WeckPi Core can be restarted in most cases using the buttons to reinitialize the display and solve the problem.
But sometimes, WeckPi Core also crashes alongside the display.
This also happens on purpose when WeckPi Core could not establish the connection with the display.
The problem is that the restart buttons are handled by WeckPi Core itself.<br>
No WeckPi Core running means the restart button does not work.
In this case, I have to connect with SSH to the Raspberry Pi and start WeckPi Core manually.

Another problem is that the Raspberry Pi has no case or anything,
so it just sits there on my nightstand and collects dust.
