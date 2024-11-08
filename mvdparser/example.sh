#!/bin/sh

# example command to create json file for a demo based on mvdparser
# require mvdparser and jq

mvdparser -f fragfile.dat -t json.dat  -v demos/4on4.mvd |\
  sed -n '/The match is over/,/Disconnected/p' | \
  sed -e 's/svc_print: (CRITICAL)//g' -e 's/_//g' -e '/svcprint/ d' -e '/: Disconnected/ d'|\
  sed -e '/^ $/ d' | \
  tail -n +4 | \
  ../mvdToJSON.py > demos/4on4.mvd.score.json && jq '.match_info += [input]'  demos/4on4.mvd.json demos/4on4.mvd.score.json > demos/4on4.mvd.desc.json
