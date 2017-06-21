#!/bin/bash 

echo -en "To: $5@gmail.com\nFrom: My Companion\nSubject: $4 $2 $3 forecast run $1\n\nYou forecast run reference ID is $1" | sendmail bandev3@gmail.com
