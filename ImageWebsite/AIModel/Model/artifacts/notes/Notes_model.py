import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
import os
import nltk

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(BASE_DIR, "notes")

device = "cuda" if torch.cuda.is_available() else "cpu"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_PATH).to(device)
model.eval()

embedding_model = SentenceTransformer("all-mpnet-base-v2")
kw_model = KeyBERT(model=embedding_model)


def clean_text(text):

    # remove code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # remove java code lines
    text = re.sub(r'import .*?;', '', text)

    # remove extra spaces
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


def split_text(text, max_tokens=1000):

    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        if len(tokenizer.encode(current_chunk + sentence, add_special_tokens=False)) < max_tokens:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def summarize_chunk(chunk):

    inputs = tokenizer(
        chunk,
        return_tensors="pt",
        truncation=True,
        max_length=1024
    ).to(device)
    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=200,
            min_length=80,
            num_beams=8,
            length_penalty=1.2,
            no_repeat_ngram_size=3,
            early_stopping=True
        )

    summary = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )

    return summary


def summarize_notes(text):

    text = clean_text(text)

    # split by headings or numbered sections
    sections = split_text(text)

    summaries = []

    for section in sections:    

        if len(section.split()) < 40:
            continue

        inputs = tokenizer(
            section,
            return_tensors="pt",
            truncation=True,
            max_length=1024
        ).to(device)
        
        with torch.no_grad():
            summary_ids = model.generate(
                inputs["input_ids"],
                max_length=120,
                min_length=40,
                num_beams=6,
                no_repeat_ngram_size=3
            )

        summary = tokenizer.decode(
            summary_ids[0],
            skip_special_tokens=True
        )

        summaries.append(summary)

    final_summary = " ".join(summaries)

    return final_summary


def bullet_summary(text):

    summary = summarize_notes(text)

    sentences = sent_tokenize(summary)

    bullets = []

    for s in sentences:

        bullets.append("• " + s)

    return "\n".join(bullets)


def extract_keywords(text):

    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1,3),
        stop_words="english",
        top_n=10
    )

    return [k[0] for k in keywords]
