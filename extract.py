import os
import pdfplumber

def extract_text_from_pdf(pdf_path):
    if not os.path.exists(pdf_path):
        print(f"file {pdf_path} doesn't exist!")
        return

    pdf_name = os.path.basename(pdf_path)
    txt_name = os.path.splitext(pdf_name)[0] + ".txt"

    # output folder
    output_folder = "extracted_text"
    os.makedirs(output_folder, exist_ok=True)
    txt_path = os.path.join(output_folder, txt_name)

    extracted_text = ""
    try:
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                extracted_text += page.extract_text() + "\n"
    except Exception as e:
        print(f"Error: {e}")
        return

    try:
        with open(txt_path, "w", encoding="utf-8") as txt_file:
            txt_file.write(extracted_text)
        print(f"File saved to: {txt_path}")
    except Exception as e:
        print(f"Error: {e}")

"""批量更新，输入初始数据所在文件夹:pdf_folder_path = 'original_pdf' """
def batch_extract_from_folder(folder_path):
    for filename in os.listdir(folder_path):
        if filename.endswith(".pdf"):
            pdf_file_path = os.path.join(folder_path, filename)
            extract_text_from_pdf(pdf_file_path)
    print('Finishing transforming')

# Specify the folder containing the PDF files
pdf_folder_path = "original_pdf"
batch_extract_from_folder(pdf_folder_path)


