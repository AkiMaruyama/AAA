# import PyPDF2
# pdfFileObject = open('test.pdf', 'rb')
# pdfReader = PyPDF2.PdfFileReader(pdfFileObject)
# count = pdfReader.numPages
# for i in range(count):
#     page = pdfReader.getPage(i)
#     content = page.extractText().encode('utf8')
#     print(content)

with open('Supabarn.pdf', 'rb') as pdf:
	for each in pdf:
		print (each.gensalt())