from fantacalcio import parse
from league import play_season

print("=" * 40)
print("Fantacalcio Manager")
print("=" * 40)

players = parse()

play_season(players)