import os
import requests
from pathlib import Path

# Configuration
UPLOAD_DIR = r"D:\GOKUL-UG\VIT\Projects\AI\Uploadocs"
API_ENDPOINT = "http://localhost:8000/api/upload-pdf"

def upload_all_pdfs():
    """Upload all PDFs from directory to ChromaDB"""
    
    # Get all PDF files
    pdf_files = list(Path(UPLOAD_DIR).glob("*.pdf"))
    
    if not pdf_files:
        print(f"❌ No PDF files found in {UPLOAD_DIR}")
        return
    
    print(f"📄 Found {len(pdf_files)} PDF files\n")
    
    success_count = 0
    failed_count = 0
    
    # Upload each PDF
    for pdf_file in pdf_files:
        try:
            print(f"⏳ Uploading: {pdf_file.name}")
            
            with open(pdf_file, 'rb') as f:
                files = {'file': f}
                response = requests.post(API_ENDPOINT, files=files, timeout=60)
            
            if response.status_code == 200:
                print(f"✅ Success: {pdf_file.name}")
                success_count += 1
            else:
                print(f"❌ Failed: {pdf_file.name} (Status: {response.status_code})")
                failed_count += 1
                
        except Exception as e:
            print(f"❌ Error uploading {pdf_file.name}: {str(e)}")
            failed_count += 1
    
    # Summary
    print(f"\n{'='*50}")
    print(f"✅ Successful: {success_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"{'='*50}")

if __name__ == "__main__":
    upload_all_pdfs()
