#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics
import time
import datetime
from twitch import Twitch
import configparser
import os


class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)

    def run(self):
        font_dir = "{}/../../../fonts/".format(os.path.dirname(os.path.realpath(__file__)))
        config_filename = 'config.ini'
        config = configparser.ConfigParser()
        config.read(config_filename)
        check_interval = config.getint('settings', 'check-interval')
        brightness = config.getint('settings', 'brightness')

        client_id = config['twitch']['client-id']
        client_bearer = config.get('twitch', 'bearer', fallback=None)
        client_secret = config.get('twitch', 'secret', fallback=None)

        if client_bearer is None and client_secret is None:
            raise Exception("If no bearer token is provided, an API secret key is needed to retrieve a bearer token.")

        streamer = config.get('twitch', 'streamer')

        twitch = Twitch(client_id, bearer=client_bearer)

        if client_bearer is None:
            # get a new bearer token and save it to file. The twitch class automatically stores this locally
            client_bearer = twitch.get_bearer(client_secret)
            config.set('twitch', 'bearer', client_bearer)
            with open(config_filename, 'w') as configfile:
                config.write(configfile)

        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("{}4x6.bdf".format(font_dir))
        font_large = graphics.Font()
        font_large.LoadFont("{}7x13.bdf".format(font_dir))
        textColor = graphics.Color(255, 255, 0)
        pos = offscreen_canvas.width
        feed_check_time = 0

        while True:
            if time.time() - feed_check_time >= check_interval:
                stream_info = twitch.get_stream_info(streamer)
                feed_check_time = time.time()

            is_online = stream_info['is_live']
            offscreen_canvas.Clear()
            if is_online:
                offscreen_canvas.brightness = brightness
                textColor = graphics.Color(0, 255, 0)
                game_name = stream_info['game_name']
                stream_start = stream_info['started_at']

                stream_duration = datetime.datetime.utcnow() - datetime.datetime.strptime(stream_start, "%Y-%m-%dT%H:%M:%SZ")

                if game_name == "Just Chatting":
                    game_name = "Just Stalling"
                len = graphics.DrawText(offscreen_canvas, font_large, pos, 14, textColor, game_name)
                pos = pos - 1
                if pos + len <= 0:
                    pos = offscreen_canvas.width
                #graphics.DrawText(offscreen_canvas, font, 0, 6, textColor, "LIVE")
                graphics.DrawText(offscreen_canvas, font, 3, 5, graphics.Color(127, 127, 255), str(stream_duration))
                offsecreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                time.sleep(0.05)
            else:
                offscreen_canvas.brightness = 50
                textColor = graphics.Color(255, 0, 0)

                graphics.DrawText(offscreen_canvas, font, 0, 6, textColor, "OFFLINE")

                offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
                time.sleep(60)


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
