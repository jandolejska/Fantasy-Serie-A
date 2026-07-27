from pathlib import Path

LOGO_DIR = Path("static/img/teams")

RENAME = {
    "atalanta.football-logos.cc.png": "atalanta.png",
    "bologna.football-logos.cc.png": "bologna.png",
    "cagliari.football-logos.cc.png": "cagliari.png",
    "como-1907.football-logos.cc.png": "como.png",
    "cremonese.football-logos.cc.png": "cremonese.png",
    "fiorentina.football-logos.cc.png": "fiorentina.png",
    "frosinone.football-logos.cc.png": "frosinone.png",
    "genoa.football-logos.cc.png": "genoa.png",
    "inter.football-logos.cc.png": "inter.png",
    "juventus.football-logos.cc.png": "juventus.png",
    "lazio.football-logos.cc.png": "lazio.png",
    "lecce.football-logos.cc.png": "lecce.png",
    "milan.football-logos.cc.png": "milan.png",
    "monza.football-logos.cc.png": "monza.png",
    "napoli.football-logos.cc.png": "napoli.png",
    "parma.football-logos.cc.png": "parma.png",
    "pisa.football-logos.cc.png": "pisa.png",
    "roma.football-logos.cc.png": "roma.png",
    "sassuolo.football-logos.cc.png": "sassuolo.png",
    "torino.football-logos.cc.png": "torino.png",
    "udinese.football-logos.cc.png": "udinese.png",
    "venezia.football-logos.cc.png": "venezia.png"
}

for old_name, new_name in RENAME.items():
    old_path = LOGO_DIR / old_name
    new_path = LOGO_DIR / new_name

    if old_path.exists():
        old_path.rename(new_path)
        print(f"✔ {old_name} → {new_name}")
    else:
        print(f"❌ Nenalezeno: {old_name}")

print("\nHotovo.")