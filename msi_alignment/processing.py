import pandas as pd
from pathlib import Path

from config import (
    data_dir,
    raw_data_dir,
    processed_data_dir,
    aligned_data_dir
)

class processing:

    def __init__(self, msi_data_path):
        self.msi_data_path = msi_data_path # Data file name
        self.msi_data_exact_path = raw_data_dir/msi_data_path # Path to read data file
        self.msi_data_columns = None
        self.numeric_columns = None

    # Clean data function
    def clean_data(self):
        with open(self.msi_data_exact_path, "r", encoding="utf-8") as file:
            lines = []
            for _ in range(4):
                line = file.readline()
                if line == "":
                    break
                lines.append(line.rstrip("\r\n"))

        if len(lines) < 4:
            raise ValueError("Not enough lines to extract column names.")

        column_names = lines[3].split("\t")
        column_names[0:3] = ["Index", "X", "Y"]
        column_names = column_names + ["Last_1", "Last_2"]

        df = pd.read_csv(self.msi_data_exact_path, sep="\t", skiprows=4, header=None)
        df.columns = column_names

        self.set_processed_files_name()
        df.to_csv(self.msi_data_exact_path, index=False, na_rep="NA")


    # Function to get column names from the first row of the file
    def get_columns(self, clean_passed = False):
        if clean_passed:
            self.set_processed_files_name()

        with open(self.msi_data_exact_path, "r", encoding="utf-8") as con:
            lines = [con.readline().rstrip("\r\n")]  # Only read the first line

        if len(lines) < 1 or lines[0] == "":
            raise ValueError(
                "File does not have enough lines to extract column names."
            )

        self.msi_data_columns = lines[0].split(",")  # Split the first line by comma
        self.numeric_columns = pd.to_numeric(pd.Series(self.msi_data_columns), errors="coerce").dropna().to_numpy()

    def set_processed_files_name(self):
        processed_msi_data_name = f"processed_{Path(self.msi_data_path).stem}.csv"
        processed_msi_data_exact_path = processed_data_dir / processed_msi_data_name
        self.msi_data_path = f"processed_{Path(self.msi_data_path).stem}.csv"
        self.msi_data_exact_path = processed_msi_data_exact_path
