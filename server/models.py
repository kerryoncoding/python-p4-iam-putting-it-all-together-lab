# from sqlalchemy.ext.hybrid import hybrid_property
# from sqlalchemy_serializer import SerializerMixin

# from config import db, bcrypt


# # Create a User model with the following attributes: (id that is an integer type and a primary key. username that is a String type...)

# # User to have many recipes   <<--- what is this?

# class User(db.Model, SerializerMixin):
#     __tablename__ = 'users'

#     serialize_rules = ('-recipes.user', '-_password_hash',)

#     id = db.Column(db.Integer, primary_key=True)
#     # user's username to be present and unique
#     username = db.Column(db.String, unique = True, nullable = False) 
#     _password_hash = db.Column(db.String)
#     image_url = db.Column(db.String)  
#     bio = db.Column(db.String)  

#     recipies = db.relationship('Recipe', backref='user')

# # incorporate bcrypt to create a secure password. Attempts to access the password_hash should be met with an AttributeError.
    
#     @hybrid_property
#     def password_hash(self):
#         raise AttributeError('Password hashes may not be viewed.')

    
#     @password_hash.setter
#     def password_hash(self, password):
#         password_hash = bcrypt.generate_password_hash(password.encode('utf-8'))
#         self._password_hash = password_hash.decode('utf-8')

#     def authentication(self, password):
#         return bcrypt.check_password_hash(self._pasword_hash, password.encode('utf-8'))
                                              
#     def __repr__(self):
#         return f'<User {self.username}>'

#     # @staticmethod
#     # def simple_hash(input):
#     #     return sum(bytearray(input, encoding = 'utf-8'))


# # a recipe belongs to a user

# class Recipe(db.Model, SerializerMixin):
#     __tablename__ = 'recipes'
#     __table_args__ = (db.CheckConstraint('length(instructions) >=50'), )

#     id = db.Column(db.Integer, primary_key=True)
#     title = db.Column(db.String, nullable = False)
#     instructions = db.Column(db.String, nullable = False)
#     minutes_to_complete = db.Column(db.Integer)

#     user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))
    
#     def __repr__(self):
#         return f'<Recipe {self.id}: {self.title}>'


from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy_serializer import SerializerMixin

from config import db, bcrypt

class User(db.Model, SerializerMixin):
    __tablename__ = 'users'

    serialize_rules = ('-recipes.user', '-_password_hash',)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String, unique=True, nullable=False)
    _password_hash = db.Column(db.String)
    image_url = db.Column(db.String)
    bio = db.Column(db.String)

    recipes = db.relationship('Recipe', backref='user')

    @hybrid_property
    def password_hash(self):
        raise AttributeError('Password hashes may not be viewed.')

    @password_hash.setter
    def password_hash(self, password):
        password_hash = bcrypt.generate_password_hash(
            password.encode('utf-8'))
        self._password_hash = password_hash.decode('utf-8')

    def authenticate(self, password):
        return bcrypt.check_password_hash(
            self._password_hash, password.encode('utf-8'))

    def __repr__(self):
        return f'<User {self.username}>'

class Recipe(db.Model, SerializerMixin):
    __tablename__ = 'recipes'
    __table_args__ = (
        db.CheckConstraint('length(instructions) >= 50'),
    )

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    instructions = db.Column(db.String, nullable=False)
    minutes_to_complete = db.Column(db.Integer)

    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Recipe {self.id}: {self.title}>'
    