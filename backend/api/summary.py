import magic


def processfile(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(uploaded_file.read(2048),mime=True)
        text = totext(file_type)
        
        
        # Proceed with processing...

def totext(file_type):
    if file_type == 'text/plain':
            pass
    elif file_type == 'application/pdf':
            pass
    elif file_type == 'application/vnd.openxmlformats-officedocument.wordprocessingml.document':
            pass
    else:
          pass