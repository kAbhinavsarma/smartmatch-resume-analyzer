"""
Professional PDF Text Extraction Module

This module provides robust text extraction capabilities for PDF documents,
supporting both direct text extraction and OCR fallback for image-based content.
Designed for enterprise-grade resume and document processing applications.

Author: Resume Analysis Team
Version: 1.0.0
"""

import fitz  # PyMuPDF for direct PDF text extraction
from pdf2image import convert_from_bytes
import pytesseract  # OCR capability for image-based PDFs
from PIL import Image
from typing import BinaryIO, Optional
import re
import logging

# Configure logging for error tracking
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ProfessionalTextExtractor:
    """
    Advanced text extraction system for PDF documents.
    
    This class provides multiple extraction methods with intelligent fallback
    to ensure maximum text recovery from various PDF formats including
    native text PDFs and image-based scanned documents.
    """
    
    def __init__(self, tesseract_path: Optional[str] = None):
        """
        Initialize the text extraction system.
        
        Args:
            tesseract_path: Optional path to Tesseract executable for OCR operations
        """
        if tesseract_path:
            pytesseract.pytesseract.tesseract_cmd = tesseract_path
            logger.info(f"Tesseract path configured: {tesseract_path}")
    
    def extract_text_from_pdf_document(self, pdf_file: BinaryIO) -> str:
        """
        Extract text from PDF using intelligent multi-method approach.
        
        This method first attempts direct text extraction using PyMuPDF for optimal
        performance and accuracy. If insufficient text is found, it falls back to
        OCR processing for image-based content.
        
        Args:
            pdf_file: Binary file object containing the PDF document
            
        Returns:
            str: Cleaned and processed text content from the PDF
            
        Raises:
            Exception: If both extraction methods fail
        """
        logger.info("Starting PDF text extraction process")
        
        # Primary extraction method: Direct text extraction
        try:
            pdf_file.seek(0)  # Reset file pointer
            pdf_document = fitz.open(stream=pdf_file.read(), filetype="pdf")
            extracted_text = ""
            
            for page_number in range(pdf_document.page_count):
                current_page = pdf_document[page_number]
                page_text = current_page.get_text()
                extracted_text += page_text
                logger.debug(f"Extracted {len(page_text)} characters from page {page_number + 1}")
            
            pdf_document.close()
            
            # Check if sufficient text was extracted
            if extracted_text.strip() and len(extracted_text.strip()) > 50:
                logger.info(f"Successfully extracted {len(extracted_text)} characters using direct method")
                return self._clean_and_normalize_text(extracted_text)
                
        except Exception as extraction_error:
            logger.warning(f"Direct text extraction failed: {str(extraction_error)}")
        
        # Fallback method: OCR-based extraction
        logger.info("Attempting OCR-based text extraction")
        pdf_file.seek(0)  # Reset file pointer for OCR attempt
        try:
            ocr_extracted_text = self._extract_text_using_ocr(pdf_file)
            logger.info(f"Successfully extracted {len(ocr_extracted_text)} characters using OCR")
            return self._clean_and_normalize_text(ocr_extracted_text)
        except Exception as ocr_error:
            logger.error(f"OCR text extraction failed: {str(ocr_error)}")
            raise Exception("Unable to extract text from PDF using available methods")
    
    def _extract_text_using_ocr(self, pdf_file: BinaryIO) -> str:
        """
        Extract text from PDF using Optical Character Recognition.
        
        This method converts PDF pages to images and applies OCR to extract text.
        Particularly useful for scanned documents or image-based PDFs.
        
        Args:
            pdf_file: Binary file object containing the PDF document
            
        Returns:
            str: Text extracted through OCR processing
        """
        try:
            # Convert PDF pages to images for OCR processing
            images = convert_from_bytes(pdf_file.read())
            extracted_text = ""
            
            # Apply OCR to each page image
            for page_image in images:
                page_text = pytesseract.image_to_string(page_image)
                extracted_text += page_text + "\n"
                
            logger.info(f"OCR extraction completed successfully, extracted {len(extracted_text)} characters")
            return extracted_text.strip()
            
        except Exception as e:
            logger.error(f"OCR extraction failed: {e}")
            return ""
    
    def _clean_and_normalize_text(self, text: str) -> str:
        """
        Clean and normalize extracted text for processing while preserving structure.
        
        This method removes excessive whitespace but maintains line breaks for
        better structure preservation during resume parsing.
        
        Args:
            text: Raw extracted text
            
        Returns:
            str: Cleaned and normalized text with preserved structure
        """
        # Replace multiple spaces with single spaces but preserve line breaks
        text = re.sub(r'[ \t]+', ' ', text)  # Only collapse horizontal whitespace
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)  # Limit multiple line breaks to double
        
        # Remove leading/trailing whitespace from each line but preserve empty lines
        lines = []
        for line in text.splitlines():
            stripped_line = line.strip()
            if stripped_line or len(lines) == 0 or lines[-1]:  # Keep empty lines between content
                lines.append(stripped_line)
        
        # Join lines and clean up excessive empty lines at start/end
        normalized_text = '\n'.join(lines).strip()
        
        logger.debug(f"Text normalization completed: {len(normalized_text)} characters")
        return normalized_text
    
    def _clean_text(self, text: str) -> str:
        """
        Clean extracted text by lowercasing and removing extra whitespace.
        
        Args:
            text: Raw extracted text
            
        Returns:
            Cleaned text
        """
        text = text.lower()
        text = "\n".join([line.strip() for line in text.splitlines() if line.strip()])
        return text

# Global instance for production use
professional_text_extractor = ProfessionalTextExtractor()

def extract_text_from_pdf_document(file: BinaryIO) -> str:
    """
    Extract text from PDF document using professional text extraction methods.
    
    Args:
        file: Binary file object containing the PDF document
        
    Returns:
        str: Extracted text content from the PDF
    """
    return professional_text_extractor.extract_text_from_pdf_document(file)
