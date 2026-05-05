import random

async def randomize_teams(players, team_count):
    player_list = players.split(" ")
    random.shuffle(player_list)
    teams = [[] for _ in range(team_count)]
    
    for i, player in enumerate(player_list):
        teams[i % team_count].append(player)
    
    return teams