# https://www.knowledgehut.com/blog/programming/sys-argv-python-examples
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import Boolean
import argparse
import sys

engine = create_engine('sqlite:///library.db')
Session = sessionmaker(bind=engine)
session = Session()
Base = declarative_base()


class Book(Base):
    __tablename__ = 'book_list'
    title = Column(String(50), primary_key=True)
    author = Column(String(50))
    pub_year = Column(Integer)
    is_borrowed = Column(Boolean)

    def __str__(self):
        return '{}, {}, {}'.format(self.title, self.author, self.pub_year)


class Friend(Base):
    __tablename__ = 'friend_list'
    first_name = Column(String(50))
    last_name = Column(String(50))
    e_mail = Column(String(100), primary_key=True)

    def __str__(self):
        return '{}, {}, {}'.format(self.first_name, self.last_name, self.e_mail)


class BorrowedBooks(Base):
    __tablename__ = 'borrowed_books'
    id = Column(Integer, primary_key=True)
    title = Column(String(50))
    author = Column(String(50))
    pub_year = Column(Integer)
    e_mail = Column(String(100))


def create_base():
    Base.metadata.create_all(engine)
    session.commit()

create_base()

def add_new_book():
    title = input("Type new book title: ")
    author = input("type new book author: ")
    pub_year = int(input("Type new book publication year: "))
    try:
        new_book = Book(title=title, author=author, pub_year=pub_year, is_borrowed=False)
        session.add(new_book)
        session.commit()
    except Exception as e:
        return e


def display_book_list():
    books = session.query(Book)
    for book in books:
        print(book)


def select_by_title(title):
    book = session.query(Book).filter(Book.title == title).one()
    return book


def select_by_borrow():
    books = session.query(Book).filter(Book.is_borrowed == False)
    return books


def add_new_friend():
    first_name = input("Type first name of a new friend: ")
    last_name = input("Type last name of a new friend: ")
    new_friend = Friend(first_name=first_name, last_name=last_name,
                        e_mail='{}.{}@gmail.com'.format(first_name, last_name))
    session.add(new_friend)
    session.commit()


def display_friend_list():
    friends = session.query(Friend)
    for friend in friends:
        print(friend)


def borrow_a_book():
    first_name = input("Type your first name: ")
    last_name = input("Type your last name: ")
    e_mail = '{}.{}@gmail.com'.format(first_name, last_name)
    friend = session.query(Friend).filter(Friend.e_mail == e_mail).one()
    print("Available books: ")
    book_list = select_by_borrow()
    for book in book_list:
        print(book)
    title = input("Type a book that you want to borrow: ")
    book = select_by_title(title)
    book.is_borrowed = True
    borrowed = BorrowedBooks(title=book.title, author=book.author, pub_year=book.pub_year, e_mail=friend.e_mail)
    session.add(borrowed)
    session.commit()


def display_borrowed_books():
    first_name = input("Type your first name: ")
    last_name = input("Type your last name: ")
    e_mail = '{}.{}@gmail.com'.format(first_name, last_name)
    print("Borrowed books: ")
    borrowed_list = session.query(BorrowedBooks).filter(BorrowedBooks.e_mail == e_mail)
    for book in borrowed_list:
        print(book.title, book.author, book.pub_year)


def return_borrowed_book():
    display_borrowed_books()
    title = input("Type title of a book that you want to return: ")
    borrowed_book = session.query(BorrowedBooks).filter(BorrowedBooks.title == title).one()
    session.delete(borrowed_book)
    book = session.query(Book).filter(Book.title == title).one()
    book.is_borrowed = False
    session.commit()


parser = argparse.ArgumentParser()
subparsers = parser.add_subparsers()

parser_add_new_book = subparsers.add_parser('add_new_book', help="Add a new book to the library")
parser_add_new_book.set_defaults(func=add_new_book)

parser_display_book_list = subparsers.add_parser('display_book_list', help="Display a list of books")
parser_display_book_list.set_defaults(func=display_book_list)

parser_add_new_friend = subparsers.add_parser('add_new_friend', help="Add a new friend to the database")
parser_add_new_friend.set_defaults(func=add_new_friend)

parser_display_friend_list = subparsers.add_parser('display_friend_list', help="Display list of friends")
parser_display_friend_list.set_defaults(func=display_friend_list)

parser_borrow_a_book = subparsers.add_parser('borrow_book', help="Borrow a book")
parser_borrow_a_book.set_defaults(func=borrow_a_book)

parser_display_borrowed_book = subparsers.add_parser('display_borrowed', help="Display borrowed books")
parser_display_borrowed_book.set_defaults(func=display_borrowed_books)

parser_return_book = subparsers.add_parser('return_book', help="Return borrowed books")
parser_return_book.set_defaults(func=return_borrowed_book)

if len(sys.argv) <= 1:
    sys.argv.append('--help')

options = parser.parse_args()
options.func()
