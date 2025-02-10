def processfile(request):
    if request.method == 'POST':
        uploaded_file = request.FILES['file']
        # Get the Content-Type header from the request
        content_type = request.headers.get('Content-Type', '')
        # Check if the file is a text file
        if not content_type.startswith('text/'):
            return "Only text files are allowed"
            
        # Proceed with processing...
        file_content = uploaded_file.read()

        
        