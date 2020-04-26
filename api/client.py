import inspect
import logging
import requests

logger = logging.getLogger("example." + __name__)

class Bear:

    _s = requests.session()
    host = None


    def __init__(self, host):
        self.host = host
        self.death_note = []

    def verify_response(
            self, res: requests.Response, ok_status=200
    ) -> requests.Response:
        func = inspect.stack()[1][3]
        if isinstance(ok_status, int):
            ok_status = [ok_status]
        if res.status_code not in ok_status:
            raise ValueError(
                f"Verified response: function {func} failed: "
                f"server responded {res.status_code} "
                f"with data: {res.content}"
            )
        else:
            logger.info(
                f"Verified response: function {func} code {res.status_code}"
            )
        return res

    vr = verify_response

    def create_bear(self, data):
        data = self._s.post(self.host + "/bear", json=data)
        if (data.status_code == 200):
            self.death_note.append(data.json())
        return data

    def show_bear(self, id_of_bear):
        return self._s.get(self.host + "/bear" + "/" + id_of_bear)

    def show_bears(self):
        return self._s.get(self.host + "/bear")

    def delete_bear(self, id_of_bear):
        return self._s.delete(self.host + f"/bear/{id_of_bear}")

    def delete_bears(self):
        return self._s.delete(self.host + "/bear")

    def update_bear(self, id_of_bear, data):
        return self._s.put(self.host + "/bear" + "/" + id_of_bear, json=data)

    def clean_up(self):
        for i in self.death_note:
            self.delete_bear(i)