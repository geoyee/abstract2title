import requests


def test_request(image_path: str = "data/test.jpg") -> None:
    resp = requests.post(
        "http://127.0.0.1:8000/predict",
        files={"file": open(image_path, "rb")}
    )
    print(resp.status_code)


if __name__ == "__main__":
    test_request()
