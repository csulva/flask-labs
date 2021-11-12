from fake import Faker
from app.models import User, TodoList, Todo
from app import db
from sqlalchemy.exc import IntegrityError
import string
from random import randint

def users(count=20):
    fake = Faker()
    i = 0
    while i < count:
        u = User(_username=fake.user_name(), _email=fake.email(), password='corn',
            member_since=fake.past_date(), last_seen=fake.past_date(), is_admin=False)
        db.session.add(u)
        try:
            db.session.commit()
            i += 1
        except IntegrityError:
            db.session.rollback()

def to_do_list(count=10):
    fake = Faker()
    user_count=User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count-1)).first()
        t = TodoList(_title=string.capwords(fake.bs()),
            created_at=fake.past_date(),
            creator=u)
        db.session.add(t)
    db.session.commit()

def tasks(count=50):
    fake = Faker()
    user_count=User.query.count()
    for i in range(count):
        u = User.query.offset(randint(0, user_count-1)).first()
        task = Todo(description=fake.text(),
                created_at=fake.past_date(),
                finished_at=fake.past_date(),
                is_finished=False,
                creator=u)
        db.session.add(task)
    db.session.commit()




