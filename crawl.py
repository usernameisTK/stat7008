import os
import requests

def download_pdfs(pdf_urls, save_folder="downloads"):
    """
    Download multiple PDF files from the given URLs.
    
    Args:
        pdf_urls (list): A list of URLs pointing to the PDF files.
        save_folder (str): The folder to save the downloaded PDFs. Defaults to 'downloads'.
    """
    try:
        # Create folder if it doesn't exist
        if not os.path.exists(save_folder):
            os.makedirs(save_folder)

        for pdf_url in pdf_urls:
            try:
                # Fetch the PDF file
                response = requests.get(pdf_url)
                response.raise_for_status()  # Raise an error if the request failed

                # Extract PDF file name
                pdf_name = os.path.basename(pdf_url.split("?")[0])  # Handle query parameters

                # Ensure the file name ends with .pdf
                if not pdf_name.lower().endswith(".pdf"):
                    pdf_name += ".pdf"

                save_path = os.path.join(save_folder, pdf_name)

                # Save PDF
                with open(save_path, "wb") as f:
                    f.write(response.content)

                print(f"Downloaded: {pdf_name} -> {save_path}")
            except Exception as e:
                print(f"Failed to download {pdf_url}: {e}")

    except Exception as e:
        print(f"An error occurred: {e}")


if __name__ == "__main__":
    pdf_urls = [
        "https://www.constellationenergy.com/content/dam/constellationenergy/pdfs/Constellation-2024-Sustainability-Report.pdf",
        "https://www.responsibilityreports.com/HostedData/ResponsibilityReports/PDF/NYSE_ED_2023.pdf",
        "https://static.conocophillips.com/files/resources/conocophillips-2023-sustainability-report.pdf",
        "https://www.conagrabrands.com/citizenship-reports/conagra-brands-citizenship-report-2023",
        "https://update.comcast.com/wp-content/uploads/dlm_uploads/2024/06/Comcast-2024ImpactReport-Final-1.pdf"
    ]
    download_pdfs(pdf_urls)
