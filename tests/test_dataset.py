import os
import tempfile

from src.dataset import load_text, save_text, strip_headers


class TestLoadText:
    """Test the load_text function."""
    
    def test_load_text_basic(self):
        """Test loading text from a file."""
        test_content = "line1\nline2\nline3\n"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp.write(test_content)
            tmp_path = tmp.name
            
        try:
            result = load_text(tmp_path)
            expected = ["line1", "line2", "line3"]
            assert result == expected
            
        finally:
            os.unlink(tmp_path)
            
    def test_load_text_empty_file(self):
        """Test loading an empty file."""
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp_path = tmp.name
            
        try:
            result = load_text(tmp_path)
            assert result == []
            
        finally:
            os.unlink(tmp_path)
            
    def test_load_text_single_line(self):
        """Test loading a file with a single line."""
        test_content = "single line"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp.write(test_content)
            tmp_path = tmp.name
            
        try:
            result = load_text(tmp_path)
            assert result == ["single line"]
            
        finally:
            os.unlink(tmp_path)
            
    def test_load_text_unicode(self):
        """Test loading text with unicode characters."""
        test_content = "héllo wörld\nünicode tëst\n"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp.write(test_content)
            tmp_path = tmp.name
            
        try:
            result = load_text(tmp_path)
            expected = ["héllo wörld", "ünicode tëst"]
            assert result == expected
            
        finally:
            os.unlink(tmp_path)


class TestSaveText:
    """Test the save_text function."""
    
    def test_save_text_basic(self):
        """Test saving text to a file."""
        test_text = "Hello\nWorld\nTest"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp_path = tmp.name
            
        try:
            save_text(tmp_path, test_text)
            
            # Read back the content
            with open(tmp_path, 'r', encoding='utf-8') as f:
                result = f.read()
                
            assert result == test_text
            
        finally:
            os.unlink(tmp_path)
            
    def test_save_text_empty(self):
        """Test saving empty text."""
        test_text = ""
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp_path = tmp.name
            
        try:
            save_text(tmp_path, test_text)
            
            # Read back the content
            with open(tmp_path, 'r', encoding='utf-8') as f:
                result = f.read()
                
            assert result == test_text
            
        finally:
            os.unlink(tmp_path)
            
    def test_save_text_unicode(self):
        """Test saving text with unicode characters."""
        test_text = "héllo wörld\nünicode tëst"
        
        with tempfile.NamedTemporaryFile(mode='w', delete=False, encoding='utf-8') as tmp:
            tmp_path = tmp.name
            
        try:
            save_text(tmp_path, test_text)
            
            # Read back the content
            with open(tmp_path, 'r', encoding='utf-8') as f:
                result = f.read()
                
            assert result == test_text
            
        finally:
            os.unlink(tmp_path)


class TestStripHeaders:
    """Test the strip_headers function."""
    
    def test_strip_gutenberg_headers(self):
        """Test stripping Project Gutenberg headers and footers."""
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
        
    def test_strip_headers_no_gutenberg_markers(self):
        """Test behavior when no Gutenberg markers are present."""
        text_lines = [
            "Line 1",
            "Line 2", 
            "Line 3"
        ]
        
        result = strip_headers(text_lines)
        # Should return empty string when no markers found
        assert result == ""
        
    def test_strip_headers_only_start_marker(self):
        """Test behavior with only start marker."""
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
        
    def test_strip_headers_empty_content(self):
        """Test with empty content between markers."""
        text_lines = [
            "Header",
            "*** START OF PROJECT GUTENBERG EBOOK TITLE ***",
            "*** END OF PROJECT GUTENBERG EBOOK TITLE ***",
            "Footer"
        ]
        
        result = strip_headers(text_lines)
        assert result == ""
        
    def test_strip_headers_whitespace_only_content(self):
        """Test with whitespace-only content between markers."""
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
        # Should be stripped to empty string
        assert result == ""
        
    def test_strip_headers_multiple_gutenberg_references(self):
        """Test with multiple references to PROJECT GUTENBERG EBOOK."""
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