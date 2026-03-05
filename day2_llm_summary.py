from transformers import pipeline

summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

text = """
Artificial Intelligence is transforming industries by automating tasks,
improving decision-making, and enabling new innovations.
Companies are investing heavily in AI research and development.
"""

result = summarizer(text, max_length=60)

print("Summary:")
print(result[0]["summary_text"])