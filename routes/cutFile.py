import PyPDF2
from fastapi import APIRouter, File, UploadFile
from difflib import get_close_matches as gcm
from itertools import chain
from os import listdir
from os.path import exists
from helpers.processText import processText as pT
FI = chain.from_iterable
indice = {}
hojas = []
control = 0
cF = APIRouter()

# 'document\TesisNotGenitoIndice.pdf'
@cF.get('/indice', response_model= dict, tags=['indice'])
def readFile(name: str):
    global control
    print(exists(f'./document/{name}'))
    pdfRead = PyPDF2.PdfFileReader(open(f'./document/{name}', 'rb'))
    for i in range(0, int(pdfRead.getNumPages()/10)):
        if(len(list(FI([gcm(x,pdfRead.getPage(i).extract_text().lower()[:20].split(' ')) for x in ['indice','contenido']])))): hojas.append(i)

    for i in range(1, len(hojas)):
        for hoja in range(hojas[i-1], hojas[i]): indice['Ip'+str(hoja)] = pT(pdfRead.getPage(hoja).extract_text())
    indice['Ip'+str(hojas[-1])] = pT(pdfRead.getPage(hojas[-1]).extract_text(), name)
    return indice

@cF.post('/indice', tags=['indice'])
async def createFile(file: UploadFile = File(...)):
    file_bytes = await file.read()
    with open(f'./document/{file.filename}', 'wb') as f:
        f.write(file_bytes)
    print(listdir('./document'))
    return readFile(file.filename)