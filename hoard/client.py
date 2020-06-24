from typing import Tuple

import requests

from hoard.api import Api
from hoard.models import create_from_dict, Dataset


class Transport:
    def __init__(self):
        self.session = requests.Session()

    def send(self, req: requests.Request) -> requests.Response:
        r = self.session.prepare_request(req)
        resp = self.session.send(r)
        resp.raise_for_status()
        return resp


class DataverseKey:
    def __init__(self, key: str = None) -> None:
        self.key = key

    def __call__(self, req: requests.Request) -> requests.Request:
        req.headers["X-Dataverse-key"] = self.key
        return req


class Client:
    def __init__(self, api: Api, transport: Transport) -> None:
        self.api = api
        self.transport = transport

    def get(self, *, pid: str = None, id: int = None) -> Dataset:
        if pid is not None:
            req = self.api.get_dataset_by_pid(pid)
        elif id is not None:
            req = self.api.get_dataset_by_id(id)
        else:
            raise Exception("You must supply either an id or a pid")
        resp = self.transport.send(req)
        return create_from_dict(resp.json()["data"])

    def create(self, dataset: Dataset, parent: str = "root") -> Tuple[int, str]:
        req = self.api.create_dataset(parent, dataset.asdict())
        resp = self.transport.send(req)
        data = resp.json()["data"]
        return data["id"], data["persistentId"]
