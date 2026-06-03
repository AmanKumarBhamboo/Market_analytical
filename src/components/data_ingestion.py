import os
import sys
import pandas as pd
import yaml

def load_config() -> dict:
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.abspath(os.path.join(current_dir, "..", ".."))
    config_path = os.path.join(project_root, "config", "config.yaml")

    if not os.path.exists(config_path):
        raise FileNotFoundError(f"Configuration file not found at: {config_path}")

    with open(config_path, "r") as f:
        return yaml.safe_load(f), project_root

def to_camel_case(col: str) -> str:
    col = col.strip()
    words = col.split()
    if not words:
        return col
    return words[0].lower() + "".join(w.capitalize() for w in words[1:])

def ingest_data():
    """
    Config file se file name utha kar data ingest aur clean karta hai.
    """
    # 1. Config aur Project Root load karo
    config, project_root = load_config()
    ingest_cfg = config["data_ingestion"]

    # 2. Input Path Build Karo

    input_csv_path = os.path.join(
        project_root, "data", ingest_cfg["input_file_name"]
    )

    # 3. Output Paths ko dynamically build karo (artifacts/Data)
    artifacts_dir = os.path.join(
        project_root, ingest_cfg["artifacts_root"], ingest_cfg["raw_data_folder"]
    )
    os.makedirs(artifacts_dir, exist_ok=True)

    # 4. Data Read Karo aur Check Karo
    if not os.path.exists(input_csv_path):
        print(f"Error: Input file '{input_csv_path}' nahi mili!")
        sys.exit(1)

    print(f"📖 Reading data from: {input_csv_path}")
    df = pd.read_csv(input_csv_path)

    # 5. Config ke hisab se cleaning apply karo
    if ingest_cfg["clean_columns"]:
        df.columns = df.columns.map(lambda c: c.strip())
        df.columns = df.columns.map(to_camel_case)

    if ingest_cfg["strip_spaces"]:
        for col in df.select_dtypes(include="object").columns:
            df[col] = df[col].str.strip()

    # 6. Output file save karo
    file_name = ingest_cfg["input_file_name"]
    output_path = os.path.join(artifacts_dir, file_name)
    df.to_csv(output_path, index=False)

    print(" Ingestion Successfully Completed")
    print(f"Saved Location : {output_path}")
    print(f"Total Rows/Cols: {df.shape}")
    print(f"Cleaned Columns: {list(df.columns)}\n")
    return df


if __name__ == "__main__":
    ingest_data()