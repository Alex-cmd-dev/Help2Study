def processfile(request):
    if request.method == 'POST':
            uploaded_file = request.FILES['file']
            file_content = uploaded_file.read()
