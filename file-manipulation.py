from os import rename, listdir
from tkinter import filedialog as fd
from PyPDF2 import PdfReader
from shutil import move


def get_PDFs_names(files):
    PDFsList = []
    for file in files:
        # devuelve True si al final del string esta el ".pdf"
        if file.endswith('.pdf') == True:
            PDFsList.append(file)
    return PDFsList


downloadRoute = fd.askdirectory()
fileNames = listdir(downloadRoute)


# Cambia el nombre de los PDFs para que tengan el nombre del trabajador
for pdf_name in get_PDFs_names(fileNames):
    fullPath = f"{downloadRoute}/{pdf_name}"
    objectClassPdfReader = PdfReader(fullPath)
    objectClassPageObject = objectClassPdfReader.pages[0]
    text = objectClassPageObject.extract_text()
    wordList = text.split('\n')
    for index in range(len(wordList)):
        if wordList[index] == 'Sr.' or wordList[index] == 'Sra.':
            newName = wordList[index + 1].split()
            try:
                # Si '-' no esta en el string, entonces la persona tiene 3 nombres
                if newName[4].find('-') < 0:
                    rename(f'{downloadRoute}/{pdf_name}',
                           # Nuevo nombre
                           downloadRoute + '/' + newName[3].upper() + ' ' +
                           newName[4].upper() + ' ' + newName[0].upper() +
                           ' ' + newName[1].upper() + ' ' + newName[2].upper() + '.pdf')
                else:
                    rename(f'{downloadRoute}/{pdf_name}',
                           downloadRoute + '/' + newName[2].upper() + ' ' + newName[3].upper() +
                           ' ' + newName[0].upper() + ' ' + newName[1].upper() + '.pdf')
            except:
                rename(f'{downloadRoute}/{pdf_name}',
                       f'{downloadRoute}/{newName[1].upper()} {newName[2].upper()} {newName[0].upper()}.pdf')


# Envío de los PFDs a sus respectivas carpetas
variableWhile = True
# ¿Hay algún PDF en la lista?
while variableWhile:
    # Especificar la RUTA de destino (donde están las subcarpetas)
    destinationFolder = fd.askdirectory()
    # Reasigna todo lo que esta en downloadRoute (PDF tienen nuevo nombre)
    fileNames = listdir(downloadRoute)
    folders = listdir(destinationFolder)
    for newNamePdf in get_PDFs_names(fileNames):
        for folder in folders:
            # ¿El nombre menos los últimos 4 caracteres (.pdf) es igual la carpeta?
            if newNamePdf[:-4] == folder:
                # Mueve el archivo dentro de la carpeta del trabajador
                move(f'{downloadRoute}/{newNamePdf}',
                     f'{destinationFolder}/{folder}/LIQUIDACIONES')
                # Agrega la palabra LIQUIDACION  y la fecha al nombre del pdf.
                rename(f'{destinationFolder}/{folder}/LIQUIDACIONES/{newNamePdf}',
                       # El nombre queda: LIQUIDACION nombre (sin .pdf) fecha
                       destinationFolder + '/' + folder + '/LIQUIDACIONES/LIQUIDACION ' +
                       newNamePdf[:-4] + ' '+wordList[6].lstrip() + '.pdf')
    fileNames = listdir(downloadRoute)
    if not get_PDFs_names(fileNames):
        variableWhile = False
