import os
import re
from PyPDF2 import PdfReader, PdfWriter
from PyPDF2.errors import PdfReadError
from reportlab.lib.pagesizes import A4

def get_user_input():
    curriculum_options = ["Cambridge", "Edexcel"]
    level_options = ["Olevel", "AS", "A2"]
    subject_options = ["Math", "Physics", "Chemistry", "Biology", "ICT", "Business", "Arabic", "English", "French"]
    period_options = ["Feb", "May", "Oct"]
    
    while True:
        curriculum = input("What curriculum do you need (Cambridge or Edexcel): ")
        if curriculum in curriculum_options:
            break
        print("Invalid input. Please enter 'Cambridge' or 'Edexcel'.")

    while True:
        level = input("What level (Olevel, AS, A2): ")
        if level in level_options:
            break
        print("Invalid input. Please enter 'Olevel', 'AS', or 'A2'.")

    while True:
        subject = input("What subject (Math, Physics, Chemistry, Biology, ICT, Business, Arabic, English, French): ")
        if subject in subject_options:
            break
        print("Invalid input. Please enter a valid subject from the list provided.")

    while True:
        start_year = input("Starting Year (Earliest is 2016): ")
        if re.match(r"^\d{4}$", start_year) and int(start_year) >= 2016:
            start_year = int(start_year)
            break
        print("Invalid input. Please enter a valid year (2016 or later).")

    while True:
        start_period = input("Starting Period (Feb, May, Oct): ")
        if start_period in period_options:
            break
        print("Invalid input. Please enter 'Feb', 'May', or 'Oct'.")

    while True:
        end_year = input("Ending Year: ")
        if re.match(r"^\d{4}$", end_year) and int(end_year) >= start_year:
            end_year = int(end_year)
            break
        print(f"Invalid input. Please enter a valid year (greater than or equal to {start_year}).")

    while True:
        end_period = input("Ending Period (Feb, May, Oct): ")
        if end_period in period_options:
            break
        print("Invalid input. Please enter 'Feb', 'May', or 'Oct'.")

    return curriculum, level, subject, start_year, start_period, end_year, end_period

def find_pdfs(curriculum, level, subject, start_year, start_period, end_year, end_period):
    base_dir = "./pdfs"
    papers = []
    answers = []

    periods = {"Feb": 1, "May": 2, "Oct": 3}

    for year in range(start_year, end_year + 1):
        for period in ["Feb", "May", "Oct"]:
            if (year == start_year and periods[period] < periods[start_period]) or \
               (year == end_year and periods[period] > periods[end_period]):
                continue

            paper_path = os.path.join(base_dir, curriculum, level, subject, f"{year}_{period}_paper.pdf")
            answer_path = os.path.join(base_dir, curriculum, level, subject, f"{year}_{period}_answers.pdf")

            if os.path.exists(paper_path):
                papers.append(paper_path)
            if os.path.exists(answer_path):
                answers.append(answer_path)

    return papers, answers

def merge_pdfs(pdf_paths, output_path):
    writer = PdfWriter()

    for pdf_path in pdf_paths:
        reader = PdfReader(pdf_path)
        if reader.is_encrypted:
            try:
                reader.decrypt('')
            except PdfReadError:
                print(f"Could not decrypt {pdf_path}")
                continue
        for page in reader.pages:
            writer.add_page(page)

    with open(output_path, 'wb') as out:
        writer.write(out)

def scale_pdf_to_a4(input_path, output_path):
    reader = PdfReader(input_path)
    writer = PdfWriter()

    for page in reader.pages:
        page.scale_to(A4[0], A4[1])
        writer.add_page(page)

    with open(output_path, 'wb') as out:
        writer.write(out)

def main():
    curriculum, level, subject, start_year, start_period, end_year, end_period = get_user_input()

    paper_paths, answer_paths = find_pdfs(curriculum, level, subject, start_year, start_period, end_year, end_period)

    if not paper_paths:
        print("No exam booklets found for the specified criteria.")
        return

    if not answer_paths:
        print("No answer booklets found for the specified criteria.")
        return

    merged_paper_path = "./merged_exam_booklets.pdf"
    merged_answer_path = "./merged_answer_booklets.pdf"
    final_paper_path = "./scaled_exam_booklets.pdf"
    final_answer_path = "./scaled_answer_booklets.pdf"

    merge_pdfs(paper_paths, merged_paper_path)
    merge_pdfs(answer_paths, merged_answer_path)

    scale_pdf_to_a4(merged_paper_path, final_paper_path)
    scale_pdf_to_a4(merged_answer_path, final_answer_path)

    # Delete intermediate merged files
    os.remove(merged_paper_path)
    os.remove(merged_answer_path)

    print("Merged and scaled PDFs have been created successfully.")

if __name__ == "__main__":
    main()
