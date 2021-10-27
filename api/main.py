from fastapi import FastAPI, status, HTTPException
from fastapi.params import Depends
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from a2wsgi import ASGIMiddleware
from api import models
from api import schemas
from api import database 
from api.database import SessionLocal, engine
from mangum import Mangum



app = FastAPI()

schemas.Base.metadata.create_all(engine)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# @app.post('/create_user', status_code=status.HTTP_201_CREATED)
# def create_user(user: models.UserDetails, db: Session = Depends(get_db)):
#     # name variable is from schemas file
#     # user_name variable is from model file
#     # we are assigning name  =  user_name
#     new_user = schemas.User(name=user.user_name, surname=user.user_surname)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user
#
#
# @app.get("/userlist")
# async def getall(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     userList = db.query(schemas.User).all()
#     return userList
#
#
# @app.get('/userlist/{id}')
# def show(id, db: Session = Depends(get_db)):
#     userList = db.query(schemas.User).filter(schemas.User.id == id).first()
#     return userList


@app.get("/")
async def root():
    return {"message": "Hello Worlwd"}

@app.post('/createid', status_code=status.HTTP_201_CREATED)
def create_id(user: models.IDGenerate, db: Session = Depends(get_db)):
    # name variable is from schemas file
    # user_name variable is from model file
    # we are assigning name  =  user_name
    new_user = schemas.IdGeneratorSql(room_id=user.id_generate, name=user.person_name, mobile_number=user.mobile_number)
    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        print("\nError Issur ", e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Room ID already exist")


@app.get('/generator_id/{room_id}', status_code=status.HTTP_200_OK)
def generator_id(room_id: str, db: Session = Depends(get_db)):
    try:
        check = db.query(schemas.IdGeneratorSql).filter(schemas.IdGeneratorSql.room_id == room_id).first()
        if check is None:
            return {"details": "Not found"}
        return check
    except Exception as e:
        return e.__str__()


@app.post('/login_with_id', status_code=status.HTTP_201_CREATED)
def login_with_id(user: models.PeopleWithID, db: Session = Depends(get_db)):
    # name variable is from schemas file
    # user_name variable is from model file
    # we are assigning name  =  user_name
    isExist = db.query(schemas.IdGeneratorSql).filter(schemas.IdGeneratorSql.room_id == user.id_generate).first()
    if isExist is None:
        print("\n Check =====  Data is None")
        return {"details": "Not found"}
    else:

        userPresentWithData = db.query(schemas.PeopleWithId).filter(
            schemas.PeopleWithId.room_id_new == user.id_generate,
            schemas.PeopleWithId.mobile_number == user.mobile_number,
            schemas.PeopleWithId.name == user.person_name).first()
        print(f"\n {userPresentWithData}")
        if userPresentWithData is None:
            user_withId = schemas.PeopleWithId(room_id_new=user.id_generate, name=user.person_name,
                                               mobile_number=user.mobile_number)
            try:
                db.add(user_withId)
                db.commit()
                db.refresh(user_withId)
                return user_withId
            except Exception as e:
                print("\n Error = ", e)
        else:
            return userPresentWithData


@app.get('/allmember/{room_id}', status_code=status.HTTP_200_OK)
def member_with_id(room_id: str, db: Session = Depends(get_db)):
    try:
        check = db.query(schemas.PeopleWithId).filter(schemas.PeopleWithId.room_id_new == room_id).all()
        if check is None:
            return {"details": "Not found"}
        return check
    except Exception as e:
        return e.__str__()


@app.post('/createpost', status_code=status.HTTP_201_CREATED)
def create_post(user: models.CreatePost, db: Session = Depends(get_db)):
    # name variable is from schemas file
    # user_name variable is from model file
    # we are assigning name  =  user_name
    new_user = schemas.CreatePostWithId(room_id=user.room_id,
                                        mobile_number=user.mobile_number,
                                        created_by_name=user.created_by_name,
                                        task_assign_to=user.task_assign_to,
                                        time_to_finish=user.time_to_finish,
                                        date_time=user.date_time,
                                        before_after=user.before_after,
                                        possible_if=user.possible_if,
                                        task_des=user.task_des,
                                        is_active=user.is_active,
                                        img_url=user.img_url,
                                        title=user.title,
                                        )

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except Exception as e:
        print("\nError Issur ", e)
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Room ID already exist")


@app.get('/getpost/{room_id}', status_code=status.HTTP_200_OK)
def get_post_list(room_id: str, db: Session = Depends(get_db)):
    try:
        check = db.query(schemas.CreatePostWithId).filter(schemas.CreatePostWithId.room_id == room_id).all()
        print(f"Error coming {check}")
        if not check:
            return {"details": "Not found"}
        return check
    except Exception as e:
        return e.__str__()


@app.delete('/deleted/{post_id}')
def delete_post(post_id: int, db: Session = Depends(get_db)):
    try:
        check = db.query(schemas.CreatePostWithId).filter(schemas.CreatePostWithId.post_id == post_id).delete(
            synchronize_session=False)
        db.commit()
        if not check:
            return {"details": "Not found"}
        return check
    except Exception as e:
        return e.__str__()


@app.put('/update/{post_id}')
def update_post(post_id, user: models.CreatePost, db: Session = Depends(get_db)):

    check = db.query(schemas.CreatePostWithId).filter(schemas.CreatePostWithId.post_id == post_id)
    isExist = check.first()
    print(f"Error check again {isExist}")
    if not isExist:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No data present")
    check.update(user.dict())
    db.commit()


    return "update data"

handler = Mangum(app=app)