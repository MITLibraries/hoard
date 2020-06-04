import requests


class ApiV1:
    version: str = "v1"

    def __init__(self, url: str, auth=None) -> None:
        url = url.rstrip("/")
        self.url = f"{url}/api/{self.version}"
        self.auth = auth

    def create_dataset(self, parent: str, dataset: dict) -> requests.Request:
        url = f"{self.url}/{parent}/datasets"
        return requests.Request("POST", url, json=dataset, auth=self.auth)

    def get_dataset_by_id(self, id: int) -> requests.Request:
        url = f"{self.url}/datasets/{id}"
        return requests.Request("GET", url)

    def get_dataset_by_pid(self, pid: str) -> requests.Request:
        url = f"{self.url}/datasets/:persistentId"
        return requests.Request("GET", url, params={"persistentId": pid})


Api = ApiV1
