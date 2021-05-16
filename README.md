Taken from:

`https://learn.adafruit.com/adafruit-rgb-matrix-plus-real-time-clock-hat-for-raspberry-pi?view=all`

Install the libraries:

```curl https://raw.githubusercontent.com/adafruit/Raspberry-Pi-Installer-Scripts/master/rgb-matrix.sh >rgb-matrix.sh
sudo bash rgb-matrix.sh```

Copy the files in this repo to /rpi-rgb-led-matrix/bindings/python/samples

Rename `config.ini.example` to `config.ini` and fill in the values in the new `config.ini`.

You'll need an API client ID and API Secret key from Twitch and this program will automatically get you a bearer token.
Get these by making an app here:

`https://dev.twitch.tv/console/apps`

I have a 16 row display so run this program from `/rpi-rgb-led-matrix/bindings/python/samples` by running:

`sudo python ./livestatus.py --led-rows=16`
