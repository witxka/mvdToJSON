#!/bin/sh

# simple test script

# treat all errors as critical
  set -e

cat 2on2.score | ../mvdToJSON.py 2on2|jq
cat 4on4.v2.score | ../mvdToJSON.py 4on4|jq
cat 4on4.v1.score | ../mvdToJSON.py 4on4v1|jq
cat duel.score | ../mvdToJSON.py duel|jq
cat duel01.score | ../mvdToJSON.py duel|jq
cat duel02.score | ../mvdToJSON.py duel|jq
# add v1 support with time control
cat duel03.score | ../mvdToJSON.py duel|jq
# add v2 support with movements
cat duel04.score | ../mvdToJSON.py duel|jq

../mvdToJSON.py || true
../mvdToJSON.py wrong_mode || true

cat chat.log | ../mvdCHATToJSON.py | jq
