from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Boolean, Table, Column, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

db = SQLAlchemy()

follower_table= Table(
    "follower_table",
    db.Model.metadata,
    Column("user_from_id", ForeignKey("user.id")),
    Column("user_to_id", ForeignKey("user.id"))
)


class User(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(20), unique= True, nullable=False)
    firstname: Mapped[str] = mapped_column(String(30), nullable=False)
    lastname: Mapped[str] = mapped_column(String(30), nullable= False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    posts: Mapped[list["Post"]] = relationship(back_populates="author")
    followers: Mapped[list["User"]]= relationship(
        "User",
        secondary= follower_table,
        primaryjoin= id == follower_table.c.user_from_id,
        secondaryjoin= id == follower_table.c.user_to_id,
        back_populates="following"
    )
    following: Mapped[list["User"]] = relationship(
        "User",
        secondary= follower_table,
        primaryjoin= id == follower_table.c.user_to_id,
        secondaryjoin= id == follower_table.c.user_from_id,
        back_populates= "followers"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email
            # do not serialize the password, its a security breach
    }


    
class Comment(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    comment_text: Mapped[str] = mapped_column(String(255), nullable=False)
    author: Mapped[int] = mapped_column(ForeignKey("user.id"))
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    post_comment: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return{
            "id": self.id,
            "comment_text": self.comment_text,
            "author": self.author,
            "post_id": self.post_id
        }
    

class Post(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    author_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[list["Comment"]] = relationship(back_populates="post_comment")
    medias: Mapped [list["Media"]] = relationship(back_populates="media_id")

    def serialize(self):
        return{
            "id": self.id,
            "author_id": self.author_id
        }

class Media(db.Model):
    id: Mapped[int] = mapped_column(primary_key=True)
    url: Mapped[str] = mapped_column(String(255), nullable=False)
    post_id: Mapped[int] = mapped_column(ForeignKey("post.id"))
    media_id: Mapped["Post"] = relationship(back_populates="medias")

    def serialize(self):
        return {
            "id": self.id,
            "url": self.url,
            "post_id": self.post_id
        }