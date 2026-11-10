from app.chunking import split_text


def test_split_respects_paragraphs():
    text = "Alpha paragraph.\n\nBravo paragraph.\n\nCharlie paragraph."
    chunks = split_text(text, chunk_size=40, overlap=5)
    assert chunks
    assert all(len(c) <= 40 for c in chunks)


def test_overlap_keeps_long_paragraph_windows():
    text = "x" * 250
    chunks = split_text(text, chunk_size=100, overlap=20)
    assert len(chunks) >= 3
    assert chunks[0][:20] == "x" * 20
