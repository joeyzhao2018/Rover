#!/bin/bash

mpg123 /home/pi/sounds/robot_blip_2.mp3
#exercise_d = {'ccar': 'ccar', 'cigar': ccar}
sudo tts "For which exercise?"
exercise=$(sudo /usr/bin/speech-recog.sh)

#scenario_d = {'baseline': 'baseline', 'medline': 'baseline'}
sudo tts "For which scenario?"
scenario=$(sudo /usr/bin/speech-recog.sh)

#lob_d = {'cards': 'cards', 'cars': 'cards', 'auto': 'auto'}
sudo tts "For which line of business?"
lob=$(sudo /usr/bin/speech-recog.sh)
 

echo "Running $1 forecast for $exercise using $scenario scenario for $lob"
sudo tts "Running $1 forecast for $exercise using $scenario scenario for $lob"
