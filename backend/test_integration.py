import requests
import json

# Test the integration between frontend and backend
def test_integration():
    # Base URLs
    backend_url = 'http://127.0.0.1:8000'
    
    print("Testing integration between frontend and backend...\n")
    
    # Test 1: Check if backend is running
    print("1. Testing backend availability...")
    try:
        response = requests.get(backend_url, timeout=5)
        if response.status_code == 200:
            print("   ✓ Backend is running and accessible")
        else:
            print(f"   ✗ Backend returned status code {response.status_code}")
    except requests.exceptions.ConnectionError:
        print("   ✗ Backend is not accessible. Make sure it's running on port 8000")
        return
    except Exception as e:
        print(f"   ✗ Error connecting to backend: {e}")
        return
    
    # Test 2: Check if posts endpoint works
    print("2. Testing posts endpoint...")
    try:
        response = requests.get(f"{backend_url}/api/posts/")
        if response.status_code == 200:
            print("   ✓ Posts endpoint is working")
            data = response.json()
            print(f"   ✓ Posts data received: {len(data.get('posts', []))} posts")
        else:
            print(f"   ✗ Posts endpoint returned status code {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error testing posts endpoint: {e}")
    
    # Test 3: Test CORS headers
    print("3. Testing CORS headers...")
    try:
        response = requests.get(
            f"{backend_url}/api/posts/",
            headers={'Origin': 'http://localhost:3000'}
        )
        cors_header = response.headers.get('Access-Control-Allow-Origin')
        if cors_header:
            print(f"   ✓ CORS headers present: {cors_header}")
        else:
            print("   ✗ CORS headers not found")
    except Exception as e:
        print(f"   ✗ Error testing CORS headers: {e}")
    
    # Test 4: Test user registration
    print("4. Testing user registration...")
    try:
        response = requests.post(
            f"{backend_url}/api/register/",
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'username': 'integration_test_user',
                'email': 'integration@test.com',
                'password': 'testpassword123'
            })
        )
        if response.status_code in [200, 201]:
            print("   ✓ User registration successful")
        elif response.status_code == 400:
            print("   ✓ User registration endpoint accessible (user may already exist)")
        else:
            print(f"   ✗ User registration failed with status code {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error testing user registration: {e}")
    
    print("\nIntegration test completed.")

if __name__ == "__main__":
    test_integration()