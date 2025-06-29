"""
agent.py

Main orchestrator for modular AI agent to scan PDFs for QR codes, validate URLs, and persist results.
"""

from typing import List, Dict, Optional
import logging
from pathlib import Path
import qrscan.pdf_reader as pdf_reader
import qrscan.qr_decoder as qr_decoder
import qrscan.url_checker as url_checker
import qrscan.result_writer as result_writer


class QRCodeAgent:
    """
    Orchestrates the process of scanning a PDF for QR codes, validating URLs, and saving results.
    """

    def __init__(self, output_format: str = "json", virus_total_api_key: Optional[str] = None) -> None:
        """
        Initialize the QRCodeAgent.

        Args:
            output_format: Output format for results ("json" or "sqlite").
            virus_total_api_key: Optional VirusTotal API key for URL checking.
        """
        self.output_format = output_format
        self.virus_total_api_key = virus_total_api_key
        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

    def scan_pdf(self, pdf_path: str) -> List[Dict]:
        """
        Scan a PDF for QR codes and validate any URLs found.

        Args:
            pdf_path: Path to the PDF file to scan.

        Returns:
            List of dictionaries containing scan results.
        """
        self.logger.info(f"Starting scan of {pdf_path}")
        
        # Step 1: Convert PDF to images
        images = pdf_reader.pdf_to_images(pdf_path)
        self.logger.info(f"Converted PDF to {len(images)} images")
        
        # Step 2: Extract QR codes from images
        qr_results = qr_decoder.extract_qr_codes(images)
        self.logger.info(f"Found {len(qr_results)} QR codes")
        
        # Step 3: Validate QR content (URLs)
        results = []
        for qr in qr_results:
            content = qr.get("qr_text")
            page = qr.get("page")
            bbox = qr.get("bbox")
            if content is None:
                continue
            if self.virus_total_api_key:
                malicious, source = url_checker.check_url_virustotal(content, self.virus_total_api_key)
            else:
                malicious = url_checker.is_url_suspicious_heuristic(content)
                source = "heuristic"
            results.append({
                "page": page,
                "bbox": bbox,
                "qr_content": content,
                "malicious": malicious,
                "source": source
            })
        
        self.logger.info(f"Completed scan with {len(results)} validated results")
        return results

    def save_results(self, results: List[Dict], output_path: str) -> None:
        """
        Save scan results to a file.

        Args:
            results: List of scan result dictionaries.
            output_path: Path where to save the results.
        """
        result_writer.save_results(results, output_path, self.output_format)
        self.logger.info(f"Results saved to {output_path}") 

if __name__ == "__main__":
    agent = QRCodeAgent()
    results = agent.scan_pdf("sample_data/multi_page_multi_qr_codes.pdf")
    agent.save_results(results, "results.json")