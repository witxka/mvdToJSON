#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description  : Read mvdparsers output for CHAT and build final CHAT info in JSON
# Author       : [cmd] witka <witxka@gmail.com>

import sys
import traceback
import logging
import json

def main():
  """Main function. Read mvdparsers output for CHAT from stdin and build chat info in JSON.

  @return The output in JSON format.
  """
  try:
    chatInfo = []
    matchChatInfo = {}
    for info in sys.stdin:
      chatInfo.append(info.strip())
    matchChatInfo["chat"] = chatInfo
    print(json.dumps (matchChatInfo))
  except Exception as e:
    logging.error(traceback.format_exc())

if __name__ == "__main__":
  main()
