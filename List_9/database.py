from sqlalchemy import create_engine, Column, Integer, String, and_, or_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean


engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'book_list'
    title = Column(String(50), primary_key=True, nullable=False)
    author = Column(String(50), nullable=False)
    pub_year = Column(Integer, nullable=False)
    is_borrowed = Column(Boolean, nullable=False)

    def __str__(self):
        return '{}, {}, {}'.format(self.title, self.author, self.pub_year)


def create_base():
    Base.metadata.create_all(engine)
    session.commit()


def add_new_book(new_title, new_author, new_pub_year, new_borrowed=False):
    try:
        new_book = Book(title=new_title, author=new_author, pub_year=new_pub_year, is_borrowed=new_borrowed)
        session.add(new_book)
        session.commit()
    except Exception as e:
        return e


def return_book_list():
    book_list = []
    books = session.query(Book)
    for book in books:
        book_list.append([book.title, book.author, book.pub_year, book.is_borrowed])
    return book_list


def select_by_borrow(title, author):
    book = session.query(Book).filter(and_((Book.title == title), (Book.author == author))).one()
    return book.is_borrowed


def update_record(old_title, new_title, new_author, new_pub_year, new_borrowed):
    book = session.query(Book).filter(Book.title == old_title).one()
    book.title = new_title
    book.author = new_author
    book.pub_year = new_pub_year
    book.is_borrowed = new_borrowed
    session.commit()


def delete_book(title):
    book = session.query(Book).filter(Book.title == title).first()
    session.delete(book)
    session.commit()


def search_database(value):
    books = session.query(Book).filter(or_(Book.title.contains(value), Book.author.contains(value))).all()
    book_list = []
    for book in books:
        book_list.append([book.title, book.author, book.pub_year])
    return book_list
