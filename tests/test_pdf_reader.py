import pytest
from qrscan import pdf_reader

def test_pdf_to_images_empty():
    with pytest.raises(Exception):
        pdf_reader.pdf_to_images("nonexistent.pdf") 