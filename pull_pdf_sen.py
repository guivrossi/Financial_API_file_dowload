import csv, json, zipfile
import requests, PyPDF2, fitz
import os


years = list(range(2018,2022))
cwd = os.getcwd() + '/Trade_strategy'

for year in years:
    zip_file_url = f'https://disclosures-clerk.house.gov/public_disc/financial-pdfs/{year}FD.ZIP'
    pdf_file_url = f'https://disclosures-clerk.house.gov/public_disc/ptr-pdfs/{year}/'

    file_path = f'{year}_ZIP_Folder'
    r = requests.get(zip_file_url)
    foldername = os.path.join(cwd, file_path)   
    
    while not os.path.exists(foldername):
        os.mkdir(foldername)
    
    zip_file_name = os.path.join(foldername , f'{year}.zip')
    text_file_name = f'Trade_strategy\{year}_ZIP_Folder\{year}FD.txt'

    with open(zip_file_name, 'wb') as f:
        f.write(r.content)

    with zipfile.ZipFile(zip_file_name) as z:
        z.extractall(foldername)

    with open(text_file_name) as f:
        for line in csv.reader(f, delimiter ='\t'):
            if line[1] == 'Pelosi': # Last name of person to search
                date = line[7]
                doc_id = line[8]
            
                r = requests.get(f"{pdf_file_url}{doc_id}.pdf")
                
                # CREATING PDF FOLDER
                pdf_folder_name = 'PDF_Folder'
                pdf_file_path = os.path.join(foldername , pdf_folder_name)

                while not os.path.exists(pdf_file_path):
                    os.mkdir(pdf_file_path)
                # DOWNLOAD EACH PDF ON THEIR FOLDERS
                pdf_file_name = os.path.join(pdf_file_path , f'{doc_id}.pdf')

                with open(pdf_file_name, 'wb') as pdf_file:
                    pdf_file.write(r.content)

                # doc = fitz.open(pdf_file_name)
                # # page = doc.load_page(page_id = 0)
 
                # print(pdf_file_name)