import subprocess

process = subprocess.run(
["python", "reaction_game_v1.py"], input="\n\n", encoding="utf-8"
)