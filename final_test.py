import unittest
from final import *

class TestClasses(unittest.TestCase):
    def testConstructorBookAuthor(self):
        b1 = Book("Cool Book", "Shaelyn", "Awesome", 5, 100,
                    "This book is amazing. Wow. - Shaelyn")
        self.assertEqual(b1.title, "Cool Book")
        self.assertEqual(b1.rating, 5)

        a1 = Author("Shaelyn", 5, "Shaelyn is amazing. Wow.")
        self.assertEqual(a1.name, "Shaelyn")
        self.assertEqual(a1.about, "Shaelyn is amazing. Wow.")

class TestDatabaseBasic(unittest.TestCase):

    def test_tables_basic(self):
        conn = sqlite3.connect('dancetestresults.db')
        cur = conn.cursor()

        sql = 'SELECT Title FROM Books'
        results = cur.execute(sql)
        result_list = results.fetchall()
        real_results = []
        for r in result_list:
            real_results.append(r[0])
        self.assertIn('Dance Dance Dance (The Rat, #4)', real_results)
        self.assertEqual(len(result_list), 400)

        sql = 'SELECT Name FROM Authors'
        results = cur.execute(sql)
        result_list = results.fetchall()
        real_results = []
        for r in result_list:
            real_results.append(r[0])
        self.assertIn('Haruki Murakami', real_results)
        self.assertEqual(len(result_list), 344)

        sql = '''
            SELECT Title, Rating, NumPages
            FROM Books
            WHERE Rating > 4
            ORDER BY Rating DESC
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        #print(result_list)
        self.assertEqual(len(result_list), 163)
        self.assertEqual(result_list[24][1], 4.33)

        conn.close()

class TestDatabaseComplex(unittest.TestCase):
    def test_tables_with_joins(self):
        conn = sqlite3.connect('dancetestresults.db')
        cur = conn.cursor()

        sql = '''
            SELECT Title, Name
            FROM Books
            JOIN Authors
            ON Books.AuthorId = Authors.Id
            WHERE AvgRating > 4
        '''
        results = cur.execute(sql)
        result_list = results.fetchall()
        self.assertEqual(result_list[119][0], 'The Volcano Dancer')
        self.assertEqual(result_list[119][1], 'Brad Keena')
        self.assertEqual(len(result_list), 123)

        sql = '''
            SELECT Title, Name
            FROM Books
            JOIN Genres
            ON Books.GenreId = Genres.Id
        '''
        results = cur.execute(sql)

    def test_tables_with_agg(self):
        conn = sqlite3.connect('dancetestresults.db')
        cur = conn.cursor()
        sql = '''
            SELECT COUNT(*)
            FROM Genres
        '''
        results = cur.execute(sql)
        count = results.fetchone()[0]
        self.assertEqual(count, 45)

        sql = '''
            SELECT Genres.Name, Avg(Rating)
            FROM Books
            JOIN Genres
            ON Books.GenreId = Genres.Id
            GROUP BY Name
            ORDER BY Avg(Rating) DESC LIMIT 10
        '''
        results = cur.execute(sql)
        count = results.fetchone()
        genre = count[0]
        rating = count[1]
        self.assertEqual(genre, 'Art')
        self.assertEqual(rating, 4.63)
        conn.close()


unittest.main()
