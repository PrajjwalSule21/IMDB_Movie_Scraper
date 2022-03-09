import requests
from bs4 import BeautifulSoup
import pandas as pd


def imbd_movie_scaper(url, filename):
    """
    This function will scrape the data from IMDB movie site.

    It will take two arguments,
    url = url of a IMDB particualar genre page.
    filename = name of your .csv file in which data stored, always give .csv filename,
    or you can give a complete path of another directory in case if you wanted to save the file in different location.

    return: It will give the csv file of all the data which is extracted through IMDB specific genre page.
    """
    # create the connection to page
    page = requests.get(url)
    page.raise_for_status()
    soup = BeautifulSoup(page.content, "html.parser")
    movies = soup.find('div', class_="lister-list").find_all('div', class_='lister-item mode-advanced')

    # make a empty dataframe
    movie_df = pd.DataFrame(
        columns=['Movie Name', 'Movie Year', 'Movie Genre', 'Certificate', 'Runtime', 'Rating', 'Votes'])

    # Extract the data
    for movie in movies:
        # extract the movie name
        name = movie.find('h3', class_="lister-item-header").a.text

        # extract
        year = movie.find('span', class_="lister-item-year text-muted unbold").text.strip('()')

        genre = movie.find('span', class_='genre').text.replace('\n', '').strip(" ")
        try:
            certificate = movie.find('span', class_='certificate').text
        except:
            pass
        try:
            runtime = movie.find('span', class_='runtime').text
        except:
            pass
        try:
            rating = movie.find('div', class_='inline-block ratings-imdb-rating').strong.text
        except:
            pass
        try:
            votes = movie.find('p', class_='sort-num_votes-visible').text.replace('\n', '')[6:]
        except:
            pass

        # append all the data on that empty dataframe
        movie_df = movie_df.append(
            {'Movie Name': name, 'Movie Year': year, 'Movie Genre': genre, 'Certificate': certificate,
             'Runtime': runtime, 'Rating': rating, 'Votes': votes},
            ignore_index=True)

    # make .csv file of the dataframe
    movie_df.to_csv(filename, index=False)



# url = "https://www.imdb.com/search/title/?genres=comedy&explore=title_type,genres&pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=3396781f-d87f-4fac-8694-c56ce6f490fe&pf_rd_r=AQEARP5P1C1YP3SVQTQ0&pf_rd_s=center-1&pf_rd_t=15051&pf_rd_i=genre&ref_=ft_gnr_pr1_i_1"
# filename = 'Comedy_Movies.csv'
#
# imbd_movie_scaper(url, filename)


