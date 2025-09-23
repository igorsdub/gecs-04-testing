
import os
import tempfile
import pytest
from src.dataset import load_text, save_text, strip_headers



# ------------------- Fixtures -------------------

@pytest.fixture
def tmp_text_file(tmp_path):
    def _make_file(content):
        file_path = tmp_path / "test.txt"
        file_path.write_text(content, encoding="utf-8")
        return str(file_path)
    return _make_file

# ------------------- Tests -------------------

def test_load_text_basic(tmp_text_file):
    test_content = "line1\nline2\nline3\n"
    file_path = tmp_text_file(test_content)
    result = load_text(file_path)
    expected = ["line1", "line2", "line3"]
    assert result == expected

def test_load_text_empty_file(tmp_text_file):
    file_path = tmp_text_file("")
    result = load_text(file_path)
    assert result == []

def test_load_text_single_line(tmp_text_file):
    file_path = tmp_text_file("single line")
    result = load_text(file_path)
    assert result == ["single line"]

def test_load_text_unicode(tmp_text_file):
    test_content = "héllo wörld\nünicode tëst\n"
    file_path = tmp_text_file(test_content)
    result = load_text(file_path)
    expected = ["héllo wörld", "ünicode tëst"]
    assert result == expected



def test_save_text_basic(tmp_path):
    test_text = "Hello\nWorld\nTest"
    file_path = tmp_path / "out.txt"
    save_text(str(file_path), test_text)
    result = file_path.read_text(encoding="utf-8")
    assert result == test_text

def test_save_text_empty(tmp_path):
    test_text = ""
    file_path = tmp_path / "out.txt"
    save_text(str(file_path), test_text)
    result = file_path.read_text(encoding="utf-8")
    assert result == test_text

def test_save_text_unicode(tmp_path):
    test_text = "héllo wörld\nünicode tëst"
    file_path = tmp_path / "out.txt"
    save_text(str(file_path), test_text)
    result = file_path.read_text(encoding="utf-8")
    assert result == test_text



def test_strip_gutenberg_headers():
    text_lines = [
        "Some header text",
        "*** START OF PROJECT GUTENBERG EBOOK TITLE ***",
        "Title: Book Title",
        "Author: Book Author", 
        "",
        "Chapter 1",
        "This is the actual content",
        "More content here",
        "",
        "Chapter 2", 
        "Even more content",
        "*** END OF PROJECT GUTENBERG EBOOK TITLE ***",
        "Some footer text"
    ]
    result = strip_headers(text_lines)
    expected = "Title: Book Title\nAuthor: Book Author\n\nChapter 1\nThis is the actual content\nMore content here\n\nChapter 2\nEven more content"
    assert result == expected

def test_strip_headers_no_gutenberg_markers():
    text_lines = ["Line 1", "Line 2", "Line 3"]
    result = strip_headers(text_lines)
    assert result == ""

def test_strip_headers_only_start_marker():
    text_lines = [
        "Header text",
        "*** START OF PROJECT GUTENBERG EBOOK TITLE ***",
        "Content line 1",
        "Content line 2",
        "No end marker"
    ]
    result = strip_headers(text_lines)
    expected = "Content line 1\nContent line 2\nNo end marker"
    assert result == expected

def test_strip_headers_empty_content():
    text_lines = [
        "Header",
        "*** START OF PROJECT GUTENBERG EBOOK TITLE ***",
        "*** END OF PROJECT GUTENBERG EBOOK TITLE ***",
        "Footer"
    ]
    result = strip_headers(text_lines)
    assert result == ""

def test_strip_headers_whitespace_only_content():
    text_lines = [
        "Header",
        "*** START OF PROJECT GUTENBERG EBOOK TITLE ***",
        "   ",
        "\t",
        "",
        "*** END OF PROJECT GUTENBERG EBOOK TITLE ***",
        "Footer"
    ]
    result = strip_headers(text_lines)
    assert result == ""

def test_strip_headers_multiple_gutenberg_references():
    text_lines = [
        "Header",
        "*** START OF PROJECT GUTENBERG EBOOK ALICE ***",
        "Content 1",
        "Content 2",
        "*** END OF PROJECT GUTENBERG EBOOK ALICE ***",
        "Footer"
    ]
    result = strip_headers(text_lines)
    expected = "Content 1\nContent 2"
    assert result == expected