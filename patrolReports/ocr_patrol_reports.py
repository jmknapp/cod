#!/usr/bin/env python3
"""OCR USS Cod Patrol Reports with Google Cloud Vision."""

import os
import io
import json
import sys
import fitz
from google.cloud import vision
from PIL import Image

OUTPUT_DIR = "/home/jmknapp/cod/patrolReports"

# List of patrol report PDFs to process
PATROL_REPORTS = [
    "USS_Cod_1st_Patrol_Report.pdf",
    "USS_Cod_2nd_Patrol_Report.pdf",
    "USS_Cod_3rd_Patrol_Report.pdf",
    "USS_Cod_4th_Patrol_Report.pdf",
    "USS_Cod_5th_Patrol_Report.pdf",
    "USS_Cod_6th_Patrol_Report.pdf",
    "USS_Cod_7th_Patrol_Report.pdf",
]

def ocr_image_bytes(image_bytes):
    """Run Google Cloud Vision OCR on image bytes."""
    client = vision.ImageAnnotatorClient()
    image = vision.Image(content=image_bytes)
    response = client.document_text_detection(image=image)
    
    if response.error.message:
        raise Exception(response.error.message)
    
    full_text = response.full_text_annotation.text if response.full_text_annotation else ""
    
    words = []
    if response.full_text_annotation:
        for page in response.full_text_annotation.pages:
            for block in page.blocks:
                for paragraph in block.paragraphs:
                    for word in paragraph.words:
                        word_text = ''.join([s.text for s in word.symbols])
                        vertices = word.bounding_box.vertices
                        if len(vertices) >= 4:
                            x = min(v.x for v in vertices)
                            y = min(v.y for v in vertices)
                            y2 = max(v.y for v in vertices)
                            words.append({
                                'text': word_text,
                                'x': x, 'y': y, 'y2': y2,
                                'height': y2 - y
                            })
    
    return full_text, words

def process_pdf(source_pdf):
    """Process a single PDF with OCR."""
    base_name = os.path.splitext(os.path.basename(source_pdf))[0]
    
    print(f"\nProcessing: {source_pdf}")
    print("=" * 60)
    
    doc = fitz.open(source_pdf)
    num_pages = len(doc)
    print(f"Pages: {num_pages}")
    
    new_doc = fitz.open()
    ocr_texts = {}
    
    for page_num in range(num_pages):
        print(f"  Page {page_num + 1}/{num_pages}...", end=" ", flush=True)
        
        page = doc[page_num]
        
        # Render page at 1:1 (no scaling) - coordinates will match directly
        pix = page.get_pixmap()
        render_width = pix.width
        render_height = pix.height
        
        # Convert to bytes for OCR
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        img_bytes = io.BytesIO()
        img.save(img_bytes, format="PNG")
        img_bytes = img_bytes.getvalue()
        
        try:
            full_text, words = ocr_image_bytes(img_bytes)
            ocr_texts[str(page_num + 1)] = full_text
            print(f"({len(words)} words)")
            
            # Create new page at render size (matches OCR coordinates)
            new_page = new_doc.new_page(width=render_width, height=render_height)
            
            # Insert original page image
            new_page.insert_image(new_page.rect, pixmap=pix)
            
            # Add OCR text layer - no scaling needed since we rendered at 1:1
            for word_info in words:
                try:
                    x = word_info['x']
                    y = word_info['y2']  # Use bottom of bounding box for baseline
                    height = word_info['height']
                    fontsize = max(6, min(24, int(height * 0.8)))
                    
                    new_page.insert_text(
                        (x, y),
                        word_info['text'],
                        fontsize=fontsize,
                        render_mode=3  # Invisible
                    )
                except:
                    pass
                    
        except Exception as e:
            print(f"Error: {e}")
            ocr_texts[str(page_num + 1)] = ""
    
    doc.close()
    
    # Save OCR PDF
    output_pdf = os.path.join(OUTPUT_DIR, f"{base_name}_gv.pdf")
    new_doc.save(output_pdf, garbage=4, deflate=True)
    new_doc.close()
    print(f"\nSaved: {output_pdf}")
    
    # Check file size
    size_mb = os.path.getsize(output_pdf) / 1024 / 1024
    print(f"Size: {size_mb:.1f} MB")
    
    # Save OCR text JSON
    json_path = os.path.join(OUTPUT_DIR, f"{base_name}_gv_ocr.json")
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(ocr_texts, f, indent=2, ensure_ascii=False)
    print(f"Saved: {json_path}")

def main():
    # Process specific patrol or all
    if len(sys.argv) > 1:
        # Process specific patrol number(s)
        for arg in sys.argv[1:]:
            try:
                patrol_num = int(arg)
                if 1 <= patrol_num <= 7:
                    pdf_file = PATROL_REPORTS[patrol_num - 1]
                    source_pdf = os.path.join(OUTPUT_DIR, pdf_file)
                    if os.path.exists(source_pdf):
                        process_pdf(source_pdf)
                    else:
                        print(f"File not found: {source_pdf}")
                else:
                    print(f"Invalid patrol number: {patrol_num} (must be 1-7)")
            except ValueError:
                # Treat as filename
                source_pdf = os.path.join(OUTPUT_DIR, arg)
                if os.path.exists(source_pdf):
                    process_pdf(source_pdf)
                else:
                    print(f"File not found: {source_pdf}")
    else:
        # Process all patrol reports
        print("Processing all 7 patrol reports...")
        for pdf_file in PATROL_REPORTS:
            source_pdf = os.path.join(OUTPUT_DIR, pdf_file)
            if os.path.exists(source_pdf):
                process_pdf(source_pdf)
            else:
                print(f"File not found: {source_pdf}")

if __name__ == "__main__":
    main()

