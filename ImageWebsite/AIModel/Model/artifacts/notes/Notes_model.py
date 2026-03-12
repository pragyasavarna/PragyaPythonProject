import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
import os
import nltk
torch.set_num_threads(os.cpu_count())
torch.set_num_interop_threads(1)

# -------------------------------
# Download punkt tokenizer once
# -------------------------------

try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt')

try:
    nltk.data.find('tokenizers/punkt_tab')
except LookupError:
    nltk.download('punkt_tab')

# -------------------------------
# Paths
# -------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MODEL_PATH = os.path.join(BASE_DIR, "notes")

# -------------------------------
# Device configuration
# -------------------------------
device = "cuda" if torch.cuda.is_available() else "cpu"

# Disable gradients globally (saves memory)
torch.set_grad_enabled(False)

# -------------------------------
# LOAD MODELS ONCE AT SERVER START
# -------------------------------
print("Loading summarization model...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, use_fast=True)

model = AutoModelForSeq2SeqLM.from_pretrained(
    MODEL_PATH,
    torch_dtype=torch.float32,
    low_cpu_mem_usage=True
).to(device)

model.eval()

print("Summarization model loaded.")

# -------------------------------
# LIGHTWEIGHT EMBEDDING MODEL
# -------------------------------
print("Loading keyword model...")

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

kw_model = KeyBERT(embedding_model)

print("Keyword model loaded.")

# -------------------------------
# TEXT CLEANING
# -------------------------------
def clean_text(text):

    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'import .*?;', '', text)
    text = re.sub(r'\s+', ' ', text)

    return text.strip()


# -------------------------------
# SPLIT TEXT INTO CHUNKS
# -------------------------------
def split_text(text, max_tokens=600):

    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        token_len = len(
            tokenizer.tokenize(current_chunk + sentence)
        )

        if token_len < max_tokens:
            current_chunk += sentence + " "
        else:
            chunks.append(current_chunk.strip())
            current_chunk = sentence + " "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


# -------------------------------
# SUMMARIZE SINGLE CHUNK
# -------------------------------
def summarize_chunk(chunk):

    inputs = tokenizer(
        chunk,
        return_tensors="pt",
        truncation=True,
        max_length=800
    ).to(device)
    with torch.no_grad():
        summary_ids = model.generate(
            inputs["input_ids"],
            max_length=80,
            min_length=40,
            num_beams=3,
            length_penalty=1.1,
            no_repeat_ngram_size=3,
            early_stopping=True
        )

    summary = tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True,
        clean_up_tokenization_spaces=True
    )
    summary = re.sub(r'\s+', ' ', summary).strip()
    return summary


# -------------------------------
# MAIN SUMMARIZATION FUNCTION
# -------------------------------
def summarize_notes(text):

    text = clean_text(text)


    summaries = []
    sections = [s for s in split_text(text) if len(s.split()) >= 40]

    for section in sections:

        summaries.append(summarize_chunk(section))

    return " ".join(summaries)


# -------------------------------
# BULLET SUMMARY
# -------------------------------
def bullet_summary(summary):

    sentences = sent_tokenize(summary)

    bullets = ["• " + s for s in sentences]

    return "\n".join(bullets)


# -------------------------------
# KEYWORD EXTRACTION
# -------------------------------
def extract_keywords(text):

    try:

        keywords = kw_model.extract_keywords(
            text,
            keyphrase_ngram_range=(1, 3),
            stop_words="english",
            top_n=10
        )

        return [k[0] for k in keywords]

    except:
        return []