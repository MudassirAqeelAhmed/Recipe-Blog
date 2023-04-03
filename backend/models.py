from exts import db

class Recipe(db.Model):
    """
    class Recipe:
        id:int primary key
        title: str
        description:str (Text)
    """
    id = db.Column(db.Integer(), primary_key=True)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.Text(), nullable=False)

    def __repr__(self) -> str:
        return f'<Recipe {self.title} >'

    def save(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self, title, description):
        self.title = title
        self.description = description
        db.session.commit()

class User(db.Model):
    """
    class User:
        id:int primary key
        username: str
        email:str 
        password: str
    """
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(25), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False)
    password = db.Column(db.String(60), nullable=False)

    def __repr__(self) -> str:
        return "<User: %s>" % self.username
    
    def save(self):
        db.session.add(self)
        db.session.commit()