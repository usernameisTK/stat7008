import os
import requests

def download_pdf(pdf_url, save_folder="downloads"):
    """
    Download a PDF file from the given URL.
    
    Args:
        pdf_url (str): The URL of the PDF file.
        save_folder (str): The folder to save the downloaded PDF. Defaults to 'downloads'.
    """
    try:
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        response = requests.get(pdf_url)
        response.raise_for_status() 

        pdf_name = os.path.basename(pdf_url.split("?")[0])  
        save_path = os.path.join(save_folder, pdf_name)

        with open(save_path, "wb") as f:
            f.write(response.content)

        print(f"Downloaded: {pdf_name} -> {save_path}")

    except Exception as e:
        print(f"An error occurred: {e}")

# Example usage
if __name__ == "__main__":
    # Replace with your PDF URL
    pdf_url = "https://www.constellationenergy.com/content/dam/constellationenergy/pdfs/Constellation-2024-Sustainability-Report.pdf"
    download_pdf(pdf_url)
