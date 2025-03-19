from abc import ABC, abstractmethod


class AbstractRequest(ABC):
    @abstractmethod
    async def fetch(
        self,
        method: str = "GET",
        url: str = None,
        data: dict = None,
        params: dict = None,
        headers: dict = None,
        cookies: dict = None,
    ):
        raise NotImplementedError("`fetch` Not implemented")
