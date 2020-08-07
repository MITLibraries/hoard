from typing import Iterator, Optional, Tuple

import requests
from sickle import Sickle  # type: ignore
import xml.etree.ElementTree as ET

from hoard.api import Api
from hoard.models import Dataset


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


class DataverseClient:
    def __init__(self, api: Api, transport: Transport) -> None:
        self.api = api
        self.transport = transport

    def get(self, *, pid: str = None, id: int = None) -> dict:
        if pid is not None:
            req = self.api.get_dataset_by_pid(pid)
        elif id is not None:
            req = self.api.get_dataset_by_id(id)
        else:
            raise Exception("You must supply either an id or a pid")
        resp = self.transport.send(req)
        return resp.json()

    def create(self, dataset: Dataset, parent: str = "root") -> Tuple[int, str]:
        req = self.api.create_dataset(parent, dataset.asdict())
        resp = self.transport.send(req)
        data = resp.json()["data"]
        return data["id"], data["persistentId"]


class DSpaceClient:
    ...


class OAIClient:
    def __init__(self, source_url: str, format: str, set: str = None) -> None:
        self.source_url = source_url
        self.format = format
        self.set = set
        self.ids: Optional[Iterator] = None
        client = Sickle(self.source_url)
        self.client = client
        session = requests.Session()
        self.session = session

    def __iter__(self) -> Iterator[str]:
        return self

    def __next__(self) -> str:
        if self.ids is None:
            self.ids = self.fetch_ids()
        session = self.session
        while True:
            header_xml = next(self.ids)
            parsed_header = ET.fromstring(header_xml.raw)
            namespace = {"oai": "http://www.openarchives.org/OAI/2.0/"}
            id_elem = parsed_header.find("oai:identifier", namespace)
            if id_elem is None:
                raise Exception("No OAI identifier found")
            else:
                id = id_elem.text
            params = {
                "verb": "GetRecord",
                "metadataPrefix": self.format,
                "identifier": id,
            }
            record = session.get(self.source_url, params=params).text
            parsed_record = ET.fromstring(record)
            deleted = parsed_record.find(
                ".//oai:header[@status='deleted']", namespaces=namespace
            )
            if deleted:
                continue
            else:
                return record

    def fetch_ids(self) -> Iterator:
        client = self.client
        params = {"metadataPrefix": self.format}
        if self.set is not None:
            params["set"] = self.set
        ids = client.ListIdentifiers(**params)
        return ids
