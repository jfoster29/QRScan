import pytest
from qrscan import result_writer

def test_save_results_json(tmp_path):
    data = [{"page": 1, "qr_text": "test", "bbox": {"x": 0, "y": 0, "width": 10, "height": 10}}]
    output = tmp_path / "out.json"
    result_writer.save_results(data, str(output), format="json")
    assert output.exists() 