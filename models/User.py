

from database.database import db


class Person(db.Model):
        person_id = db.Column(db.Integer,primary_key=True)
        first_name = db.Column(db.String(20),nullable=False)
        last_name = db.Column(db.String(20),nullable=False)
        nationality = db.Column(db.String(30),nullable=False)

        def __repr__(self) -> str:
            return f"{self.first_name} {self.last_name} - {self.person_id}"