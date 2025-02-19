from transformers import pipeline


summarizer = pipeline("summarization", model="facebook/bart-large-cnn")


def summarize(text):
    try:
        ARTICLE = text
        response = summarizer(ARTICLE, max_length=600, min_length=50, do_sample=False)
        return response
    except Exception as e:
        raise ValueError(f"Failed to create summary: {e}")
