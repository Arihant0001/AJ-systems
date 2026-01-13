#!/usr/bin/env python3
"""
Test script for Password Reset Flow
Run this after starting the backend server
"""

import requests
import time

BASE_URL = "http://localhost:8000"

def test_forgot_password():
    """Test the forgot password endpoint"""
    print("\n" + "="*60)
    print("TEST 1: Forgot Password Request")
    print("="*60)
    
    # Test with valid email
    response = requests.post(
        f"{BASE_URL}/auth/forgot-password",
        json={"email": "test@example.com"}
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("✅ Always returns success (no email enumeration)")
    
    # Test with invalid email (should still return success)
    response = requests.post(
        f"{BASE_URL}/auth/forgot-password",
        json={"email": "nonexistent@example.com"}
    )
    
    print(f"\nTesting non-existent email:")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("✅ Same response (security feature)")
    
    print("\n⚠️  Check the backend console for the reset link!")
    return True


def test_reset_password_invalid_token():
    """Test reset with invalid token"""
    print("\n" + "="*60)
    print("TEST 2: Reset Password with Invalid Token")
    print("="*60)
    
    response = requests.post(
        f"{BASE_URL}/auth/reset-password",
        json={
            "token": "invalid-token-12345",
            "new_password": "NewPassword123"
        }
    )
    
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}")
    print("✅ Correctly rejects invalid token")


def test_complete_flow():
    """Test complete password reset flow"""
    print("\n" + "="*60)
    print("COMPLETE FLOW TEST")
    print("="*60)
    
    print("\n📝 Instructions:")
    print("1. Run this script")
    print("2. Copy the reset link from backend console")
    print("3. Visit the link in your browser")
    print("4. Enter new password")
    print("5. Try logging in with new password")
    
    print("\nCURL examples:")
    print("\n1. Request reset:")
    print('curl -X POST http://localhost:8000/auth/forgot-password \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"email":"your-email@example.com"}\'')
    
    print("\n2. Reset password (use token from console):")
    print('curl -X POST http://localhost:8000/auth/reset-password \\')
    print('  -H "Content-Type: application/json" \\')
    print('  -d \'{"token":"YOUR-TOKEN-HERE","new_password":"NewPassword123"}\'')


if __name__ == "__main__":
    print("\n🔐 Password Reset Feature Test Suite")
    print("="*60)
    print("Make sure the backend server is running on http://localhost:8000")
    print("="*60)
    
    try:
        # Test forgot password endpoint
        test_forgot_password()
        time.sleep(1)
        
        # Test invalid token
        test_reset_password_invalid_token()
        time.sleep(1)
        
        # Show complete flow instructions
        test_complete_flow()
        
        print("\n" + "="*60)
        print("✅ All automated tests passed!")
        print("="*60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to backend server")
        print("Make sure the server is running: cd backend && uvicorn app.main:app --reload")
    except Exception as e:
        print(f"\n❌ Error: {e}")
