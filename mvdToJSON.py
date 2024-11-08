#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Description  : Read mvdparsers output and build final match info in JSON
# Author       : [cmd] witka <witxka@gmail.com>

import sys
import traceback
import logging
import json

def paresScores(scores):
  """Parse scores like 23 (-6) 44.2% 

  @param scores The score string to parse.
  @return The dictionary about scores 
  """
  parsedScores = {}
  info = scores.split()
  parsedScores["frags"] = int(info[0])
  parsedScores["rank"] = int(info[1][1:-1])
  parsedScores["efficiency"] = float(info[2][:-1])
  return parsedScores

def paresTeamScores(scores):
  """Parse team scores like  36 (-16) 3 40.9%

  @param scores The tema score string to parse.
  @return The dictionary about scores 
  """
  parsedScores = {}
  info = scores.split()
  parsedScores["frags"] = int(info[0])
  parsedScores["rank"] = int(info[1][1:-1])
  parsedScores["teamkills"] = int(info[2])
  parsedScores["efficiency"] = float(info[3][:-1])
  return parsedScores

def parseWeaponEfficiency(weaponEfficiency):
  """Parse weapon efficiency like 
     Wp: lg24.7% rl44.8 6.95277e-310l14.3 g32.4 sg37.9%

  @param weaponEfficiency The weapon efficiency string to parse.
  @return The dictionary about weapon efficiency 
  """
  parsedWeaponEfficiency = {}
  weapons = {"lg":'%',"rl":'',"sg":'%',"g":'%'}   
  info = weaponEfficiency.replace("Wp:","").split()
  for stat in info:
    for wp in weapons:
      try:
        if stat.index(wp) == 0 :
          parsedWeaponEfficiency[wp] = float(stat.replace(wp,"").replace(weapons[wp],""))

      except ValueError :
        continue  
  return parsedWeaponEfficiency

def parseSkillRL(skillRL):
  """Parse RL skill like 
     RL skill: ad:74.1 dh:12
  @param skillRL The skill of RL.
  @return The dictionary about RL skill. 
  """

  parsedSkillRL = {}
  info = skillRL.replace("RL skill: ","").split()
  parsedSkillRL["ad"] = float(info[0].split(':')[1])
  parsedSkillRL["dh"] = int(info[1].split(':')[1])
  return parsedSkillRL

def parseSpeed(speed):
  """Parse speed like 
    Speed: max:876.9 average:346.5
  @param speed The speed to parse.
  @return The dictionary about speed. 
  """

  parsedSpeed = {}
  info = speed.replace("Speed:","").split()
  parsedSpeed["max"] = float(info[0].split(':')[1])
  parsedSpeed["average"] = float(info[1].split(':')[1])
  return parsedSpeed

def parseArmorsAndMegas(armorsAndMegas):
  """Parse armors and megas info like 
     Armr&mhs: ga:14 ya:7 ra:16 mh:7
  @param armorsAndMegas The stat about taken armors and megas.
  @return The dictionary about armors and megas statistics. 
  """

  parsedArmorsAndMegas = {}
  info = armorsAndMegas.replace("Armr&mhs: ","").split()
  parsedArmorsAndMegas["ga"] = int(info[0].split(':')[1])
  parsedArmorsAndMegas["ya"] = int(info[1].split(':')[1])
  parsedArmorsAndMegas["ra"] = int(info[2].split(':')[1])
  parsedArmorsAndMegas["mh"] = int(info[3].split(':')[1])
  return parsedArmorsAndMegas

def parseDamage(damage):
  """Parse damage info like 
     Damage: Tkn:7263 Gvn:6633 Tm:0
  @param damage The damage info to parse.
  @return The dictionary about damage. 
  """

  parsedDamage = {}
  info = damage.replace("Damage: ","").split()
  parsedDamage["tkn"] = int(info[0].split(':')[1])
  parsedDamage["gvn"] = int(info[1].split(':')[1])
  parsedDamage["tm"] = int(info[2].split(':')[1])
  return parsedDamage

def parseEndGame(endGame):
  """Parse stat at the end of the game like 
    EndGame: H:67 A:0
  @param endGame The end game info to parse.
  @return The dictionary about end game stat. 
  """

  parsedEndGame = {}
  info = endGame.replace("EndGame: ","").split()
  parsedEndGame["H"] = int(info[0].split(':')[1])
  parsedEndGame["A"] = int(info[1].split(':')[1])
  return parsedEndGame

def parseSpawnfrags(spawnfrags):
  """Parse stat about spawn frags like 
    SpawnFrags: 3
  @param spawfrags The spawnfrags  info to parse.
  @return The number of spawn frags. 
  """
 
  info = spawnfrags.replace("SpawnFrags: ","")
  return int(info)

def parsePowerups(powerups):
  """Parse powerups info like 
     Powerups: Q:6 P:1 R:1
  @param powerups The powerups info to parse.
  @return The dictionary about powerups. 
  """

  parsedPowerups = {}
  info = powerups.replace("Powerups: ","").split()
  parsedPowerups["Q"] = int(info[0].split(':')[1])
  parsedPowerups["P"] = int(info[1].split(':')[1])
  parsedPowerups["R"] = int(info[2].split(':')[1])
  return parsedPowerups

def parseStreaks(streaks):
  """Parse streaks info like 
     Streaks: Frags:13 QuadRun:4
  @param streaks The streaks info to parse.
  @return The dictionary about streaks. 
  """

  parsedStreaks = {}
  info = streaks.replace("Streaks: ","").split()
  parsedStreaks["frags"] = int(info[0].split(':')[1])
  parsedStreaks["quadrun"] = int(info[1].split(':')[1])
  return parsedStreaks

def parseStatRL(statRL):
  """Parse stat about RL like 
     RL: Took:6 Killed:6 Dropped:2
  @param statRL The statistics about RL to parse.
  @return The dictionary about RL statistics. 
  """

  parsedStatRL = {}
  info = statRL.replace("RL: ","").split()
  parsedStatRL["took"] = int(info[0].split(':')[1])
  parsedStatRL["killed"] = int(info[1].split(':')[1])
  parsedStatRL["dropped"] = int(info[2].split(':')[1])
  return parsedStatRL

def mvdParseDuel():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for duel mode.

  @return The dictionary of the match info.
  """
  matchInfo = {}

  playersNumber = 0
  playerStat = {}
  allPlayersStat = []
  while playersNumber < 2:
    playerStat["name"] = sys.stdin.readline().strip()[:-1]
    playerStat["scores"] = paresScores(sys.stdin.readline().strip())
    playerStat["weapons_efficiency"] = parseWeaponEfficiency(sys.stdin.readline().strip())
    playerStat["skill_RL"] = parseSkillRL(sys.stdin.readline().strip())
    playerStat["speed"] = parseSpeed(sys.stdin.readline().strip())
    playerStat["armors_and_megas"] = parseArmorsAndMegas(sys.stdin.readline().strip())
    playerStat["damage"] = parseDamage(sys.stdin.readline().strip())
    playerStat["end_game"] = parseEndGame(sys.stdin.readline().strip())
    playerStat["spawnfrags"] = parseSpawnfrags(sys.stdin.readline().strip())
    allPlayersStat.append(playerStat)
    playerStat = {}
    playersNumber += 1
  matchInfo["players"] = allPlayersStat
  return matchInfo

def mvdParse4on4():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 4on4 mode.

  @return The dictionary of the match info.
  """
  matchInfo = {}
  matchInfo["players_stat"] = parse4on4PlayersStatistics()
  matchInfo["match_stat"] = parse4on4MatchStatistics()
  return matchInfo

def parse4on4PlayersStatistics():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 4on4 mode with team statistics.

  @return The dictionary of the match info team statistics.
  """
  matchInfo = {}
  teamsNumber = 0
  allTeamsStat = []
  while teamsNumber < 2:
    allPlayersStat = []
    teamStat = {}
    playersNumber = 0
    teamStat["name"] = sys.stdin.readline().strip().replace("Team ","")[:-1]
    while playersNumber < 4:
      playerStat = {}
      playerStat["name"] = sys.stdin.readline().strip()[:-1]
      playerStat["scores"] = paresTeamScores(sys.stdin.readline().strip())
      playerStat["weapons_efficiency"] = parseWeaponEfficiency(sys.stdin.readline().strip())
      playerStat["skill_RL"] = parseSkillRL(sys.stdin.readline().strip())
      playerStat["armors_and_megas"] = parseArmorsAndMegas(sys.stdin.readline().strip())
      playerStat["powerups"] = parsePowerups(sys.stdin.readline().strip())
      playerStat["stat_RL"] = parseStatRL(sys.stdin.readline().strip()) 
      playerStat["damage"] = parseDamage(sys.stdin.readline().strip())
      playerStat["streaks"] = parseStreaks(sys.stdin.readline().strip())
      playerStat["spawnfrags"] = parseSpawnfrags(sys.stdin.readline().strip())
      allPlayersStat.append(playerStat)
      playersNumber += 1
    teamStat["players"] = allPlayersStat
    allTeamsStat.append(teamStat)
    teamsNumber += 1
  matchInfo["teams"] = allTeamsStat  
  return matchInfo


def parse4on4MatchStatistics():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 4on4 match statistics.

  @return The dictionary of the match info.
  """
  matchInfo = {}

  matchInfo["teams"] = parse4on4TeamStatistics()
  matchInfo["top_scores"] = parse4on4TopScores()
  matchInfo["team_scores"] = parse4on4TeamScores()

  return matchInfo

def parse4on4TeamStatistics():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 4on4 team statistics.

  @return The dictionary of the match info.
  """
  matchInfo = {}
  # skip the head
  sys.stdin.readline()
  sys.stdin.readline()

  teamsNumber = 0
  teamStat = {}
  allTeamsStat = []
  while teamsNumber < 2:
    teamStat = {}
    info = sys.stdin.readline().strip() 
    teamStat["name"] = info.split(":")[0]
    teamStat["weapons_efficiency"] = parseWeaponEfficiency(info.replace(teamStat["name"]+":",""))
    teamStat["powerups"] = parsePowerups(sys.stdin.readline().strip())
    teamStat["armors_and_megas"] = parseArmorsAndMegas(sys.stdin.readline().strip())
    teamStat["stat_RL"] = parseStatRL(sys.stdin.readline().strip()) 
    teamStat["damage"] = parseDamage(sys.stdin.readline().strip())

    allTeamsStat.append(teamStat)
    teamsNumber += 1
  return allTeamsStat

def parse4on4TopScores():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 4on4 match statistics top scores.

  @return The dictionary of the match info.
  """
  matchInfo = {}
  keys = {"frags":"", "deaths":"", "friendkills":"", "efficiency":"%", "fragstreak":"",
        "quadrun":""}
  # skip the head
  sys.stdin.readline()
  for field in keys:
    info = sys.stdin.readline().strip().replace(keys[field],"")
    union = {}
    union["name"] = info.split()[1]
    union["count"] = float(info.split()[2])  
    matchInfo[field] = union
  return matchInfo

def parse4on4TeamScores():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 4on4 match statistics team scores.

  @return The dictionary of the match info.
  """
  matchInfo = []
  # skip the head
  sys.stdin.readline().strip()
  for i in range(2):
    info = sys.stdin.readline().strip()
    union = {}
    union["name"] = info.split()[0][:-1]
    union["frags"] = int(info.split()[1]) 
    union["percentage"] = float(info.split()[2].replace("%","")) 
    matchInfo.append(union)
  
  return matchInfo

def mvdParse2on2():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 2on2 mode.

  @return The dictionary of the match info.
  """
  matchInfo = {}
  matchInfo["players_stat"] = parse2on2PlayersStatistics()
  matchInfo["match_stat"] = parse2on2MatchStatistics()
  return matchInfo

def parse2on2PlayersStatistics():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 2on2 mode with team statistics.

  @return The dictionary of the match info team statistics.
  """
  matchInfo = {}
  teamsNumber = 0
  allTeamsStat = []
  while teamsNumber < 2:
    allPlayersStat = []
    teamStat = {}
    playersNumber = 0
    teamStat["name"] = sys.stdin.readline().strip().replace("Team ","")[:-1]
    while playersNumber < 2:
      playerStat = {}
      playerStat["name"] = sys.stdin.readline().strip()[:-1]
      playerStat["scores"] = paresTeamScores(sys.stdin.readline().strip())
      playerStat["weapons_efficiency"] = parseWeaponEfficiency(sys.stdin.readline().strip())
      playerStat["skill_RL"] = parseSkillRL(sys.stdin.readline().strip())
      playerStat["armors_and_megas"] = parseArmorsAndMegas(sys.stdin.readline().strip())
      playerStat["powerups"] = parsePowerups(sys.stdin.readline().strip())
      playerStat["stat_RL"] = parseStatRL(sys.stdin.readline().strip()) 
      playerStat["damage"] = parseDamage(sys.stdin.readline().strip())
      playerStat["streaks"] = parseStreaks(sys.stdin.readline().strip())
      playerStat["spawnfrags"] = parseSpawnfrags(sys.stdin.readline().strip())
      allPlayersStat.append(playerStat)
      playersNumber += 1
    teamStat["players"] = allPlayersStat
    allTeamsStat.append(teamStat)
    teamsNumber += 1
  matchInfo["teams"] = allTeamsStat  
  return matchInfo

def parse2on2MatchStatistics():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 2on2 match statistics.

  @return The dictionary of the match info.
  """
  matchInfo = {}

  matchInfo["teams"] = parse2on2TeamStatistics()
  matchInfo["top_scores"] = parse2on2TopScores()
  matchInfo["team_scores"] = parse2on2TeamScores()

  return matchInfo

def parse2on2TeamStatistics():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 2on2 team statistics.

  @return The dictionary of the match info.
  """
  matchInfo = {}
  # skip the head
  sys.stdin.readline()
  sys.stdin.readline()

  teamsNumber = 0
  teamStat = {}
  allTeamsStat = []
  while teamsNumber < 2:
    teamStat = {}
    info = sys.stdin.readline().strip() 
    teamStat["name"] = info.split(":")[0]
    teamStat["weapons_efficiency"] = parseWeaponEfficiency(info.replace(teamStat["name"]+":",""))
    teamStat["powerups"] = parsePowerups(sys.stdin.readline().strip())
    teamStat["armors_and_megas"] = parseArmorsAndMegas(sys.stdin.readline().strip())
    teamStat["stat_RL"] = parseStatRL(sys.stdin.readline().strip()) 
    teamStat["damage"] = parseDamage(sys.stdin.readline().strip())

    allTeamsStat.append(teamStat)
    teamsNumber += 1
  return allTeamsStat


def parse2on2TopScores():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 2on2 match statistics top scores.

  @return The dictionary of the match info.
  """
  matchInfo = {}
  scoresInfo = []
  savedField ="frags"
  keys = ["frags", "deaths", "friendkills", "efficiency", "fragstreak", "quadrun","--END--"]
  # skip the head
  sys.stdin.readline()
  field = keys[0]
  i = 0

  while field != "--END--":
    info = sys.stdin.readline().strip().replace("%","")
    if info.count(":") != 0:
      if scoresInfo:
        matchInfo[savedField] = scoresInfo
        scoresInfo = []
        
      savedField = field
      i += 1
      field = keys[i] 
      union = {}
      union["name"] = info.split()[1]
      union["count"] = float(info.split()[2])  
      scoresInfo.append(union)
    else:
      union = {}
      union["name"] = info.split()[0]
      union["count"] = float(info.split()[1])  
      scoresInfo.append(union)
      keys.append("")

  matchInfo[savedField] = scoresInfo 
  return matchInfo  

def parse2on2TeamScores():
  """Parse mvdparser output to JSON format for match info.
     The output for parsing should be for 2on2 match statistics team scores.

  @return The dictionary of the match info.
  """
  matchInfo = []
  # skip the head
  sys.stdin.readline().strip()
  for i in range(2):
    info = sys.stdin.readline().strip()
    union = {}
    union["name"] = info.split()[0][:-1]
    union["frags"] = int(info.split()[1]) 
    union["percentage"] = float(info.split()[2].replace("%","")) 
    matchInfo.append(union)
  
  return matchInfo

def main():
  """Main function. Read mvdparsers output fron stdin and build final match info in JSON.

  @return The output in JSON format.
  """
  try:
    matchInfo = mvdParse2on2()
    print(json.dumps (matchInfo))
  except Exception as e:
    logging.error(traceback.format_exc())

if __name__ == "__main__":
  main()
