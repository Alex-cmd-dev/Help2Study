from . import gemini
import magic
import PyPDF2
import docx2txt


def summarize():
    pass


def processfile(request):
    if request.method == "POST":
        uploaded_file = request.FILES["file"]
        mime = magic.Magic(mime=True)
        file_type = mime.from_buffer(uploaded_file.read(4096), mime=True)
        try:
            text = toText(file_type, uploaded_file)
        except Exception as e:
            return {"message": f"Error : {e}"}


def toText(file_type, file):
    try:
        if file_type == "text/plain":
            return txt_to_text(file)

        elif file_type == "application/pdf":
            return pdf_to_text(file)
        elif (
            file_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            return docx_to_text(file)
    except Exception as e:
        return {"message": f"Invalid file type : {e}"}


def pdf_to_text(pdf):
    try:
        with open(pdf, "rb") as pdf_file:
            pdf_reader = PyPDF2.PdfReader(pdf_file)
            text = ""
            for page_num in range(len(pdf_reader.pages)):
                page = pdf_reader.pages[page_num]
                text += page.extract_text
            return text
    except Exception as e:
        raise ValueError(f"Failed to read pdf file: {e}")


def txt_to_text(txt):
    try:
        with open(txt, "r", encoding="utf-8") as file:
            return file.read()
    except Exception as e:
        raise ValueError(f"Failed to read txt file: {e}")


def docx_to_text(docx):
    try:
        text = docx2txt.process(f"{docx}")
        return text
    except Exception as e:
        raise ValueError(f"Failed to read docx file: {e}")
