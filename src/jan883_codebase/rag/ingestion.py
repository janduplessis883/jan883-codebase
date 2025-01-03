CHUNK_SIZE = 300
CHUNK_OVERLAP = 0


def split_into_chunks(
    text: str, chunk_size: int = CHUNK_SIZE, chunk_overlap: int = CHUNK_OVERLAP
) -> List[str]:
    """Function to split the text into chunks of a maximum number of tokens
    ensure that the chunks are of size CHUNK_SIZE and overlap by chunk_overlap tokens
    use the `tokenizer.encode` method to tokenize the text
    """
    tokens = text.split()
    chunks = []
    start = 0
    while start < len(tokens):
        end = start + chunk_size
        chunk = tokens[start:end]
        chunks.append(" ".join(chunk))
        start = end - chunk_overlap
    return chunks
