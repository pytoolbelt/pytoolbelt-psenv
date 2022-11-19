import boto3
from typing import Dict, List, Optional, Generator


class ParameterStore:
    """
    Class to represent the AWS ssm parameter store
    """

    def __init__(self, path: str) -> None:
        self.path = path
        self.ssm_client = boto3.client("ssm")

    @staticmethod
    def _ssm_params_to_dict(params: Dict[str, str]) -> Dict[str, str]:
        return {key.split("/")[-1]: value for key, value in params.items()}

    @staticmethod
    def _chunk_list(chunk_list: List[str], chunk_size: Optional[int] = 10):
        for i in range(0, len(chunk_list), chunk_size):
            yield chunk_list[i : i + chunk_size]

    def fetch(self) -> Dict[str, str]:

        params = {}
        next_token = ""

        while True:

            fetch_kwargs = {"Path": self.path, "Recursive": True, "WithDecryption": True}

            if next_token:
                fetch_kwargs["NextToken"] = next_token

            response = self.ssm_client.get_parameters_by_path(**fetch_kwargs)
            params.update(**{p["Name"].upper(): p["Value"] for p in response["Parameters"] if "\n" not in p["Value"]})

            try:
                next_token = response["NextToken"]
            except KeyError:
                break

        return self._ssm_params_to_dict(params)

    def push(self, params: Dict[str, str], overwrite: bool = False) -> List[str]:
        responses = []
        for key, value in params.items():
            name = f"{self.path}/{key}"
            response = self.ssm_client.put_parameter(Name=name, Value=value, Type="SecureString", Overwrite=overwrite)
            msg = f"Posted {name} -- version {response['Version']}"
            responses.append(msg)
        return responses

    def delete(self, params: Dict[str, str]) -> Generator[Dict[str, List[str]], None, None]:
        names = [f"{self.path}/{key}" for key in params.keys()]
        for names_chunk in self._chunk_list(names):
            yield self.ssm_client.delete_parameters(Names=names_chunk)
