#!/bin/bash 

sendemail -f pi@mycompanion -t $4 -u "Requesting approval for $1" -m "Please review attached $1 data and approve. Your forecast run reference ID is $2" -a $3 -S /usr/sbin/sendmail

#echo -en "To: $3\nFrom: My Companion\nSubject: Requesting approval for $1\n\nPlease review attached $1 data and approve. Your forecast run reference ID is $2" | sendmail $3
