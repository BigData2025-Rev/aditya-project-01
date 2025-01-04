import sys
import os
import uuid

from getpass import getpass
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from model.user import User, Role
from db.session import session as Db

if __name__=='__main__':
    username = input("Please Enter a Username: ")
    email = input("Please enter an email address: ")
    password = getpass("Please enter password: ")
    re_password = getpass("Please re-enter password: ")
    while re_password != password or not password:
        print("Passwords do not match! Please enter again!")
        password = getpass("Please enter password: ")
        re_password = getpass("Please re-enter password: ")
    role = Role.admin.value
    with Db() as session:
        try:
            db_user = session.query(User).filter(User.username==username,User.role==role).first()
            if db_user:
                raise Exception("admin with the username exists!")
            else:
                user = User(username=username, email=email, role=role)
                user.set_password(password=re_password)
                session.add(user)
                session.commit()
                get_db_user = session.query(User).filter(User.username==username, User.role==role).first()
                if get_db_user:
                    print(f"Created admin, username: {get_db_user.username}, userid: {uuid.UUID(bytes=get_db_user.id)}")
                else:
                    raise Exception("user could not be created")
        except Exception as e:
            print(f"Could not create admin! {e}")
