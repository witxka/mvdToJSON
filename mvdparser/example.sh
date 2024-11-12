#!/bin/sh

# example command to create json file for a demo based on mvdparser
# require mvdparser and jq

mvdparser -f fragfile.dat -t json.dat  -v demos/4on4.mvd | \
  tee >(grep CHAT |\
  sed -e '/svc_print: (CHAT) (/ d' -e 's/svc_print: (CHAT) //g' -e 's/_//g' |\
  uniq |\
  ../mvdCHATToJSON.py >demos/4on4.mvd.chat.json) |\
  sed -n '/The match is over/,/Disconnected/p' |\
  sed -e 's/svc_print: (CRITICAL)//g' -e 's/_//g' -e '/svcprint/ d' -e '/: Disconnected/ d' |\
  sed -e '/^ $/ d' |\
  tail -n +4 |\
  ../mvdToJSON.py 4on4 >demos/4on4.mvd.score.json  && jq '. += input'  demos/4on4.mvd.json demos/4on4.mvd.score.json |\
  jq ' . += input' - demos/4on4.mvd.chat.json > demos/4on4.mvd.desc.json
