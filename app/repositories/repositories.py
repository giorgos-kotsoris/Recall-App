# πρόσβαση των services στα δεδομένα.


from app.infrastructure.database import db
from app.infrastructure.models import GroupModel, MemberModel, UserModel


class GroupRepository:
    def all(self):
        return GroupModel.query.order_by(GroupModel.name).all()

    def get(self, group_id):
        return db.session.get(GroupModel, group_id)

    def by_name(self, name):
        return GroupModel.query.filter_by(name=name).first()

    def add(self, group):
        db.session.add(group)
        db.session.commit()
        return group

    def delete(self, group):
        db.session.delete(group)
        db.session.commit()


class MemberRepository:
    def all(self, group_id=None):
        query = MemberModel.query
        if group_id:
            query = query.filter_by(group_id=group_id)
        return query.order_by(MemberModel.last_name, MemberModel.first_name).all()

    def get(self, member_id):
        return db.session.get(MemberModel, member_id)

    def add(self, member):
        db.session.add(member)
        db.session.commit()
        return member

    def delete(self, member):
        db.session.delete(member)
        db.session.commit()


class UserRepository:
    def all(self):
        return UserModel.query.order_by(UserModel.username).all()

    def get(self, user_id):
        return db.session.get(UserModel, user_id)

    def by_username(self, username):
        return UserModel.query.filter_by(username=username).first()

    def add(self, user):
        db.session.add(user)
        db.session.commit()
        return user

    def delete(self, user):
        db.session.delete(user)
        db.session.commit()
