import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

import django

django.setup()

from pathlib import Path

import pandas as pd

from sports.models import Sport, Weight

BASE_DIR = Path(__file__).resolve().parent
import os

ROOT_DIR = os.path.dirname(BASE_DIR)


def sports():
    SPORT_DATA_FILE = os.path.join(BASE_DIR, "sport.csv")

    db = pd.read_csv(SPORT_DATA_FILE)

    for i in range(0, len(db)):
        name = db["name"][i]

        Sport.objects.create(name=name)


def weights():
    WEIGHT_DATA_FILE = os.path.join(BASE_DIR, "weight.csv")

    db = pd.read_csv(WEIGHT_DATA_FILE)

    for i in range(0, len(db)):
        sport_id = db["sport"][i]
        name = db["name"][i]
        gender = db["gender"][i]
        min_weight = db["min_weight"][i]

        Weight.objects.create(name=name, sport_id=sport_id, gender=gender, min_weight=min_weight)


if __name__ == "__main__":
    sports()
    weights()
