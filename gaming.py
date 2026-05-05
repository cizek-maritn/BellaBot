import random

GODS = [
    "Achilles", "Agni", "Aladdin", "Amaterasu", "Anhur", "Anubis", "Aphrodite", 
    "Apollo", "Ares", "Artemis", "Artio", "Athena", "Atlas", "Awilix", "Bacchus", 
    "Baron Samedi", "Bellona", "Cabrakan", "Cerberus", "Cernunnos", "Chaac", 
    "Charon", "Chiron", "Cupid", "Da Ji", "Danzaburou", "Discordia", "Eset", 
    "Fenrir", "Ganesha", "Geb", "Gilgamesh", "Guan Yu", "Hades", "Hecate", 
    "Hercules", "Hou Yi", "Hua Mulan", "Hun Batz", "Ishtar", "Izanami", "Janus", 
    "Jing Wei", "Jormungandr", "Kali", "Khepri", "Kukulkan", "Loki", "Medusa", 
    "Mercury", "Merlin", "Mordred", "Morgan Le Fay", "Ne Zha", "Neith", "Nemesis", 
    "Nu Wa", "Nut", "Odin", "Osiris", "Pele", "Poseidon", "Princess Bari", "Ra", 
    "Rama", "Ratatoskr", "Scylla", "Sobek", "Sol", "Sun Wukong", "Susano", 
    "Sylvanus", "Thanatos", "The Morrigan", "Thor", "Tsukuyomi", "Ullr", "Vulcan", 
    "Xbalanque", "Yemoja", "Ymir", "Zeus"
]

async def randomize_teams(players, team_count):
    players = players.replace(",", "")
    player_list = players.split(" ")
    random.shuffle(player_list)
    teams = [[] for _ in range(team_count)]
    
    for i, player in enumerate(player_list):
        teams[i % team_count].append(player)
    
    return teams

async def randomize_gods(teams, aspects):
    team_gods = []
    for team in teams:
        team_god = [random.choice(GODS) for _ in range(len(team))]
        if aspects:
            for i, god in enumerate(team_god):
                rng=random.random()
                if rng < 0.5:
                    team_god[i] = "Aspect " + god
        team_gods.append(team_god)
    
    return team_gods

async def latest_god():
    return "Atlas"