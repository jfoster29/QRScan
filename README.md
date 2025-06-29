# QRScan

A modular Python agent for scanning PDFs for QR codes, extracting URLs, checking for malicious links, and storing results in JSON or SQLite.

## Features
- PDF to image conversion (PyMuPDF, OpenCV)
- QR code extraction (pyzbar)
- URL safety checking (VirusTotal API + heuristics)
- Results export to JSON or SQLite

## Installation

```bash
# Clone the repo
$ git clone <repo-url>
$ cd qrscan

# Install dependencies with Poetry
$ poetry install
```

## Usage Example

```python
from qrscan import QRCodeAgent

agent = QRCodeAgent(virus_total_api_key="your_api_key")
results = agent.scan_pdf("sample_data/sample.pdf")
agent.save_results(results, "output.json")
```

## Configuration
- Place your VirusTotal API key in a `.env` file as `VIRUSTOTAL_API_KEY=your_api_key`.

## Testing

```bash
$ poetry run pytest
```

## Project Structure

```
qrscan/                        # Project root
├── qrscan/                    # Main Python package
│   ├── __init__.py            # Exposes QRCodeAgent
│   ├── agent.py               # Main orchestrator class
│   ├── pdf_reader.py          # PDF → list of OpenCV images
│   ├── qr_decoder.py          # Image → QR code data
│   ├── url_checker.py         # VirusTotal + heuristic URL scanning
│   └── result_writer.py       # JSON or SQLite result storage
├── tests/                     # Unit tests for each module
├── .env                       # API keys (gitignored)
├── .gitignore                 # Ignore virtualenv, pycache, .env, etc.
├── pyproject.toml             # Poetry configuration
├── poetry.lock                # Poetry dependency lockfile
├── README.md                  # This file
└── sample_data/               # PDFs for testing
``` 