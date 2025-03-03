"""
"""
from flask_reddit import db
from flask_reddit.users import constants as USER
from flask_reddit.threads.models import thread_upvotes, comment_upvotes, Thread
from datetime import datetime

class Subscribe(db.Model):
    __tablename__= 'subscribe'

    subscriber_id = db.Column(db.Integer, db.ForeignKey('users_user.id'), primary_key=True)
    thread_id = db.Column(db.Integer, db.ForeignKey('threads_thread.id'), primary_key=True)
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

class User(db.Model):
    """
    """
    __tablename__ = 'users_user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(USER.MAX_USERNAME), unique=True)
    email = db.Column(db.String(USER.MAX_EMAIL), unique=True)
    password = db.Column(db.String(USER.MAX_PASSW))
    created_on = db.Column(db.DateTime, default=db.func.now())

    threads = db.relationship('Thread', backref='user', lazy='dynamic')
    comments = db.relationship('Comment', backref='user', lazy='dynamic')
    subreddits = db.relationship('Subreddit', backref='user', lazy='dynamic')

    status = db.Column(db.SmallInteger, default=USER.ALIVE)
    role = db.Column(db.SmallInteger, default=USER.USER)

    subscribe = db.relationship('Thread', foreign_keys=[Subscribe.subscriber_id], backref='user', lazy='dynamic', cascade='all, delete-orphan')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

    def __repr__(self):
        return '<User %r>' % (self.username)

    def get_status(self):
        """
        returns string form of status, 0 = 'dead', 1 = 'alive'
        """
        return USER.STATUS[self.status]

    def get_role(self):
        """
        analogous to above but for roles
        """
        return USER.ROLE[self.role]

    def get_thread_karma(self):
        """
        fetch the number of votes this user has had on his/her threads

        1.) Get id's of all threads by this user

        2.) See how many of those threads also were upvoted but not by
        the person him/her self.
        """
        thread_ids = [t.id for t in self.threads]
        select = thread_upvotes.select(db.and_(
                thread_upvotes.c.thread_id.in_(thread_ids),
                thread_upvotes.c.user_id != self.id
            )
        )
        rs = db.engine.execute(select)
        return rs.rowcount

    def get_comment_karma(self):
        """
        fetch the number of votes this user has had on his/her comments
        """
        comment_ids = [c.id for c in self.comments]
        select = comment_upvotes.select(db.and_(
                comment_upvotes.c.comment_id.in_(comment_ids),
                comment_upvotes.c.user_id != self.id
            )
        )
        rs = db.engine.execute(select)
        return rs.rowcount

    def is_subscribed(self, thread):
        if thread.id is None:
            return False
        return self.subscribe.filter_by(subscriber_id=thread.id).first() is not None

    def subscribe_to_thread(self, thread):
        if not self.is_subscribed(thread):
            t = Subscribe(subscriber_id=self, thread_id=thread)
            db.session.add(t)

    def unsubscribe(self, thread):
        t = self.subscribe.filter_by(subscriber_id=thread.id).first()
        if t:
            db.session.delete()