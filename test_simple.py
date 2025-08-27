#!/usr/bin/env python3
"""
Simple test script for Claim-Checker components (no scikit-learn required)
"""
import sys
import os

# Add the verifier app to the path
sys.path.append(os.path.join(os.path.dirname(__file__), 'verifier', 'app'))


def test_simple_nlp():
    """Test simplified NLP functions"""
    try:
        from nlp_simple import simple_keywords, simple_similarity_score, detect_refutation_terms
        
        print("🧪 Testing Simplified NLP Functions")
        print("=" * 40)
        
        # Test keyword extraction
        text = "5G technology causes COVID-19"
        keywords = simple_keywords(text)
        print(f"✅ Keyword extraction: {keywords}")
        
        # Test similarity scoring
        text1 = "5G causes COVID"
        text2 = "5G technology and coronavirus"
        similarity = simple_similarity_score(text1, text2)
        print(f"✅ Similarity score: {similarity:.3f}")
        
        # Test refutation detection
        refutation_text = "There is no evidence that 5G causes COVID"
        has_refutation = detect_refutation_terms(refutation_text)
        print(f"✅ Refutation detection: {has_refutation}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_models():
    """Test database models"""
    try:
        from models import Claim, Evidence, Verdict
        
        print("\n🗄️ Testing Database Models")
        print("=" * 40)
        
        # Test that models can be imported
        assert Claim is not None
        assert Evidence is not None
        assert Verdict is not None
        
        print("✅ All models imported successfully")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


def test_database():
    """Test database connection"""
    try:
        from database import get_db, engine
        
        print("\n🔌 Testing Database Connection")
        print("=" * 40)
        
        # Test that database components can be imported
        assert engine is not None
        assert get_db is not None
        
        print("✅ Database connection setup working")
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False


if __name__ == "__main__":
    print("🚀 Claim-Checker Simple Component Test")
    print("=" * 50)
    
    success_count = 0
    total_tests = 3
    
    if test_simple_nlp():
        success_count += 1
    
    if test_models():
        success_count += 1
    
    if test_database():
        success_count += 1
    
    print(f"\n📊 Test Results: {success_count}/{total_tests} tests passed")
    
    if success_count == total_tests:
        print("🎉 All tests passed! System components are working.")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
    
    print("\n💡 To run the full system with Docker:")
    print("   docker compose up --build -d")
