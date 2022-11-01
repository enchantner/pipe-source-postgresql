import calendar
import random
from datetime import datetime

from faker import Faker

from pipereport.base.source import BaseSource


class Source(BaseSource):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields = self.required_field("fields")
        self.parameters = self.required_field("parameters")

    def run(self):
        fake = Faker()

        for i in range(self.parameters["files_count"]):
            lines = (
                tuple(str(getattr(fake, col, random.random)()) for col in self.fields["columns"])
                for _ in range(self.fields["size"])
            )
            self.write_block(
                lines,
                self.parameters["files_path"].format(
                    timestamp=calendar.timegm(datetime.utcnow().utctimetuple()), part=i
                ),
                columns=self.fields["columns"],
            )
