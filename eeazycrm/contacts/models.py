from datetime import datetime
from eeazycrm import db
from flask import request
from flask_login import current_user


class Contact(db.Model):
    id = db.Column(db.Integer, db.Sequence('contact_id_seq'), primary_key=True)
    first_name = db.Column(db.String(20))
    last_name = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    avatar = db.Column(db.String(25))
    phone = db.Column(db.String(20), nullable=False)
    mobile = db.Column(db.String(20))
    address_line = db.Column(db.String(40))
    addr_state = db.Column(db.String(20))
    addr_city = db.Column(db.String(20))
    post_code = db.Column(db.String(20))
    country = db.Column(db.String(20))
    notes = db.Column(db.String(200))
    account_id = db.Column(db.Integer, db.ForeignKey('account.id', ondelete='cascade'), nullable=False)
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id', ondelete='SET NULL'), nullable=True)
    deals = db.relationship(
        'Deal',
        backref='contact',
        lazy=True
    )
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    @staticmethod
    def contact_list_query():
        account = request.args.get('acc', None, type=int)
        if current_user.role.name == 'admin':
            contacts = Contact.query\
                .filter(Contact.account_id == account if account else True)
        else:
            contacts = Contact.query \
                .filter(Contact.account_id == account if account else True) \
                .filter(owner_id=current_user.id)
        return contacts

    @staticmethod
    def get_label(contact):
        return contact.first_name + ' ' + contact.last_name

    def get_contact_name(self):
        if self.last_name:
            return self.first_name + ' ' + self.last_name
        else:
            return None

    def __repr__(self):
        return f"Account('{self.last_name}', '{self.email}', '{self.phone}')"
