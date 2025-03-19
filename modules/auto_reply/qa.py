from sentence_transformers import SentenceTransformer, util
import re
import discord

model = SentenceTransformer('all-mpnet-base-v2')

qa_groups = {
    # Heists related questions
    ("when is project 1 due", "what is the due date for the assignment", "when is the due date of project 1"):
        "Please check the LMS",
    
    # Game crash
    ("how do i join a group"):
        "Join a group at #1346793983141089306",
}

# Flatten qa_groups keys into a list of common questions and build an answers dictionary mapping each question to its answer
common_questions = []
answers = {}
for key, response in qa_groups.items():
    questions = key if isinstance(key, tuple) else (key,)
    for q in questions:
        common_questions.append(q)
        answers[q] = response

# Pre-compute embeddings for the common questions
common_embeddings = model.encode(common_questions)

def preprocess_message(text):
    # Remove Discord mentions and URLs
    text = re.sub(r'<@!?[0-9]+>', '', text).strip()
    text = re.sub(r'http\S+', '', text).strip()
    return text

def chunk_message(text, chunk_size=10, overlap=8):
    """
    Splits text into overlapping chunks.
    :param text: The input text.
    :param chunk_size: Maximum number of words per chunk.
    :param overlap: Number of words to overlap between chunks.
    :return: List of text chunks.
    """
    words = text.split()
    if len(words) <= chunk_size:
        return [text]
    chunks = []
    step = chunk_size - overlap
    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)
        if i + chunk_size >= len(words):
            break
    return chunks

def find_best_match(message: discord.Message, threshold):
    user = message.author
    content = message.content
    # Preprocess the new message
    cleaned_message = preprocess_message(content)
    if not cleaned_message:
        return None
    # Skip single-word messages
    if len(cleaned_message.split()) == 1:
        return None

    # Split the cleaned message into overlapping chunks
    chunks = chunk_message(cleaned_message)
    best_overall_score = -1
    best_response = None

    # For each chunk, compute its embedding and calculate cosine similarity against the precomputed common question embeddings
    for chunk in chunks:
        chunk_embedding = model.encode(chunk)
        cosine_scores = util.cos_sim(chunk_embedding, common_embeddings)[0]
        # Check if any similarity score in this chunk exceeds our threshold and beats previous scores
        for idx, score in enumerate(cosine_scores):
            if score > threshold and score > best_overall_score:
                best_overall_score = score
                best_response = answers[common_questions[idx]]
    
    # If the best response is callable, call it with the user to get the dynamic result.
    if callable(best_response):
        best_response = best_response(user)
    return best_response
