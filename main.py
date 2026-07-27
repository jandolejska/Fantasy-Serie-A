from fantacalcio import parse
from league import play_season

print("=" * 40)
print("Fantasy Serie A Manager")
print("=" * 40)

players = parse()

play_season(players)