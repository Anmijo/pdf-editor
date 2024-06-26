from PyPDF2 import PdfReader, PdfWriter
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.lib.units import inch
import io

def add_text_to_pdf(input_pdf_path, output_pdf_path, text):
    # Read the input PDF
    reader = PdfReader(input_pdf_path)
    writer = PdfWriter()

    # Create a PDF with ReportLab
    packet = io.BytesIO()
    can = canvas.Canvas(packet, pagesize=letter)
    can.setFont("Helvetica-Bold", 50)
    
    # Calculate position to center the text
    width, height = letter
    text_width = can.stringWidth(text, "Helvetica-Bold", 50)
    x = (width - text_width) / 2
    y = height / 2
    
    can.drawString(x, y, text)
    can.save()

    # Move to the beginning of the StringIO buffer
    packet.seek(0)
    
    # Read the new PDF
    new_pdf = PdfReader(packet)

    # Get the first page of the existing PDF
    page = reader.pages[0]

    # Merge the new PDF with the existing page
    page.merge_page(new_pdf.pages[0])
    
    # Add the modified page to the writer
    writer.add_page(page)

    # Add the remaining pages
    for i in range(1, len(reader.pages)):
        writer.add_page(reader.pages[i])

    # Write the output PDF
    with open(output_pdf_path, "wb") as output_file:
        writer.write(output_file)

# Example usage
input_pdf_path = "input.pdf"
output_pdf_path = "output.pdf"
text = "Chemistry"
add_text_to_pdf(input_pdf_path, output_pdf_path, text)
