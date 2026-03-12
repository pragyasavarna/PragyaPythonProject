import re
import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from nltk.tokenize import sent_tokenize
from sentence_transformers import SentenceTransformer
from keybert import KeyBERT
import os
import nltk

# -------------------------------
# Download punkt tokenizer once
# -------------------------------
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

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

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)

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
def split_text(text, max_tokens=900):

    sentences = sent_tokenize(text)

    chunks = []
    current_chunk = ""

    for sentence in sentences:

        token_len = len(
            tokenizer.encode(current_chunk + sentence, add_special_tokens=False)
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
        max_length=1024
    ).to(device)

    summary_ids = model.generate(
        inputs["input_ids"],
        max_length=200,
        min_length=80,
        num_beams=6,
        length_penalty=1.2,
        no_repeat_ngram_size=3,
        early_stopping=True
    )

    return tokenizer.decode(summary_ids[0], skip_special_tokens=True)


# -------------------------------
# MAIN SUMMARIZATION FUNCTION
# -------------------------------
def summarize_notes(text):

    text = clean_text(text)

    sections = split_text(text)

    summaries = []

    for section in sections:

        if len(section.split()) < 40:
            continue

        summaries.append(summarize_chunk(section))

    return " ".join(summaries)


# -------------------------------
# BULLET SUMMARY
# -------------------------------
def bullet_summary(text):

    summary = summarize_notes(text)

    sentences = sent_tokenize(summary)

    bullets = ["• " + s for s in sentences]

    return "\n".join(bullets)


# -------------------------------
# KEYWORD EXTRACTION
# -------------------------------
def extract_keywords(text):

    keywords = kw_model.extract_keywords(
        text,
        keyphrase_ngram_range=(1, 3),
        stop_words="english",
        top_n=10
    )

    return [k[0] for k in keywords]