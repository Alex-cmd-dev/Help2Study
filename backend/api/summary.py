import magic
import PyPDF2


def processfile(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(uploaded_file.read(2048),mime=True)
        text = toText(file_type)

def toText(file_type):
    if file_type == 'text/plain':
            pass
    elif file_type == 'application/pdf':
            pass
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            pass
    else:
          pass






def pdf_to_text(pdf_path):
    try:
          with open(pdf_path, 'rb') as pdf_file:
               pdf_reader = PyPDF2.PdfReader(pdf_file)
               text = ''
               for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text
    except Exception as e:
       return {'message': f'Error opening file type: {e}'}
    return text
    
def txt_to_text(txt_path):
    

         
               
        
         
    

