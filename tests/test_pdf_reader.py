"""
Tests for pdf_reader module.

Tests PDF-to-image conversion functionality including edge cases and error handling.
"""

import pytest
import numpy as np
import tempfile
import os
import cv2
from unittest.mock import Mock, patch, MagicMock
from qrscan import pdf_reader


def test_pdf_to_images_empty():
    """Test that non-existent PDF raises appropriate exception."""
    with pytest.raises(Exception):
        pdf_reader.pdf_to_images("nonexistent.pdf")


def test_pdf_to_images_successful_conversion():
    """Test successful PDF to images conversion."""
    # Create a mock PDF document with multiple pages
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_page1 = Mock()
    mock_page2 = Mock()
    
    # Mock pixmap for page 1 (RGB format)
    mock_pix1 = Mock()
    mock_pix1.samples = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8).tobytes()
    mock_pix1.height = 100
    mock_pix1.width = 100
    mock_pix1.n = 3
    
    # Mock pixmap for page 2 (RGBA format)
    mock_pix2 = Mock()
    mock_pix2.samples = np.random.randint(0, 255, (150, 150, 4), dtype=np.uint8).tobytes()
    mock_pix2.height = 150
    mock_pix2.width = 150
    mock_pix2.n = 4
    
    mock_page1.get_pixmap.return_value = mock_pix1
    mock_page2.get_pixmap.return_value = mock_pix2
    
    mock_doc.__len__.return_value = 2
    mock_doc.load_page.side_effect = [mock_page1, mock_page2]
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc):
        with patch('qrscan.pdf_reader.cv2.cvtColor') as mock_cvt:
            mock_cvt.return_value = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
            
            result = pdf_reader.pdf_to_images("test.pdf")
            
            assert len(result) == 2
            assert isinstance(result[0], np.ndarray)
            assert isinstance(result[1], np.ndarray)
            assert result[0].shape[2] == 3  # BGR format
            assert result[1].shape[2] == 3  # BGR format


def test_pdf_to_images_single_page():
    """Test PDF with single page conversion."""
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_page = Mock()
    
    # Mock pixmap for single page (RGB format)
    mock_pix = Mock()
    mock_pix.samples = np.random.randint(0, 255, (200, 200, 3), dtype=np.uint8).tobytes()
    mock_pix.height = 200
    mock_pix.width = 200
    mock_pix.n = 3
    
    mock_page.get_pixmap.return_value = mock_pix
    mock_doc.__len__.return_value = 1
    mock_doc.load_page.return_value = mock_page
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc):
        result = pdf_reader.pdf_to_images("single_page.pdf")
        
        assert len(result) == 1
        assert isinstance(result[0], np.ndarray)
        assert result[0].shape == (200, 200, 3)


def test_pdf_to_images_rgba_conversion():
    """Test RGBA to BGR conversion path."""
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_page = Mock()
    
    # Mock pixmap with RGBA format (4 channels)
    mock_pix = Mock()
    mock_pix.samples = np.random.randint(0, 255, (100, 100, 4), dtype=np.uint8).tobytes()
    mock_pix.height = 100
    mock_pix.width = 100
    mock_pix.n = 4
    
    mock_page.get_pixmap.return_value = mock_pix
    mock_doc.__len__.return_value = 1
    mock_doc.load_page.return_value = mock_page
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc):
        with patch('qrscan.pdf_reader.cv2.cvtColor') as mock_cvt:
            expected_bgr = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
            mock_cvt.return_value = expected_bgr
            
            result = pdf_reader.pdf_to_images("rgba_test.pdf")
            
            assert len(result) == 1
            assert isinstance(result[0], np.ndarray)
            assert isinstance(expected_bgr, np.ndarray)
            assert np.array_equal(result[0], expected_bgr), f"result[0]={result[0]}, expected_bgr={expected_bgr}"
            assert mock_cvt.call_count == 1
            args, kwargs = mock_cvt.call_args
            assert np.array_equal(args[0], np.frombuffer(mock_pix.samples, dtype=np.uint8).reshape(100, 100, 4))
            assert args[1] == cv2.COLOR_RGBA2BGR


def test_pdf_to_images_grayscale_conversion():
    """Test grayscale to BGR conversion path."""
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_page = Mock()
    
    # Mock pixmap with grayscale format (1 channel)
    mock_pix = Mock()
    mock_pix.samples = np.random.randint(0, 255, (100, 100, 1), dtype=np.uint8).tobytes()
    mock_pix.height = 100
    mock_pix.width = 100
    mock_pix.n = 1
    
    mock_page.get_pixmap.return_value = mock_pix
    mock_doc.__len__.return_value = 1
    mock_doc.load_page.return_value = mock_page
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc):
        with patch('qrscan.pdf_reader.cv2.cvtColor') as mock_cvt:
            expected_bgr = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8)
            mock_cvt.return_value = expected_bgr
            
            result = pdf_reader.pdf_to_images("grayscale_test.pdf")
            
            assert len(result) == 1
            assert isinstance(result[0], np.ndarray)
            assert isinstance(expected_bgr, np.ndarray)
            assert np.array_equal(result[0], expected_bgr), f"result[0]={result[0]}, expected_bgr={expected_bgr}"
            assert mock_cvt.call_count == 1
            args, kwargs = mock_cvt.call_args
            assert np.array_equal(args[0], np.frombuffer(mock_pix.samples, dtype=np.uint8).reshape(100, 100, 1))
            assert args[1] == cv2.COLOR_GRAY2BGR


def test_pdf_to_images_rgb_no_conversion():
    """Test RGB format that doesn't need conversion."""
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_page = Mock()
    
    # Mock pixmap with RGB format (3 channels)
    mock_pix = Mock()
    mock_pix.samples = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8).tobytes()
    mock_pix.height = 100
    mock_pix.width = 100
    mock_pix.n = 3
    
    mock_page.get_pixmap.return_value = mock_pix
    mock_doc.__len__.return_value = 1
    mock_doc.load_page.return_value = mock_page
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc):
        with patch('qrscan.pdf_reader.cv2.cvtColor') as mock_cvt:
            result = pdf_reader.pdf_to_images("rgb_test.pdf")
            
            assert len(result) == 1
            assert isinstance(result[0], np.ndarray)
            assert result[0].shape == (100, 100, 3)
            # Should not call cv2.cvtColor for RGB format
            mock_cvt.assert_not_called()


def test_pdf_to_images_empty_pdf():
    """Test PDF with no pages."""
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_doc.__len__.return_value = 0
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc):
        result = pdf_reader.pdf_to_images("empty.pdf")
        
        assert len(result) == 0
        assert isinstance(result, list)


def test_pdf_to_images_file_io_error():
    """Test handling of file I/O errors."""
    with patch('qrscan.pdf_reader.fitz.open', side_effect=FileNotFoundError("File not found")):
        with pytest.raises(FileNotFoundError):
            pdf_reader.pdf_to_images("nonexistent.pdf")


def test_pdf_to_images_corrupted_pdf():
    """Test handling of corrupted PDF files."""
    with patch('qrscan.pdf_reader.fitz.open', side_effect=Exception("Corrupted PDF")):
        with pytest.raises(Exception):
            pdf_reader.pdf_to_images("corrupted.pdf")


def test_pdf_to_images_page_load_error():
    """Test handling of page loading errors."""
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_doc.__len__.return_value = 1
    mock_doc.load_page.side_effect = Exception("Page load error")
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc):
        with pytest.raises(Exception):
            pdf_reader.pdf_to_images("error_test.pdf")


def test_pdf_to_images_pixmap_error():
    """Test handling of pixmap creation errors."""
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_page = Mock()
    mock_page.get_pixmap.side_effect = Exception("Pixmap error")
    
    mock_doc.__len__.return_value = 1
    mock_doc.load_page.return_value = mock_page
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc):
        with pytest.raises(Exception):
            pdf_reader.pdf_to_images("pixmap_error.pdf")


def test_pdf_to_images_unsupported_format():
    """Test handling of unsupported pixel formats."""
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_page = Mock()
    
    # Mock pixmap with unsupported format (5 channels)
    mock_pix = Mock()
    mock_pix.samples = np.random.randint(0, 255, (100, 100, 5), dtype=np.uint8).tobytes()
    mock_pix.height = 100
    mock_pix.width = 100
    mock_pix.n = 5  # Unsupported format
    
    mock_page.get_pixmap.return_value = mock_pix
    mock_doc.__len__.return_value = 1
    mock_doc.load_page.return_value = mock_page
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc):
        # Should not raise exception but may produce unexpected results
        result = pdf_reader.pdf_to_images("unsupported.pdf")
        assert len(result) == 1
        assert isinstance(result[0], np.ndarray)


def test_pdf_to_images_context_manager():
    """Test that the PDF document is properly closed using context manager."""
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_doc.__len__.return_value = 0
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc) as mock_open:
        pdf_reader.pdf_to_images("test.pdf")
        
        # Verify context manager was used
        mock_open.assert_called_once_with("test.pdf")
        mock_doc.__enter__.assert_called_once()
        mock_doc.__exit__.assert_called_once()


def test_pdf_to_images_matrix_parameter():
    """Test that the correct matrix parameter is used for pixmap creation."""
    mock_doc = MagicMock()
    mock_doc.__enter__ = Mock(return_value=mock_doc)
    mock_doc.__exit__ = Mock(return_value=None)
    mock_page = Mock()
    
    mock_pix = Mock()
    mock_pix.samples = np.random.randint(0, 255, (100, 100, 3), dtype=np.uint8).tobytes()
    mock_pix.height = 100
    mock_pix.width = 100
    mock_pix.n = 3
    
    mock_page.get_pixmap.return_value = mock_pix
    mock_doc.__len__.return_value = 1
    mock_doc.load_page.return_value = mock_page
    
    with patch('qrscan.pdf_reader.fitz.open', return_value=mock_doc):
        with patch('qrscan.pdf_reader.fitz.Matrix') as mock_matrix:
            mock_matrix.return_value = "test_matrix"
            
            pdf_reader.pdf_to_images("test.pdf")
            
            # Verify Matrix was called with correct parameters
            mock_matrix.assert_called_once_with(1, 1)
            mock_page.get_pixmap.assert_called_once_with(matrix="test_matrix") 