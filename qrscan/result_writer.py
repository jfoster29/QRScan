"""
result_writer.py

Persists scan results to JSON or SQLite using pandas.
"""

from typing import List, Dict, Any
import json
import pandas as pd
import os


def save_results(data: List[Dict[str, Any]], output_path: str, format: str = "json") -> None:
    """
    Save results to a file in JSON or SQLite format.

    Args:
        data: List of result dictionaries.
        output_path: Path to the output file.
        format: Output format ('json' or 'sqlite'). If not specified, inferred from extension.
    """
    ext = os.path.splitext(output_path)[1].lower()
    if format is None or format == "json":
        if ext == ".sqlite" or ext == ".db":
            format = "sqlite"
        else:
            format = "json"
    
    if format == "json":
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)
    elif format == "sqlite":
        df = pd.DataFrame(data)
        df.to_sql('qr_scan_results', f'sqlite:///{output_path}', if_exists='replace', index=False)
    else:
        raise ValueError(f"Unsupported format: {format}") 