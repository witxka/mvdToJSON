#!/bin/bash

# treat all errors as critical
  set -e

###
# Parse mvdparser output and generate score  description file for 
# match info. Require mvdpareser and jq
#
# @param argv[1] The file name for demo to parse
###

if [[ $# -ne 1 ]] ; then
  echo "Usage: $0 path type"
  echo "  Where path is the full path for demo file"
  exit 1
fi

fileName=$1

./mvdparser.amd64.glibc6.2.31 -f ./fragfile.dat -t ./json.dat  -v $fileName | \
  sed -n '/The match is over/,/Disconnected/p' |\
  sed -e 's/svc_print: (CRITICAL)//g' -e 's/_//g' -e '/svcprint/ d' -e '/: Disconnected/ d' |\
  sed -e '/^ $/ d' |\
  tail -n +4 |\
  iconv -tUTF-8 >$fileName.score
