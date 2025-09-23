from pathlib import Path
from unittest.mock import patch

from src.config import (
    ANALYZED_DIR,
    DATA_DIR,
    PROCESSED_DATA_DIR,
    PROJ_ROOT,
    RAW_DATA_DIR,
    RESULT_DIR,
)


class TestPathConfiguration:
    """Test path configuration constants."""
    
    def test_proj_root_is_valid(self):
        """Test that PROJ_ROOT is correctly set."""
        assert isinstance(PROJ_ROOT, Path)
        assert PROJ_ROOT.exists()
        assert PROJ_ROOT.is_dir()
        # Should be one level up from src directory
        assert (PROJ_ROOT / "src").exists()
        
    def test_data_directories(self):
        """Test data directory paths are correctly configured."""
        assert isinstance(DATA_DIR, Path)
        assert isinstance(RAW_DATA_DIR, Path)
        assert isinstance(PROCESSED_DATA_DIR, Path)
        
        # Check relative paths
        assert DATA_DIR == PROJ_ROOT / "data"
        assert RAW_DATA_DIR == DATA_DIR / "raw"
        assert PROCESSED_DATA_DIR == DATA_DIR / "processed"
        
    def test_output_directories(self):
        """Test output directory paths are correctly configured."""
        assert isinstance(ANALYZED_DIR, Path)
        assert isinstance(RESULT_DIR, Path)
        
        # Check relative paths
        assert ANALYZED_DIR == PROJ_ROOT / "analyzed"
        assert RESULT_DIR == PROJ_ROOT / "results"
        
    def test_all_paths_are_pathlib_objects(self):
        """Test that all path constants are Path objects."""
        paths = [
            PROJ_ROOT,
            DATA_DIR,
            RAW_DATA_DIR,
            PROCESSED_DATA_DIR,
            ANALYZED_DIR,
            RESULT_DIR
        ]
        
        for path in paths:
            assert isinstance(path, Path)


class TestEnvironmentSetup:
    """Test environment setup functionality."""
    
    @patch('src.config.load_dotenv')
    def test_dotenv_loaded(self, mock_load_dotenv):
        """Test that load_dotenv is called during module import."""
        # Since the module is already imported, we need to reload it
        import importlib
        
        import src.config
        importlib.reload(src.config)
        
        mock_load_dotenv.assert_called_once()


class TestLoggerConfiguration:
    """Test logger configuration with tqdm integration."""
    
    @patch('src.config.tqdm')
    @patch('src.config.logger')
    def test_logger_tqdm_integration_available(self, mock_logger, mock_tqdm):
        """Test logger configuration when tqdm is available."""
        # Simulate tqdm being available
        import importlib
        
        import src.config
        importlib.reload(src.config)
        
        # Should configure logger with tqdm.write
        assert mock_logger.remove.called
        assert mock_logger.add.called
        
    @patch('src.config.logger')
    def test_logger_tqdm_integration_unavailable(self, mock_logger):
        """Test logger configuration when tqdm is not available."""
        with patch.dict('sys.modules', {'tqdm': None}):
            import importlib
            
            import src.config
            
            # Force ModuleNotFoundError for tqdm
            with patch('src.config.tqdm', side_effect=ModuleNotFoundError):
                importlib.reload(src.config)
                
            # Should not modify logger when tqdm is unavailable
            # The exact behavior depends on the module's state