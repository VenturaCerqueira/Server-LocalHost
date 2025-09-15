import requests

def test_login():
    url = "http://127.0.0.1:5000/login"
    data = {
        "username": "testuser",
        "password": "newpassword123"
    }
    with requests.Session() as session:
        response = session.post(url, data=data)
        print("Status Code:", response.status_code)
        if response.history:
            print("Request was redirected")
            for resp in response.history:
                print(resp.status_code, resp.url)
            print("Final destination:")
            print(response.status_code, response.url)
        else:
            print("Request was not redirected")
        print("Response text snippet:", response.text[:200])

if __name__ == "__main__":
    test_login()
