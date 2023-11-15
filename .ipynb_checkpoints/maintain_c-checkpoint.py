import subprocess
import pickle
import sys

with open("searched_file", "rb") as searched_file:
    searched = pickle.load(searched_file)

antes = 0
agora = 1
while antes < agora:
    print(f"quantidade coletada: {agora-antes}; total: {agora}")
    with open("searched_file", "rb") as searched_file:
        searched = pickle.load(searched_file)
    antes = len(searched)
    # Run the other script
    subprocess.run(["python", "collect_parallel.py", sys.argv[1], "5"])
    with open("searched_file", "rb") as searched_file:
        searched = pickle.load(searched_file)
    agora = len(searched)