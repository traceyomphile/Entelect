import json
from pathlib import Path
import Objects


class Main:
    def __init__(self, input_file: Path, output_file: Path):
        self.input_file: Path = Path(input_file)
        self.output_file: Path = Path(output_file)

    def read_input(self) -> dict:
        try:
            with open(self.input_file, "r", encoding="utf-8") as file:
                data = json.load(file)
                return data
        except FileNotFoundError:
            print(f"Error: The file '{self.input_file}' was not found.")
            return None
        except json.JSONDecodeError:
            print(f"Error: The file '{self.input_file}' does not contain valid JSON.")
            return None

    def write_output(self, data):
        try:
            self.output_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.output_file, "w", encoding="utf-8") as file:
                json.dump(data, file, indent=4)
        except OSError as e:
            print(f"Error writing to file '{self.output_file}': {e}")

    def parse_data(self):
        data = self.read_input()
        if data is None:
            return None
        
        car_contents = data.get("car", {})
        car = Objects.Car(
            accel_m_per_s2=car_contents.get("accel_m/se2", 0),
            brake_m_per_s2=car_contents.get("brake_m/se2", 0),
            limp_constant_m_per_s=car_contents.get("limp_constant_m/s", 0),
            crawl_constant_m_per_s=car_contents.get("crawl_constant_m/s", 0)
        )
        race_contents = data.get("race", {})
        race = Objects.Race(
            name=race_contents.get("name", ""),
            laps=race_contents.get("laps", 0),
            corner_crash_penalty_s=race_contents.get("corner_crash_penalty_s", 0.0),
            starting_weather_condition_id=race_contents.get("starting_weather_condition_id", 0)
        )
        track_contents = data.get("track", {})
        track = Objects.Track(
            length_m=track_contents.get("length_m", 0),
            corners=track_contents.get("corners", [])
        )

        tyres_contents = data.get("tyres", {})
        tyres = Objects.Tyres(
            grip_m_per_s2=tyres_contents.get("grip_m/se2", 0),
            wear_constant_m_per_s=tyres_contents.get("wear_constant_m/s", 0)
        )

        weather_contents = data.get("weather", {})
        weather = Objects.Weather(
            condition_id=weather_contents.get("condition_id", 0),
            change_probability_percent=weather_contents.get("change_probability_percent", 0)
        )

    def main(self):
        data = self.read_input()

        if data is None:
            return

        print("JSON loaded successfully:")
        print(json.dumps(data, indent=4))

        self.write_output(data)
        print(f"\nOutput written to: {self.output_file}")


if __name__ == "__main__":
    src_dir = Path(__file__).parent
    project_dir = src_dir.parent

    input_file = project_dir / "input" / "level1.json"
    output_file = project_dir / "output" / "output.json"

    app = Main(input_file, output_file)
    app.main()