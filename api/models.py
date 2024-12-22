from sqlalchemy import Column, Integer, String
from api.services.db_service import Base

class Song(Base):
    __tablename__ = 'song'

    id = Column(Integer, primary_key=True)
    title = Column(String(255), nullable=False)
    artist = Column(String(255), nullable=False)

    def __repr__(self):
        return f'<Song {self.title} by {self.artist}>'

class Playlist(Base):
    __tablename__ = 'playlist'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    created_at = Column(String(255))

    def __repr__(self):
        return f'<Playlist {self.name}>'

class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)

    def __repr__(self):
        return f'<User {self.username}>'