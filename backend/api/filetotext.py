import magic
import docx2txt



def processfile(uploaded_file):
    mime = magic.Magic(mime=True)
    file_type = mime.from_buffer(uploaded_file.read(4096), mime=True)
    try:
        text = toText(file_type, uploaded_file)
        return summary
    except Exception as e:
        raise ValueError(f"Failed to process file: {str(e)}")


def toText(file_type, file):
    try:
        if (
            file_type
            == "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        ):
            return docx_to_text(file)
        else:
            raise Exception(f"Unsupported file type: {file_type}")
    except Exception as e:
        raise ValueError(f"Something went wrong: {str(e)}")

def docx_to_text(docx):
    try:
        text = docx2txt.process(f"{docx}")
        return text
    except Exception as e:
        raise ValueError(f"Failed to read docx file: {str(e)}")
