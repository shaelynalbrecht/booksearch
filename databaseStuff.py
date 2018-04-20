import json
import sqlite3
import requests

def create_database():
    conn = sqlite3.connect('booksearch.db')
    cur = conn.cursor()

    # Drop tables
    statement = '''
        DROP TABLE IF EXISTS 'Books';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Authors';
    '''
    cur.execute(statement)
    statement = '''
        DROP TABLE IF EXISTS 'Genres';
    '''
    cur.execute(statement)
    conn.commit()

    statement = '''
        CREATE TABLE 'Books' (
                'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
                'Title' TEXT NOT NULL,
                'AuthorId' INTEGER,
                /*'Author' TEXT NOT NULL,*/
                'GenreId' INTEGER,
                /*'Genre' TEXT NOT NULL,*/
                'Rating' REAL NOT NULL,
                'NumPages' INTEGER NOT NULL,
                'Desc' TEXT NOT NULL
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Authors' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL,
            'AvgRating' REAL NOT NULL,
            'About' TEXT NOT NULL
        );
    '''
    cur.execute(statement)

    statement = '''
        CREATE TABLE 'Genres' (
            'Id' INTEGER PRIMARY KEY AUTOINCREMENT,
            'Name' TEXT NOT NULL
        );
    '''
    cur.execute(statement)

    conn.commit()
    conn.close()

#CREATE MAPPINGS
def insert_stuff(books, authors, genres):
    conn = sqlite3.connect('booksearch.db')
    cur = conn.cursor()
    for book in books:
        insertion = (None, book.title, 0, 0, book.rating, book.num_pages, book.description)
        #insertion = (None, book.title, 0, book.author, 0, book.genre, book.rating,
            #book.num_pages, book.description)
        statement = 'INSERT INTO "Books" '
        statement += 'VALUES (?, ?, ?, ?, ?, ?, ?)'
        #statement += 'VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()

    for author in authors:
        insertion = (None, author.name, author.avgrating,
            author.about)
        statement = 'INSERT INTO "Authors" '
        statement += 'VALUES (?, ?, ?, ?)'
        cur.execute(statement, insertion)

    conn.commit()

    statement = '''
        DELETE
        FROM Authors
        where  id not in (
            select min(id)
            from   authors
            group  by Name
            )
    '''
    cur.execute(statement)
    conn.commit()

    for genre in genres:
        insertion = (None, genre)
        statement = 'INSERT INTO "Genres" '
        statement += 'VALUES (?, ?)'
        cur.execute(statement, insertion)

    statement = '''
        DELETE
        FROM Genres
        where  id not in (
            select min(id)
            from   Genres
            group  by Name
            )
    '''
    cur.execute(statement)

    conn.commit()
    conn.close()


def update_stuff(books):
    conn = sqlite3.connect('booksearch.db')
    cur = conn.cursor()

    statement = '''
        SELECT * FROM Authors
    '''

    cur.execute(statement)
    author_mapping = {}

    for author in cur:
        author_id = author[0]
        name = author[1]
        author_mapping[name] = author_id

    conn.commit()

    statement = '''
        SELECT * FROM Genres
    '''

    cur.execute(statement)
    genre_mapping = {}

    for genre in cur:
        genre_id = genre[0]
        name = genre[1]
        genre_mapping[name] = genre_id

    conn.commit()

    for author in author_mapping:
        author_id = author_mapping[author]
        count = 1
        bookid = 1
        for book in books:
            if book.author == author:
                bookid = count
                insert = (author_id, bookid)
                statement = '''
                    UPDATE Books
                    SET AuthorId =?
                    WHERE Id =?
                '''
                cur.execute(statement, insert)
                conn.commit()
            count += 1

    for genre in genre_mapping:
        genre_id = genre_mapping[genre]
        count = 1
        bookid = 1
        for book in books:
            if book.genre == genre:
                bookid = count
                insert = (genre_id, bookid)
                statement = '''
                    UPDATE Books
                    SET GenreId =?
                    WHERE Id =?
                '''
                cur.execute(statement, insert)
                conn.commit()
            count += 1

    conn.close()
