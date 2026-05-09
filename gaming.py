import random
from urllib.parse import quote
import re
from bs4 import BeautifulSoup
import cloudscraper

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

RELICS = ["Purification Beads", "Blink Rune", "Agility Relic", "Aegis of Acceleration", "Sundering Arc", "Phantom Shell"]

UPGRADED_RELICS = ["ACTIVE: Talisman of Purification", "ACTIVE: Blinking Abyss", "ACTIVE: Agility Greaves", 
                   "ACTIVE: Time-lock Aegis", "ACTIVE: Sundering Echo", "ACTIVE: Shell of Rebuke"]

STARTERS = ["Heroism", "War Banner", "Bluestone Brooch", "Hunter's Cowl", "Blood-soaked Shroud", "Sharpshooter's Arrow",
            "Bumba's Spear", "Archamge's Gem", "Sundering Axe", "Death's Embrace", "Bumba's Hammer", "Pendulum of the Ages"]

ITEMS = [
    # Tier III - Offensive
    "ACTIVE: Blood-Bound Book", "Bancroft's Talon", "Book of Thoth", "ACTIVE: Eros' Bow", "ACTIVE: Sun Beam Bow",
    "Jotunn's Revenge", "Chronos' Pendant", "Transcendence", "Odysseus' Bow", "Rage",
    "Hydra's Lament", "Vital Amplifier", "Daybreak Gavel", "Bracer of The Abyss", "Barbed Carver",
    "Nimble Ring", "Mercury's Talaria", "ACTIVE: Dagger of Frenzy", "ACTIVE: Lernaean Bow", "Devourer's Gauntlet",
    "Divine Ruin", "Soul Gem", "The Executioner", "Gem of Focus", "ACTIVE: Bloodforge", "Polynomicon",
    "Necronomicon", "Oath-Sworn Spear", "Bragi's Harp", "Qin's Blade", "Typhon's Heart",
    "Gluttonous Grimoire", "Tyrfing", "ACTIVE: Death Metal", "The Reaper", "Ancient Signet", "ACTIVE: Pendulum Blade",
    "Hastened Fatalis", "The Cosmic Horror", "Spear of Desolation", "Avenging Blade", "ACTIVE: Arondight",
    "Riptalon", "Tekko-Kagi", "Musashi's Dual Swords", "Doom Orb", "ACTIVE: Jade Scepter", "ACTIVE: Staff of Myrddin",
    "Demon Blade", "Damaru", "The World Stone", "The Crusher", "Totem of Death", "ACTIVE: Omen Drum",
    "Deathbringer", "Soul Reaver", "Rod of Tahuti", "Heartseeker", "Obsidian Shard", "Titan's Bane",
    "ACTIVE: Dreamer's Idol", "ACTIVE: Avatar's Parashu",

    # Tier III - Defensive
    "Gauntlet of Thebes", "Yogi's Necklace", "ACTIVE: Eye of Providence", "Chandra's Grace", "Spectral Armor",
    "ACTIVE: Amanita Charm", "Genji's Guard", "Alchemist Coat", "Phoenix Feather", "ACTIVE: Kinetic Cuirass",
    "Shield of the Phoenix", "Breastplate of Valor", "ACTIVE: Screeching Gargoyle", "Magi's Cloak", "Berserker's Shield",
    "Erosion", "Contagion", "ACTIVE: Stampede", "Prophetic Cloak", "Gladiator's Shield", "ACTIVE: Pharaoh's Curse",
    "ACTIVE: Ancile", "Shroud of Vengeance", "Spirit Robe", "Leviathan's Hide", "Shogun's Ofuda", "Umbral Link",
    "Oni Hunter's Garb", "ACTIVE: Doublet of Binding", "ACTIVE: Hide of the Nemean Lion", "Mystical Mail", "ACTIVE: Glorious Pridwen",
    "Regrowth Striders", "Stone of Binding", "Stygian Anchor", "Wyrmskin Hide", "ACTIVE: Ragnarok's Wake",
    "Freya's Tears", "Mantle Of Discord", "ACTIVE: Heartwood Charm", "Draconic Scale", "ACTIVE: Circe's Hexstone",
    "Xibalban Effigy", "Resolute Mantle", "ACTIVE: Radiant Bulwark", "ACTIVE: Dwarven Plate", "Hussar's Wings",

    # Tier III - Hybrid
    "ACTIVE: Rod Of Asclepius", "ACTIVE: Scepter of Dominion", "ACTIVE: Lifebinder", "ACTIVE: Shield Splitter", "Golden Blade",
    "ACTIVE: Eye of the Storm", "Helm of Radiance", "Gem of Isolation", "Brawler's Beat Stick", "Runeforged Hammer",
    "ACTIVE: Eye of Erebus", "Void Shield", "ACTIVE: Sanguine Lash", "Shifter's Shield", "Void Stone", "Triton's Conch",
    "ACTIVE: Helm of Darkness", "Sphere of Negation", "Wish-Granting Pearl",
]

ALADDIN = "Genie's Lamp"

VULCAN_T1 = ["Dual Mod", "Efficiency Mod", "Alternator Mod"]
VULCAN_T2 = ["Thermal Mod", "Resonator Mod", "Shrapnel Mod"]
VULCAN_T3 = ["Masterwork Mod", "Surplus Mod", "Seismic Mod"]

RATATOSKR = ["Ashwort Acorn", "Briskberry Acorn", "Thistlethorn Acorn"]

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

async def random_god():
    return random.choice(GODS)

async def random_build(god):
    starter = random.choice(STARTERS)
    relic = random.choice(RELICS)

    build = []
    active_items = 0
    item_list = ITEMS.copy()

    # Add god-specific items
    if god == "Aladdin":
        # Aladdin's build will always include Genie's Lamp, but the rest of the build is random
        build.append(ALADDIN)
        active_items += 1

    if god == "Ratatoskr":
        # Ratatoskr's build will always include one of his acorns, but the specific acorn is random
        rat_acorns=RATATOSKR.copy()
        chosen_acorn = random.choice(RATATOSKR)
        rat_acorns.remove(chosen_acorn)
        build.append(chosen_acorn)

        # Add the remaining acorns to the item list so that they can be randomly included in the build
        item_list.extend(rat_acorns)

    while len(build) < 6:
        item = random.choice(item_list)

        # allow selecting active items only if under the active limit
        if active_items < 3 or not item.startswith("ACTIVE:"):
            original_item = item
            display_name = original_item
            if original_item.startswith("ACTIVE:"):
                display_name = original_item.replace("ACTIVE: ", "")
                active_items += 1

            build.append(display_name)
            # remove the original entry (with prefix if present) from the pool
            item_list.remove(original_item)

    msg = f"**{god}** random build:\nStarter: {starter}\nRelic: {relic}\nBuild: {', '.join(build)}"

    # randomly add one of each tier of Vulcan's unique mods if Vulcan is the chosen god
    if god == "Vulcan":
        msg += "\n\nVulcan's unique mods:\n"
        msg += f"Tier I: {random.choice(VULCAN_T1)}\n"
        msg += f"Tier II: {random.choice(VULCAN_T2)}\n"
        msg += f"Tier III: {random.choice(VULCAN_T3)}"

    return msg

async def get_item_info(item_name):
    # Remove "ACTIVE: " prefix if present
    clean_name = item_name.replace("ACTIVE: ", "")
    
    # Format the name for the wiki URL (spaces to underscores, special characters encoded)
    wiki_name = clean_name.replace(" ", "_")
    wiki_name = wiki_name.replace("'", "%27")  # Encode apostrophes
    url_encoded_name = quote(wiki_name, safe="")
    wiki_url = f"https://wiki.smite2.com/w/{url_encoded_name}"
    
    return f"**{clean_name}**\n{wiki_url}"

async def gacha_links():
    msg = "## Honkai Star Rail\n"
    msg += "Prydwen, List of HSR characters - <https://www.prydwen.gg/star-rail/characters/>\n"
    msg += "Star Rail Station, Warp tracker - <https://starrailstation.com/en/warp#char_event>\n"
    msg += "Fribbels, Relic scorer and build evaluator - <https://fribbels.github.io/hsr-optimizer>\n"
    msg += "Gachabase, beta news and info - <https://gachabase.net/>\n"
    msg += "The Genius Archive, endgame clears and info - <https://theherta.com/>\n"
    msg += "Cat Cake Log, cat cake collection info - <https://catcake.hoshimi.io/>\n"

    msg += "## Wuthering Waves\n"
    msg += "Prydwen, List of WW characters - <https://www.prydwen.gg/wuthering-waves/characters>\n"
    msg += "Wuwa Tracker, Warp tracker - <https://wuwatracker.com/>\n"
    msg += "Wuwaflex Echo scorer - <https://wuwaflex.com/>\n"
    msg += "Wuwatracker Event Calendar - <https://wuwatracker.com/timeline>\n"
    msg += "Wuwa Interactive Map - <https://wuthering-waves-map.appsample.com/>\n"

    return msg

async def hsr_banners():
    url = "https://game8.co/games/Honkai-Star-Rail/archives/408381"
    scraper = cloudscraper.create_scraper()
    try:
        res = scraper.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()
    except Exception as e:
        return {"error": f"fetch_failed: {e}", "url": url}

    soup = BeautifulSoup(res.text, "html.parser")

    # Find the table containing Version / Banner Schedule
    table = None
    for tbl in soup.find_all("table"):
        header = tbl.find("th")
        if header and "Version" in header.get_text(" ", strip=True):
            table = tbl
            break

    if table is None:
        return {"error": "table_not_found", "url": url}

    banners = []
    for tr in table.find_all("tr"):
        # skip header rows
        if tr.find("th"):
            continue
        tds = tr.find_all("td")
        if len(tds) < 2:
            continue

        version_text = tds[0].get_text(" ", strip=True)

        chars_td = tds[1]
        chars = []
        # preferred: divs with class 'align' contain character anchors
        for div in chars_td.find_all(class_=lambda c: c and "align" in c):
            a = div.find("a")
            if not a:
                continue
            name = a.get_text(" ", strip=True)
            if name:
                chars.append(name)

        # fallback: find anchors with images directly under the td
        if not chars:
            for a in chars_td.find_all("a"):
                # skip phase links like 'Phase 1'
                txt = a.get_text(" ", strip=True)
                if re.match(r"Phase\s*\d", txt, re.I):
                    continue
                # skip links that look like dates
                if re.search(r"\d{1,2}/\d{1,2}/\d{2,4}", txt):
                    continue
                if txt:
                    chars.append(txt)

        # dedupe while preserving order
        seen = set()
        uniq = []
        for c in chars:
            if c not in seen:
                seen.add(c)
                uniq.append(c)

        banners.append({"version": version_text, "characters": uniq})

    msg = f"## Latest HSR banners (source: {url}):\n"
    for b in banners:
        msg += f"- **{b['version']}**: {', '.join(b['characters'])}\n"

    return msg

async def wuwa_banners():
    url = "https://game8.co/games/Wuthering-Waves/archives/453303"
    scraper = cloudscraper.create_scraper()
    try:
        res = scraper.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        res.raise_for_status()
    except Exception as e:
        return {"error": f"fetch_failed: {e}", "url": url}

    soup = BeautifulSoup(res.text, "html.parser")

    def clean_text(value):
        return re.sub(r"\s+", " ", value or "").strip()

    def extract_banner_title(td):
        anchor = td.find("a")
        if anchor:
            return clean_text(anchor.get_text(" ", strip=True))
        return clean_text(td.get_text(" ", strip=True))

    def extract_featured_names(td):
        names = []
        align_blocks = td.find_all(class_=lambda c: c and "align" in c)

        for block in align_blocks:
            text = clean_text(block.get_text(" ", strip=True))
            if not text:
                continue
            if re.match(r"^Phase\s*\d+$", text, re.I):
                continue
            if re.search(r"\d{1,2}/\d{1,2}/\d{2,4}", text):
                continue
            if text not in names:
                names.append(text)

        return names

    def parse_banner_table(table):
        rows = []
        for tr in table.find_all("tr"):
            if tr.find("th"):
                continue
            tds = tr.find_all("td")
            if len(tds) < 2:
                continue

            banner_title = extract_banner_title(tds[0])
            featured = extract_featured_names(tds[1])

            if banner_title and featured:
                rows.append({"banner": banner_title, "featured": featured})
        return rows

    tables = []
    for table in soup.find_all("table"):
        header_texts = [clean_text(th.get_text(" ", strip=True)) for th in table.find_all("th")]
        header_joined = " | ".join(header_texts)
        if "banner" in header_joined.lower() and "featured characters" in header_joined.lower():
            tables.append(table)

    if len(tables) < 2:
        # Fallback: use the first two banner tables on the page if the header text is wrapped oddly.
        banner_tables = []
        for table in soup.find_all("table"):
            rows = table.find_all("tr")
            if not rows:
                continue
            first_row_headers = [clean_text(th.get_text(" ", strip=True)) for th in rows[0].find_all("th")]
            if len(first_row_headers) >= 2 and "banner" in first_row_headers[0].lower():
                banner_tables.append(table)
        if len(banner_tables) >= 2:
            tables = banner_tables[:2]

    if not tables:
        return {"error": "tables_not_found", "url": url}

    current = parse_banner_table(tables[0])
    upcoming = parse_banner_table(tables[1]) if len(tables) > 1 else []

    msg = f"## Latest Wuthering Waves banners (source: {url}):\n"
    msg += "### Current\n"
    for row in current:
        msg += f"- **{row['banner']}**: {', '.join(row['featured'])}\n"

    if upcoming:
        msg += "### Upcoming\n"
        for row in upcoming:
            msg += f"- **{row['banner']}**: {', '.join(row['featured'])}\n"

    return msg