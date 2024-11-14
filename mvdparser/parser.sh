#!/bin/bash

# treat all errors as critical
  set -e

###
# Parse mvdparser output and generate join JSON description file for 
# server, players, match and chat info. Require mvdpareser and jq
#
# @param argv[1] The file name for demo to parse
# @param argv[2] The type of demo {duel, 2on2, 4on4}
###

if [[ $# -ne 2 ]] ; then
  echo "Usage: $0 path type"
  echo "  Where path is the full path for demo file"
  echo "  type the type of demo to parse {duel, 2on2, 4on4}"
  exit 1
fi

fileName=$1
demoType=$2

./mvdparser.amd64.glibc6.2.31 -f ./fragfile.dat -t ./json.dat  -v $fileName | \
  tee >(grep CHAT |\
  sed -e '/svc_print: (CHAT) (/ d' -e 's/svc_print: (CHAT) //g' -e 's/_//g' |\
  uniq |\
  ../mvdCHATToJSON.py >$fileName.chat.json) |\
  sed -n '/The match is over/,/Disconnected/p' |\
  sed -e 's/svc_print: (CRITICAL)//g' -e 's/_//g' -e '/svcprint/ d' -e '/: Disconnected/ d' |\
  sed -e '/^ $/ d' |\
  tail -n +4 |\
  ../mvdToJSON.py $demoType >$fileName.score.json  && jq '. += input' $fileName.json $fileName.score.json |\
  jq ' . += input' - $fileName.chat.json > $fileName.desc.json
