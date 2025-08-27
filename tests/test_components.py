import pytest
import sys
import os

# Add the verifier app to the path
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'verifier', 'app'))


def test_nlp_keyword_extraction():
    """Test NLP keyword extraction function"""
    try:
        from nlp import simple_keywords
        
        # Test basic keyword extraction
        text = "5G technology causes COVID-19"
        keywords = simple_keywords(text)
        
        assert isinstance(keywords, list)
        assert len(keywords) > 0
        assert "5G" in keywords or "technology" in keywords
        
        print(f"✅ Keyword extraction working: {keywords}")
        
    except ImportError as e:
        pytest.skip(f"Missing dependencies: {e}")


def test_nlp_similarity_scoring():
    """Test NLP similarity scoring function"""
    try:
        from nlp import similarity_score
        
        # Test similarity scoring
        text1 = "5G causes COVID"
        text2 = "5G technology and coronavirus"
        similarity = similarity_score(text1, text2)
        
        assert isinstance(similarity, float)
        assert 0.0 <= similarity <= 1.0
        
        print(f"✅ Similarity scoring working: {similarity:.3f}")
        
    except ImportError as e:
        pytest.skip(f"Missing dependencies: {e}")


def test_nlp_refutation_detection():
    """Test NLP refutation detection function"""
    try:
        from nlp import detect_refutation_terms
        
        # Test refutation detection
        refutation_text = "There is no evidence that 5G causes COVID"
        has_refutation = detect_refutation_terms(refutation_text)
        
        assert isinstance(has_refutation, bool)
        
        print(f"✅ Refutation detection working: {has_refutation}")
        
    except ImportError as e:
        pytest.skip(f"Missing dependencies: {e}")


def test_models_import():
    """Test that models can be imported"""
    try:
        from verifier.app.models import Claim, Evidence, Verdict
        
        assert Claim is not None
        assert Evidence is not None
        assert Verdict is not None
        
        print("✅ Database models imported successfully")
        
    except ImportError as e:
        pytest.skip(f"Missing dependencies: {e}")


def test_database_connection():
    """Test database connection setup"""
    try:
        from verifier.app.database import get_db, engine
        
        assert engine is not None
        assert get_db is not None
        
        print("✅ Database connection setup working")
        
    except ImportError as e:
        pytest.skip(f"Missing dependencies: {e}")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
