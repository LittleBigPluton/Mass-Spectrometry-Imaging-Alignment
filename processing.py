import pandas as pd

from config import (
    data_dir,
    raw_data_dir,
    processed_data_dir,
    aligned_data_dir
)

class processing:

    def __init__(msi_data_path):
        self.msi_data_path = msi_data # Data file name
        self.msi_data_exact_path = raw_data_dir/msi_data_path # Path to read data file
        self.column_names = None
        self.aligned_data_name = None
        self.aligned_data_exact_path = None

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

        processed_msi_data_name = re.sub(r"(.*/)(.*)(\.txt)$", r"\1processed_\2\3", self.msi_data_path)
        processed_msi_data_exat_path = processed_data_dir / processed_msi_data_name
        df.to_csv(processed_msi_data_exat_path, index=False, na_rep="NA")
         # Return the cleaned file for further use
         self.msi_data = processed_msi_data_name
         self.msi_data_exact_path = processed_msi_data_exat_path

    # Function to get column names from the first row of the file
    def get_columns(self):
        with open(self.msi_data_exact_path, "r", encoding="utf-8") as con:
            lines = [con.readline().rstrip("\r\n")]  # Only read the first line

        if len(lines) < 1 or lines[0] == "":
            raise ValueError(
                "File does not have enough lines to extract column names."
            )

        column_names = lines[0].split(",")  # Split the first line by comma
        self.column_names = column_names
        return column_names

    # Modify file
    def modify_file(self, change_list=None, change=True):
        if change_list is None:
            change_list = {}

        df = pd.read_csv(self.msi_data_exact_path)
        if change and len(change_list) > 0:
            # Save DF's column names
            updated_names = list(df.columns)
            for name in change_list:
                if name in updated_names:
                    print("Changed")
                    print(name)
                    print(change_list[name])
                    updated_names = [change_list[name] if column_name == name else column_name for column_name in updated_names]
            df.columns = updated_names

        self.aligned_data_name = re.sub(r"\.txt$", "_aligned.csv", self.msi_data)
        self.aligned_data_exact_path = aligned_data_dir / aligned_data_name
        df.to_csv(self.aligned_data_exact_path, index=False, quoting=csv.QUOTE_NONE, escapechar="\\")
        print("File saved to:",self.aligned_data_exact_path)
