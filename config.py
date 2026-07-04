from pathlib import Path

root_directory = Path(__file__).resolve().parent

# Data folders
data_dir = root_directory / "data"
raw_data_dir = data_dir / "raw"
processed_data_dir = data_dir / "processed"
aligned_data_dir = data_dir / "aligned"

# Figure folder
figures_dir = root_directory / "figures"

# Create directories if they do not already exist
data_dir.mkdir(parents=True, exist_ok=True)
raw_data_dir.mkdir(parents=True, exist_ok=True)
processed_data_dir.mkdir(parents=True, exist_ok=True)
figures_dir.mkdir(parents=True, exist_ok=True)
aligned_data_dir.mkdir(parents=True, exist_ok=True)

# Define data files that aligned
reference_file = "20240409_NZ10_6_04042024_CLMC.txt"
sample_file = "20240408_NZ5_6_04042024_CLMC.txt"
tolerance = 0.0005
