import pytest
from qrscan import qr_decoder
import numpy as np

def test_extract_qr_codes_empty():
    images = [np.zeros((100, 100, 3), dtype=np.uint8)]
    results = qr_decoder.extract_qr_codes(images)
    assert isinstance(results, list) 