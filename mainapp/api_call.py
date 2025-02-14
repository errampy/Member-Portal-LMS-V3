import requests
import json

def api_get(url, headers=None):
    """
    Make a GET request to the specified URL.

    Parameters:
    - url (str): The API endpoint.
    - headers (dict, optional): Any custom headers to send with the request.

    Returns:
    - response (dict or None): The response JSON if successful, otherwise None.
    """
    try:
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            return response.json()
        else:
            return response.status_code
    except requests.exceptions.RequestException as e:
        print(f"GET request failed: {e}")
        return None


def api_post(url, data=None, headers=None):
    """
    Make a POST request to the specified URL.

    Parameters:
    - url (str): The API endpoint.
    - data (dict, optional): The payload for the POST request.
    - headers (dict, optional): Any custom headers to send with the request.

    Returns:
    - response (dict or None): The response JSON if successful, otherwise None.
    """
    try:
        response = requests.post(url, json=data)
        print('status ', response.status_code)
        print('status ', response.json())
        return response
    except Exception as error:
        print(f"POST APIS ERROR IS : {error}")
        return None
    

def call_post_method_without_token(URL,data):
    api_url = URL
    headers = { "Content-Type": "application/json"}
    response = requests.post(api_url,data=data,headers=headers)
    return response

def call_post_method_without_token_v2(URL, data, files=None):
    headers = {} 

    try:
        if files:
            response = requests.post(URL, data=data, files=files, headers=headers)
        else:
            headers["Content-Type"] = "application/json"
            response = requests.post(URL, json=data, headers=headers)

        return response
    except requests.RequestException as e:
        print("Request Error:", e)
        return None
    
def call_post_method_with_token_v2(URL, endpoint, data, access_token=None, files=None):
    api_url = URL + endpoint
    headers = {"Authorization": f'Bearer {access_token}'}
    
    if files:
        response = requests.post(api_url, data=data, files=files, headers=headers)
    else:
        headers["Content-Type"] = "application/json"
        response = requests.post(api_url, data=data, headers=headers)

    if response.status_code in [200, 201]:
        try:
            return {'status_code': 0, 'data': response.json()}
        except json.JSONDecodeError:
            return {'status_code': 1, 'data': 'Invalid JSON response'}
    else:
        try:
            return {'status_code': 1, 'data': response.json()}
        except json.JSONDecodeError:
            return {'status_code': 1, 'data': 'Something went wrong'}




def api_post_with_token(url, data=None, headers=None):
    """
    Make a POST request to the specified URL using an authentication token.

    Parameters:
    - url (str): The API endpoint.
    - data (dict, optional): The payload for the POST request.
    - headers (dict, optional): Any custom headers to send with the request.

    Returns:
    - response_json (dict or None): The response JSON if successful, otherwise None.
    """
    try:
        # Step 1: Login to retrieve the access token
        login_url = "https://loanmanagementb1.pythonanywhere.com/api/token/"  # Assuming '/login' is the endpoint for login
        login_data = {
            'email': "admin@gmail.com",
            'password': '1234'
        }
        login_response = requests.post(login_url, json=login_data)
        
        # Check if login was successful
        if login_response.status_code != 200:
            print("Login failed: ", login_response.status_code, login_response.text)
            return None
        
        # Extract access token from the login response
        login_json = login_response.json()
        access_token = login_json.get('access_token')
        if not access_token:
            print("Access token not found in login response.")
            return None
        
        # Step 2: Make the second POST request with the access token
        headers = headers or {}
        headers['Authorization'] = f'Bearer {access_token}'
        
        response = requests.post(url, json=data, headers=headers)
        
        # Check if the second POST request was successful
        if response.status_code != 200:
            print("POST request failed: ", response.status_code, response.text)
            return None
        
        # Return the JSON response from the POST request
        return response.json()
    
    except Exception as error:
        print(f"API POST ERROR: {error}")
        return None

def api_put(url, data=None, headers=None):
    """
    Make a PUT request to the specified URL.

    Parameters:
    - url (str): The API endpoint.
    - data (dict, optional): The payload for the PUT request.
    - headers (dict, optional): Any custom headers to send with the request.

    Returns:
    - response (dict or None): The response JSON if successful, otherwise None.
    """
    try:
        response = requests.put(url, json=data, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"PUT request failed: {e}")
        return None


def api_delete(url, headers=None):
    """
    Make a DELETE request to the specified URL.

    Parameters:
    - url (str): The API endpoint.
    - headers (dict, optional): Any custom headers to send with the request.

    Returns:
    - response (dict or None): The response JSON if successful, otherwise None.
    """
    try:
        response = requests.delete(url, headers=headers)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"DELETE request failed: {e}")
        return None


