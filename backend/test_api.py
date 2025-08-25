import requests
import json

# Base URL for the Django API
BASE_URL = 'http://127.0.0.1:8000'

def test_root_endpoint():
    """Test the root endpoint redirects to posts"""
    print("Testing root endpoint...")
    try:
        response = requests.get(BASE_URL, allow_redirects=False)
        if response.status_code == 302:
            print("✓ Root endpoint correctly redirects")
        else:
            print(f"✗ Root endpoint returned status code {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing root endpoint: {e}")

def test_posts_endpoint():
    """Test the posts endpoint"""
    print("Testing posts endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/posts/")
        if response.status_code == 200:
            print("✓ Posts endpoint is accessible")
            data = response.json()
            print(f"  - Response: {data}")
        else:
            print(f"✗ Posts endpoint returned status code {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing posts endpoint: {e}")

def test_register_endpoint():
    """Test the register endpoint"""
    print("Testing register endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/register/",
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'username': 'testuser',
                'email': 'test@example.com',
                'password': 'testpassword123'
            })
        )
        if response.status_code in [200, 201]:
            print("✓ Register endpoint is accessible")
            data = response.json()
            print(f"  - Response: {data}")
        elif response.status_code == 400:
            print("✓ Register endpoint is accessible (user may already exist)")
            data = response.json()
            print(f"  - Response: {data}")
        else:
            print(f"✗ Register endpoint returned status code {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing register endpoint: {e}")

def test_login_endpoint():
    """Test the login endpoint"""
    print("Testing login endpoint...")
    try:
        response = requests.post(
            f"{BASE_URL}/login/",
            headers={'Content-Type': 'application/json'},
            data=json.dumps({
                'username': 'testuser',
                'password': 'testpassword123'
            })
        )
        if response.status_code == 200:
            print("✓ Login endpoint is accessible")
            data = response.json()
            print(f"  - Response: {data}")
        elif response.status_code == 401:
            print("✓ Login endpoint is accessible (invalid credentials)")
            data = response.json()
            print(f"  - Response: {data}")
        else:
            print(f"✗ Login endpoint returned status code {response.status_code}")
    except Exception as e:
        print(f"✗ Error testing login endpoint: {e}")

if __name__ == "__main__":
    print("Testing Django API endpoints...\n")
    
    test_root_endpoint()
    print()
    
    test_posts_endpoint()
    print()
    
    test_register_endpoint()
    print()
    
    test_login_endpoint()
    print()
    
    print("API testing completed.")