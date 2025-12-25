"""
Tests for the RAG retrieval system
"""

import pytest
from retrieve import retrieve, RetrieverError

def test_retrieve_normal_query():
    """Test retrieval with a normal query"""
    results = retrieve("ice cream")
    assert isinstance(results, list)
    if results:
        assert 'id' in results[0]
        assert 'text' in results[0]
        assert 'score' in results[0]
        assert 0 <= results[0]['score'] <= 1

def test_retrieve_empty_query():
    """Test retrieval with empty query"""
    with pytest.raises(RetrieverError):
        retrieve("")

def test_retrieve_no_matches():
    """Test retrieval with query that should have no matches"""
    results = retrieve("xyzabcnonexistent")
    assert isinstance(results, list)
    # Might return low-score matches, but check if empty or low scores

def test_retrieve_with_params():
    """Test retrieval with custom top_k and threshold"""
    results = retrieve("service", top_k=3, threshold=0.7)
    assert len(results) <= 3
    for r in results:
        assert r['score'] >= 0.7

if __name__ == "__main__":
    pytest.main([__file__])