#!/usr/bin/env python3
"""
Script di test per gli endpoints del Social Media Automation System
Testa tutti i principali endpoint API per verificare che funzionino correttamente.
"""

import requests
import json
from datetime import datetime, timedelta

# URL base del servizio (cambiare se necessario)
BASE_URL = "https://social-automation-latest.onrender.com"
# BASE_URL = "http://localhost:8000"  # Per test locali

def test_health_check():
    """Test dell'endpoint di health check"""
    print("🔍 Testing Health Check...")
    try:
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health Check: OK")
            print(f"   Response: {response.json()}")
        else:
            print(f"❌ Health Check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health Check error: {e}")

def test_templates_api():
    """Test dell'API Templates"""
    print("\n🔍 Testing Templates API...")
    
    # Test GET templates (lista vuota inizialmente)
    try:
        response = requests.get(f"{BASE_URL}/templates/")
        print(f"   GET /templates: {response.status_code}")
        if response.status_code == 200:
            templates = response.json()
            print(f"   Templates found: {len(templates)}")
        else:
            print(f"   Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Templates API error: {e}")

def test_content_api():
    """Test dell'API Content/Scheduling"""
    print("\n🔍 Testing Content API...")
    
    try:
        response = requests.get(f"{BASE_URL}/content/1")  # Test get posts for account 1
        print(f"   GET /content/1: {response.status_code}")
        if response.status_code != 404:  # 404 è normale se non ci sono account
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Content API error: {e}")

def test_analytics_api():
    """Test dell'API Analytics"""
    print("\n🔍 Testing Analytics API...")
    
    try:
        response = requests.get(f"{BASE_URL}/analytics/1/summary")  # Account 1 summary
        print(f"   GET /analytics/1/summary: {response.status_code}")
        if response.status_code != 404:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Analytics API error: {e}")

def test_engagement_api():
    """Test dell'API Engagement"""
    print("\n🔍 Testing Engagement API...")
    
    try:
        response = requests.get(f"{BASE_URL}/engagement/1")  # Engagement for post 1
        print(f"   GET /engagement/1: {response.status_code}")
        if response.status_code != 404:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Engagement API error: {e}")

def test_hashtags_api():
    """Test dell'API Hashtags"""
    print("\n🔍 Testing Hashtags API...")
    
    try:
        response = requests.get(f"{BASE_URL}/hashtags/trending")
        print(f"   GET /hashtags/trending: {response.status_code}")
        if response.status_code == 200:
            hashtags = response.json()
            print(f"   Trending hashtags: {len(hashtags)}")
    except Exception as e:
        print(f"   ❌ Hashtags API error: {e}")

def test_media_api():
    """Test dell'API Media"""
    print("\n🔍 Testing Media API...")
    
    try:
        response = requests.get(f"{BASE_URL}/media/user/1")  # Media for user 1
        print(f"   GET /media/user/1: {response.status_code}")
        if response.status_code != 404:
            print(f"   Response: {response.json()}")
    except Exception as e:
        print(f"   ❌ Media API error: {e}")

def main():
    """Esegue tutti i test"""
    print("🚀 Starting API Tests for Social Media Automation System")
    print(f"📍 Base URL: {BASE_URL}")
    print("=" * 60)
    
    test_health_check()
    test_templates_api()
    test_content_api()
    test_analytics_api()
    test_engagement_api()
    test_hashtags_api()
    test_media_api()
    
    print("\n" + "=" * 60)
    print("✅ API Tests completed!")
    print(f"📚 Full API documentation: {BASE_URL}/docs")
    print(f"🏠 Homepage: {BASE_URL}/")

if __name__ == "__main__":
    main()
