#!/usr/bin/env python3
"""
Simple local test script to verify the Claim-Checker system components
"""
import asyncio
import httpx
import json
from typing import Dict, Any


async def test_services():
    """Test the services if they're running locally"""
    
    # Test gateway health
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8080/health")
            if response.status_code == 200:
                print("✅ Gateway service is running")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Gateway service returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Gateway service not accessible: {e}")
    
    # Test evidence service health
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.get("http://localhost:8000/health")
            if response.status_code == 200:
                print("✅ Evidence service is running")
                print(f"   Response: {response.json()}")
            else:
                print(f"❌ Evidence service returned status {response.status_code}")
    except Exception as e:
        print(f"❌ Evidence service not accessible: {e}")
    
    # Test authentication
    try:
        async with httpx.AsyncClient(timeout=10.0) as client:
            login_data = {
                "email": "test@example.com",
                "password": "password123"
            }
            response = await client.post(
                "http://localhost:8080/auth/login",
                json=login_data
            )
            if response.status_code == 200:
                print("✅ Authentication endpoint working")
                token_data = response.json()
                print(f"   Token type: {token_data.get('token_type')}")
            else:
                print(f"❌ Authentication failed with status {response.status_code}")
    except Exception as e:
        print(f"❌ Authentication test failed: {e}")


def test_nlp_functions():
    """Test NLP functions directly"""
    try:
        # Import NLP functions
        import sys
        import os
        sys.path.append(os.path.join(os.path.dirname(__file__), 'verifier', 'app'))
        
        from nlp import simple_keywords, similarity_score, detect_refutation_terms
        
        # Test keyword extraction
        text = "5G technology causes COVID-19"
        keywords = simple_keywords(text)
        print(f"✅ Keyword extraction working")
        print(f"   Input: '{text}'")
        print(f"   Keywords: {keywords}")
        
        # Test similarity scoring
        text1 = "5G causes COVID"
        text2 = "5G technology and coronavirus"
        similarity = similarity_score(text1, text2)
        print(f"✅ Similarity scoring working")
        print(f"   Similarity between '{text1}' and '{text2}': {similarity:.3f}")
        
        # Test refutation detection
        refutation_text = "There is no evidence that 5G causes COVID"
        has_refutation = detect_refutation_terms(refutation_text)
        print(f"✅ Refutation detection working")
        print(f"   Text: '{refutation_text}'")
        print(f"   Has refutation terms: {has_refutation}")
        
    except ImportError as e:
        print(f"❌ Missing dependencies: {e}")
        print("   Install with: pip install scikit-learn numpy")
    except Exception as e:
        print(f"❌ NLP functions test failed: {e}")


if __name__ == "__main__":
    print("🧪 Testing Claim-Checker System Components")
    print("=" * 50)
    
    # Test NLP functions
    print("\n📝 Testing NLP Functions:")
    test_nlp_functions()
    
    # Test services
    print("\n🌐 Testing Services:")
    asyncio.run(test_services())
    
    print("\n✨ Test completed!")
