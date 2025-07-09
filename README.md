# Amazon ML OCR Project

This project performs Optical Character Recognition (OCR) on Amazon product images to extract text information.

## Files Description

- [`myocr.ipynb`](myocr.ipynb) - Main Jupyter notebook for OCR processing
- [`Model_OCR.py`](Model_OCR.py) - Python script for OCR model implementation
- [`test.csv`](test.csv) - Test dataset
- [`Img_text_new.csv`](Img_text_new.csv) - OCR results

## Requirements

```python
pip install easyocr opencv-python matplotlib pandas tqdm pillow
```

## Usage

1. Run the Jupyter notebook [`myocr.ipynb`](myocr.ipynb)
2. Or execute the Python script [`Model_OCR.py`](Model_OCR.py)

## Features

- OCR text extraction from product images
- Batch processing of multiple images
- Results export to CSV format

## License

MIT