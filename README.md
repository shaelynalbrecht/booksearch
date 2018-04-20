# booksearch
SI 206 Final Project

Hi, I'm Shaelyn Albrecht and this is my final project for SI 206!

My project allows users to search for books with specific keywords, and
then the program scrapes data from Goodreads in order to get the results.

Data Source:
  Goodreads.com
  (You don't need to do anything extra to be able to access the info
  from this website!)

Plotly:
  My program utilizes Plotly to provide visualizations of various
  information related to the book search results.
  In order to see these visualizations,
  you will need to install plotly and make a free plotly account!
  This website provides step-by-step instructions for doing so:
  https://plot.ly/python/getting-started/

Significant Data Processing Functions:
book_options():
  This function serves as the base for the interactive data viewing section
  of the program. Based on the user's input, this function calls one of four
  other functions (results_by_genre, average_ratings_by_genre, num_pages_distribution,
  or most_common_words).
  Each of the four functions makes calls to the database to select specific
  fields of information, which are then used to create plotly graphs! 

USER GUIDE:
  If this is your first time running the program, you will need to run it with
  --init. The program will ask you for keywords to search, and then it will
  populate a database with your search results. You can then move on to the data
  visualization portion of the program by typing "thanks".
  Additionally, if you have run the program before, but you want to search a new
  term, you will need to run it with --init. Otherwise, you will go right to the
  data visualization portion, and the visualizations will all be based on the
  most recent search results.
  NOTE: if you are running with --init and searching a term that is not already
  in the cache, be aware that it will probably take a really long time.
  (inside my function get_books_and_initialize, I have it set to stop scraping
    after 6 pages of results because otherwise it takes hours to load everything,
    but if you want more results, feel free to change the value from 6 to
    however many pages you'd like, but be aware that it will take a realllyy
    long time.)
  Once you're in the Data Visualization portion:
  If at any point you want to exit the program, simply type "exit".
  Otherwise, if you're ready to start visualizing data, type "Okay!"
  You will then be presented with several options.
