from pydantic import BaseModel


# class UserDetails(BaseModel):
#     user_name: str
#     user_surname: str


class IDGenerate(BaseModel):
    person_name: str
    id_generate: str
    mobile_number: str


class PeopleWithID(BaseModel):
    person_name: str
    id_generate: str
    mobile_number: str


class CreatePost(BaseModel):
    room_id: str
    mobile_number: str
    created_by_name: str
    task_assign_to: str
    time_to_finish: str
    date_time: str
    before_after: str
    possible_if: str
    task_des: str
    is_active: str
    img_url: str
    title: str
