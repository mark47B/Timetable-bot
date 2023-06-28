from pydantic import BaseModel


class ProfileLink(BaseModel):
    id: str
    fullname: str

    def __len__(self):
        return len(self.fullname)
