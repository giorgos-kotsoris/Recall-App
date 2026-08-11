from app.domain.entities import Group, Member
from app.infrastructure.models import GroupModel, MemberModel
from app.repositories.repositories import GroupRepository, MemberRepository


class OrganizationService:
    def __init__(self):
        self.groups = GroupRepository()
        self.members = MemberRepository()

    def list_groups(self): return self.groups.all()
    def list_members(self, group_id=None): return self.members.all(group_id)
    def get_member(self, member_id): return self.members.get(member_id)

    def create_group(self, name, description):
        entity = Group(name.strip(), (description or "").strip() or None)
        entity.validate()
        if self.groups.by_name(entity.name):
            raise ValueError("Υπάρχει ήδη ομάδα με αυτό το όνομα.")
        return self.groups.add(GroupModel(name=entity.name, description=entity.description))

    def delete_group(self, group_id):
        group = self.groups.get(group_id)
        if not group: raise LookupError("Η ομάδα δεν βρέθηκε.")
        if group.members: raise ValueError("Δεν μπορείτε να διαγράψετε ομάδα που έχει μέλη.")
        self.groups.delete(group)

    def create_member(self, data):
        entity = Member(**data)
        entity.validate()
        if not self.groups.get(entity.group_id): raise ValueError("Η επιλεγμένη ομάδα δεν υπάρχει.")
        return self.members.add(MemberModel(**entity.__dict__))

    def update_member(self, member_id, data):
        entity = Member(**data)
        entity.validate()
        member = self.members.get(member_id)
        if not member: raise LookupError("Το μέλος δεν βρέθηκε.")
        if not self.groups.get(entity.group_id): raise ValueError("Η επιλεγμένη ομάδα δεν υπάρχει.")
        for field, value in entity.__dict__.items(): setattr(member, field, value)
        from app.infrastructure.database import db
        db.session.commit()
        return member

    def delete_member(self, member_id):
        member = self.members.get(member_id)
        if not member: raise LookupError("Το μέλος δεν βρέθηκε.")
        self.members.delete(member)
