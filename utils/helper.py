import re


WATCHLIST = [
    "Pecharunt",
    "Koraidon",
    "Miraidon",
    "Wo-Chien",
    "Chien-Pao",
    "Ting-Lu",
    "Chi-Yu",
    "Ogerpon",
    "Terapagos",
    "Zarude",
    "Zacian",
    "Zamazenta",
    "Eternatus",
    "Urshifu",
    "Glastrier",
    "Spectrier",
    "Calyrex",
    "Magearna",
    "Marshadow",
    "Zeraora",
    "Type: Null",
    "Silvally",
    "Tapu Koko",
    "Tapu Lele",
    "Tapu Bulu",
    "Tapu Fini",
    "Cosmog",
    "Cosmoem",
    "Solgaleo",
    "Lunala",
    "Necrozma",
    "Diancie",
    "Hoopa",
    "Volcanion",
    "Xerneas",
    "Yveltal",
    "Zygarde",
    "Victini",
    "Keldeo",
    "Meloetta",
    "Genesect",
    "Cobalion",
    "Terrakion",
    "Virizion",
    "Tornadus",
    "Thundurus",
    "Reshiram",
    "Zekrom",
    "Landorus",
    "Kyurem",
    "Phione",
    "Manaphy",
    "Darkrai",
    "Shaymin",
    "Arceus",
    "Uxie",
    "Mesprit",
    "Azelf",
    "Dialga",
    "Palkia",
    "Heatran",
    "Regigigas",
    "Giratina",
    "Cresselia",
    "Jirachi",
    "Deoxys",
    "Regirock",
    "Regice",
    "Registeel",
    "Latias",
    "Latios",
    "Kyogre",
    "Groudon",
    "Rayquaza",
    "Mewtwo",
]


def find_watchlist_match(text):
    """Return (matched Pokémon name, shiny flag), or (None, False)."""
    if not text:
        return None, False

    is_shiny = re.search(r"\bshiny\b", text, re.IGNORECASE) is not None

    for name in WATCHLIST:
        # Flexible whitespace supports names such as "Tapu Koko".
        escaped = re.escape(name).replace(r"\ ", r"\s+")
        pattern = rf"(?<!\w){escaped}(?!\w)"
        if re.search(pattern, text, re.IGNORECASE):
            return name, is_shiny

    if is_shiny:
        return "Shiny Pokémon", True

    return None, False


def build_notification(name, is_shiny, original_text):
    """Build a Saved Messages alert; this function never clicks game buttons."""
    level_match = re.search(
        r"\bLv\.?\s*(\d+)\b", original_text or "", re.IGNORECASE
    )
    level = f"Level: {level_match.group(1)}" if level_match else "Level: unknown"
    shiny_label = "\n✨ SHINY encounter!" if is_shiny else ""

    return (
        "🛑 HEXAAUTOHUNT PAUSED\n\n"
        f"Target: {name}\n"
        f"{level}"
        f"{shiny_label}\n\n"
        f"Game message:\n{original_text}\n\n"
        "The encounter has not been clicked or battled.\n"
        "After handling it manually, send /resume to continue."
    )
