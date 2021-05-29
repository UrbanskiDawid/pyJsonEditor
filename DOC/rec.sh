#!/bin/sh
#https://github.com/asciinema/asciinema
#
#https://github.com/asciinema/asciicast2gif
#rm -rf rec.cast rec.gif
#asciinema rec rec.cast
sudo docker run --rm -v $PWD:/data asciinema/asciicast2gif -s 1.5 rec.cast rec.gif
sudo chown dave:dave rec.gif
ls -1 rec.gif
