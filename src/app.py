from datetime import datetime
from collections import defaultdict
import requests


def get_data(url: str) -> dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()


def calc_summaries(weather_data: dict) -> dict:
    grouped_by_day = defaultdict(list)
    summaries = {}

    # Group entries by day
    for entry in weather_data:
        entry_time = datetime.fromisoformat(entry["date_time"].replace('Z', '+00:00'))
        day_key = entry_time.date()
        grouped_by_day[day_key].append(entry)

    # Process each day
    for day, entries in grouped_by_day.items():
        morning_temps, morning_rains, afternoon_temps, afternoon_rains = [], [], [], []
        all_temps = [entry["average_temperature"] for entry in entries]

        for entry in entries:
            entry_time = datetime.fromisoformat(entry["date_time"].replace('Z', '+00:00'))
            # collect morning period entries
            if 6 <= entry_time.hour < 12:
                morning_temps.append(entry["average_temperature"])
                morning_rains.append(entry["probability_of_rain"])
            # collection afternoon period entries
            elif 12 <= entry_time.hour < 18:
                afternoon_temps.append(entry["average_temperature"])
                afternoon_rains.append(entry["probability_of_rain"])

        key = day.strftime("%A %B %d").replace(" 0", " ")
        summaries[key] = {
            "morning_average_temperature": "Insufficient forecast data" if not morning_temps else str(round(sum(morning_temps) / len(morning_temps))),
            "morning_chance_of_rain": "Insufficient forecast data" if not morning_rains else str(round(sum(morning_rains) / len(morning_rains), 2)),
            "afternoon_average_temperature": "Insufficient forecast data" if not afternoon_temps else str(round(sum(afternoon_temps) / len(afternoon_temps))),
            "afternoon_chance_of_rain": "Insufficient forecast data" if not afternoon_rains else str(round(sum(afternoon_rains) / len(afternoon_rains), 2)),
            "high_temperature": str(max(all_temps)),
            "low_temperature": str(min(all_temps))
        }

    return summaries


def main():
    weather_data = get_data("https://e75urw7oieiszbzws4gevjwvze0baaet.lambda-url.eu-west-2.on.aws/")
    summaries = calc_summaries(weather_data)

    for day, summary in summaries.items():
        summary = ["Day: " + day + "\n\n",
                   "Morning Average Temperature: ", summary["morning_average_temperature"] + "\n",
                   "Morning Chance Of Rain: ", summary["morning_chance_of_rain"] + "\n",
                   "Afternoon Average Temperature: ", summary["afternoon_average_temperature"] + "\n",
                   "Afternoon Chance Of Rain: ", summary["afternoon_chance_of_rain"] + "\n",
                   "High Temperature: " + summary["high_temperature"] + "\n",
                   "Low Temperature: " + summary["low_temperature"] + "\n"]

        print("".join(summary))


if __name__ == "__main__":
    main()
