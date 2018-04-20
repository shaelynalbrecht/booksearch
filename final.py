# Shaelyn Albrecht
# Welcome to my Final Project for SI 206!!
# I hope you enjoy your time here :)
import json
import sqlite3
import requests
from bs4 import BeautifulSoup
from os import path
from wordcloud import WordCloud
import plotly.plotly as py
import plotly.graph_objs as go
import sys
from caching import *
from databaseStuff import *
import re
from Book import Book
from Author import Author

def get_soup(search):
     baseurl1 = "https://www.goodreads.com/search?"
     params_diction_1 = {}
     params_diction_1["q"] = search
     params_diction_1["search_type"] = "books"
     results = make_request_using_cache(baseurl1, params_diction_1)
     soup = BeautifulSoup(results, "html.parser")
     return soup

# returns a tuple with a list of Book objects,
# a list of Author objects, and a list of Genres
def get_books_and_initialize(soup):
    books = []
    authors = []
    genres = []
    baseurl = "https://www.goodreads.com"
    check = "yes"
    count = 1
    while check == "yes":
        print("getting info")
        table = soup.find('table')
        results = table.find_all('tr')
        for r in results:
            print("getting a book")
            tds = r.find_all('td')
            title = r.find(class_='bookTitle').text
            author = r.find(class_='authorName').text

            urls = tds[1].find_all('a')
            #Go to individual book to get description & rating & NumPages & genre
            book_url_end = urls[0]['href']
            book_url = baseurl + book_url_end
            one_book = make_request_using_cache2(book_url)
            one_book_soup = BeautifulSoup(one_book, "html.parser")
            try:
                rating = float(one_book_soup.find(class_='average').text)
            except:
                rating = 0
            try:
                num_pages = one_book_soup.find(itemprop="numberOfPages").text
                num_pages = int(num_pages[:num_pages.find("pages")])
            except:
                num_pages = 0
            try:
                genre = one_book_soup.find(class_="actionLinkLite bookPageGenreLink").text
            except:
                genre = "None"
            try:
                desc = one_book_soup.find(class_="readable stacked")
                desc2 = desc.find_all('span')
                description = desc2[1].text
            except:
                try:
                    description = one_book_soup.find(class_="readable stacked").text
                except:
                    description = "No description."
            b = Book(title, author, genre, rating, num_pages, description)
            books.append(b)

            #Go to author to get author info
            author_url = urls[1]['href']
            author_info = make_request_using_cache2(author_url)
            author_soup = BeautifulSoup(author_info, "html.parser")
            avgrating = float(author_soup.find(class_='average').text)
            try:
                about1 = author_soup.find(class_='aboutAuthorInfo')
                about2 = about1.find_all('span')
                about = about2[1].text
            except:
                about = author_soup.find(class_='aboutAuthorInfo').text
            a = Author(author, avgrating, about)
            authors.append(a)

            genres.append(genre)

        count += 1
        if count > 6:
            check = "no"

        is_there_a_next = soup.find(class_="next_page disabled")
        if is_there_a_next != None:
            check = "no"
            #print("this is the last page")
        else:
            #print("there's still a next page")
            try:
                find_next_page = soup.find(class_="next_page")
                next_page = find_next_page['href']
                print(next_page)
                next_page_url = baseurl + next_page
                next_page_results = make_request_using_cache2(next_page_url)
                soup = BeautifulSoup(next_page_results, "html.parser")
            except:
                break

    return books, authors, genres

# what percentage of the search results are in each genre
# pie chart
def results_by_genre():
    conn = sqlite3.connect('booksearch.db')
    cur = conn.cursor()
    statement = '''
        SELECT G.Name, Count(*)
        FROM Books
        JOIN Genres AS G
        ON GenreId = G.Id
        GROUP BY G.Name
    '''
    cur.execute(statement)
    labels = []
    values = []
    for row in cur:
        labels.append(row[0])
        values.append(row[1])

    trace = go.Pie(labels=labels, values=values,
                   hoverinfo='label+percent', textinfo='value',
                   textfont=dict(size=20),
                   marker=dict(#colors=colors,
                               line=dict(color='#000000', width=2)))

    py.plot([trace], filename='styled_pie_chart')

    statement = '''
        SELECT Count(*)
        FROM Genres
    '''
    count = cur.execute(statement)
    count = count.fetchone()[0]
    if count > 10:
        print("Your results have more than 10 genres!")
        command = input("Would you like to see a list of the 10 most common genres? (y/n): ")
        if command == "y":
            statement = '''
                SELECT G.Name
                FROM Books
                JOIN Genres AS G
                ON GenreId = G.Id
                GROUP BY G.Name
                ORDER BY Count(*) DESC LIMIT 10
            '''
            cur.execute(statement)
            count = 1
            for row in cur:
                print(str(count) + ". " + row[0])
                count += 1



    conn.close()

# what the average ratings are for each genre of the books in the search results
# bar chart
def average_ratings_by_genre(search):
    conn = sqlite3.connect('booksearch.db')
    cur = conn.cursor()

    statement = '''
        SELECT G.Name, Avg(Rating)
        FROM Books
        JOIN Genres AS G
        ON GenreId = G.Id
        GROUP BY G.Name
    '''
    cur.execute(statement)

    x = []
    y = []
    text = []

    for row in cur:
        x.append(row[0])
        y.append(row[1])
        txt = str(row[1]) + " stars"
        text.append(txt)

    trace0 = go.Bar(
    x=x,
    y=y,
    text=text,
    marker=dict(
        color='rgb(158,202,225)',
        line=dict(
            color='rgb(8,48,107)',
            width=1.5,
            )
            ),
            opacity=0.6
            )

    data = [trace0]
    layout = go.Layout(
        title='Average Ratings by Genre for books in search results for: ' + search,
        )

    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename='text-hover-bar')

    command = input("Do you want to see the highest rated book for a specific genre? (y/n): ")
    while command != "n":
        command = input("Type the name of the genre: ")
        print()
        statement = '''
            SELECT Title, Authors.Name, Genres.Name, Rating, NumPages, [Desc],
            Authors.AvgRating, Authors.About
            FROM Books
            JOIN Genres
            ON Books.GenreId = Genres.Id
            JOIN Authors
            ON Books.AuthorId = Authors.Id
            WHERE Genres.Name == "{}"
            ORDER BY Rating DESC LIMIT 1
        '''.format(command)
        results = cur.execute(statement)
        r = results.fetchone()
        hrbook = Book(r[0], r[1], r[2], r[3], r[4], r[5])
        hrauthor = Author(r[1], r[6], r[7])
        print(hrbook)
        print()
        command = input("Do you want to see info about this author? (y/n): ")
        if command == "y":
            print()
            print(hrauthor)
            print()
        command = input("Do you want to look up another genre? (y/n): ")

    conn.close()


# distribution of the number of pages of books in the search results
# a histogram
def num_pages_distribution():
    conn = sqlite3.connect('booksearch.db')
    cur = conn.cursor()

    statement = '''
        SELECT NumPages
        FROM Books
    '''
    cur.execute(statement)

    x = []
    for row in cur:
        x.append(row[0])

    data = [go.Histogram(x=x)]

    py.plot(data, filename='NumPages histogram')

    command = input("Would you like more specifics? (y/n): ")
    if command == "y":
        print("Do you want to see info for the book")
        print("with the maximum or minimum # of pages?")
        command = input("(Max/Min): ")
        print()
        statement = '''
            SELECT {}(NumPages)
            FROM Books
        '''.format(command)
        results = cur.execute(statement)
        r = results.fetchone()[0]
        statement = '''
            SELECT Title, a.Name, g.Name, Rating, NumPages, [Desc], a.AvgRating,
            a.About
            FROM Books
            JOIN Authors as a
            ON Books.AuthorId = a.Id
            JOIN Genres as g
            ON Books.GenreId = g.Id
            WHERE NumPages = {}
        '''.format(r)
        results = cur.execute(statement)
        r = results.fetchone()
        maxminbook = Book(r[0], r[1], r[2], r[3], r[4], r[5])
        maxminauthor = Author(r[1], r[6], r[7])
        print(maxminbook)
        print()
        command = input("Do you want to see info about this author? (y/n): ")
        if command == "y":
            print()
            print(maxminauthor)
            print()

    conn.close()

# most commonly used words in the descriptions
# word cloud
def most_common_words():
    conn = sqlite3.connect('booksearch.db')
    cur = conn.cursor()
    statement = '''
        SELECT [Desc]
        FROM Books
    '''
    cur.execute(statement)
    words = ''
    for row in cur:
        words += row[0]
        words += " "

    # Generate a word cloud image
    wordcloud = WordCloud().generate(words)

    # Display the generated image:
    # the matplotlib way:
    import matplotlib.pyplot as plt
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # lower max_font_size
    wordcloud = WordCloud(max_font_size=40).generate(words)
    plt.figure()
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")
    plt.show()

def print_help():
    print('****************************************************')
    print('*            Yay for Data Visualization!!          *')
    print('*                                                  *')
    print('*                 Type "1" to see:                 *')
    print('*         What percent of the search results       *')
    print('*                are in each genre                 *')
    print('*                                                  *')
    print('*                 Type "2" to see:                 *')
    print('*        The average ratings for each genre        *')
    print('*                                                  *')
    print('*                 Type "3" to see:                 *')
    print('*         A distribution of the # of pages         *')
    print('*        that the books in the results have        *')
    print('*                                                  *')
    print('*                 Type "4" to see:                 *')
    print('*            A wordcloud visualization of          *')
    print('*            the most commonly used words          *')
    print('*              in the book descriptions!           *')
    print('*                                                  *')
    print('*         (type "exit" if you want to leave)       *')
    print('*                                                  *')

def book_options(books, authors, genres, search):
    print_help()
    print('*      (type "help" if you forget these choices)   *')
    print('*                                                  *')
    option = input("What do you want to do? ")

    while option != "exit":
        if option == "1":
            results_by_genre()
        elif option == "2":
            average_ratings_by_genre(search)
        elif option == "3":
            num_pages_distribution()
        elif option == "4":
            most_common_words()
        elif option == "help":
            print_help()
        else:
            print("Please enter a valid command!")
        option = input("Now what do you want to do? ")

if __name__ == "__main__":
    print("*********** Welcome to my final project! ***********")
    print("*                                                  *")

    books = []
    authors = []
    genres = []

    if len(sys.argv) > 1 and sys.argv[1] == '--init':
        print('*     Deleting DB and starting over from scratch   *')
        file = open('currentdatabase.txt', 'w')
        create_database()
        print('****************************************************')
        print('*            Hey, please enter a search            *')
        print('*           term if you want to see books          *')
        print('*           with your term(s) in the title!        *')
        print('*                                                  *')
        print('*                                                  *')
        search_term = input('********** keywords: ')
        while search_term != 'thanks':
            create_database()
            print("Collecting book results for: " + search_term + "!!")
            soup = get_soup(search_term)
            books, authors, genres = get_books_and_initialize(soup)
            insert_stuff(books, authors, genres)
            update_stuff(books)
            #book_options(books, authors, genres, words)
            file.write(search_term)

            print('***          Your search results are in!           *')
            print('*         Enter "thanks" if you\'re ready to        *')
            print('*           move on to data visualization          *')
            print('')
            search_term = input('*** Enter "thanks" to move on: ')

        file.close()

    file = open('currentdatabase.txt', 'r')
    currentdatabase = file.read()

    print()
    print('****************************************************')
    print('*       Welcome to the ~Super~ Informative         *')
    print('*                  Book Search!!                   *')
    print('*         (The Interactive Portion! :D )           *')
    print('*                                                  *')
    print('*            Your database currently               *')
    print('*           holds info for books with:             *')
    print(currentdatabase)
    print('*                                                  *')
    print('*           To get data for a different            *')
    print('*           keyword(s), please exit and            *')
    print('*            rerun with --init in the              *')
    print('*                  command line.                   *')
    print('*                                                  *')
    print('*                                                  *')
    print('*              Okay, let\'s look at                 *')
    print('*                  some graphs!                    *')
    print('*             Enter "Okay!" to start,              *')
    print('*               or "exit" to leave.                *')
    print()
    command = input("Response : ")

    while command != "yes" and command != "exit":
        if command == "Okay!" or command == "no":
            book_options(books, authors, genres, currentdatabase)

        command = input("Are you sure you want to quit? (yes/no): ")
        if command == "yes":
            print("Okay :(")
        else:
            print("Yay! Let's look at more data! ")
            print()
    print("Bye, thanks for coming!")
