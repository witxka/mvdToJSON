#!/bin/sh

# simple test script

# treat all errors as critical
  set -e

cat 2on2.score | ../mvdToJSON.py 2on2|jq
cat 4on4.score | ../mvdToJSON.py 4on4|jq
cat duel.score | ../mvdToJSON.py duel|jq

../mvdToJSON.py || true
../mvdToJSON.py wrong_mode || true
