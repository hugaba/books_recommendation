from sklearn.neighbors import NearestNeighbors
from scipy.sparse import csr_matrix
import pandas as pd
import numpy as np

# load matrix user_matrix
loader = np.load('data/csr_matrix.npz')
book_matrix = csr_matrix((loader['data'], loader['indices'], loader['indptr']), shape=loader['shape'])

# load datasets
# ratings
ratings = pd.read_csv('data/ratings.csv')
# books_with_cat
books = pd.read_csv('data/books_with_cat.csv')


def get_n_nearest_users(user_index: int, n_users: int) -> list:
    """
    get top n nearest users
    :book_matrix: csr_matrix: car_matrix of ratings of users
    :user_index: int: index of reference user to get nearest user from
    :n_users: int: number of nearest user to return
    :return: list: list of nearest users
    """
    # instantiate NearestNeighbors algorithm
    recommender = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=n_users).fit(book_matrix)
    # find 'n_users' nearest users from 'user_index' user
    _, nearest_user = recommender.kneighbors([book_matrix.toarray()[user_index - 1]])

    similar_user = []
    for arr in nearest_user:
        for user in arr:
            similar_user.append(user + 1)

    return similar_user


def get_top_n_books_nearest_users(nearest_users_ids: list, n_books: int) -> list:
    """
    get top n nearest books for user
    :nearest_users_ids: list: list of users
    :n_books: int: number of books to return
    :return: list: list of top n_books ids
    """
    # select reference user from nearest_users_ids (nearest_users_id[0] is the reference user aka the closest to itself)
    base_user = ratings[ratings['user_id'] == nearest_users_ids[0]]
    # select nearest users
    nearest_users = ratings[ratings['user_id'].isin(nearest_users_ids[1:])]
    unread_books = []
    # get list of books which have not been read by base_user
    for book in nearest_users['book_id'].unique():
        if not (book in base_user['book_id'].unique()):
            unread_books.append(book)
    top_books = []

    for book in unread_books:
        # creation of variables needed to calculate weighted_rating
        # minimum count numbers for each book
        minimum_book_count = 3
        # number of time the book has been rated by nearest users
        book_count = len(nearest_users[nearest_users['book_id'] == book])
        # average rating of the book by nearest users
        avg_book_rating = nearest_users['rating'][nearest_users['book_id'] == book].sum(axis=0) / book_count
        # total number of ratings of nearest users
        nb_rating = len(nearest_users)
        # average rating of all nearest users
        avg_rating = nearest_users['rating'].sum(axis=0) / nb_rating
        # using weighted_rating formula from IMDB
        # https://www.datacamp.com/community/tutorials/recommender-systems-python
        weighted_rating = (book_count * avg_book_rating / (
                book_count + minimum_book_count)) + minimum_book_count * avg_rating / (
                                  book_count + minimum_book_count)
        top_books.append(weighted_rating)
    top_books_dict = {
        'book_id': unread_books,
        'rating': top_books
    }
    df = pd.DataFrame.from_dict(top_books_dict).sort_values(by=['rating'], ascending=False)
    return df['book_id'][:n_books].values


def get_top_n_books_by_category(category: str, n_books: int, user_id: int = None) -> list:
    """
    get top n nearest books in a specific category
    :category: str: category of the book
    :n_books: int: number of books to return
    :return: list: list of top n_books ids
    """
    # get list of books already read by user (if new user user_id = None and read_books stay empty)
    read_books = []
    if user_id is not None:
        read_books = ratings[ratings['user_id'] == user_id]['book_id'].unique()

    # select books in the required category
    cat_books = books[(books['category'] == category) & (books['average_rating'] > 4.5)]
    if not len(cat_books) > 5:
        cat_books = books[(books['category'] == category) & (books['average_rating'] > 3.5)]
    # select only the books which aren't in the read_books list
    cat_books = cat_books[~cat_books['book_id'].isin(read_books)]

    top_books = []

    # minimum count numbers for each book
    minimum_book_count = 3
    # total number of ratings of nearest users
    nb_rating = len(ratings)
    # average rating of all nearest users
    avg_rating = ratings['rating'].sum(axis=0) / nb_rating

    for book_id in cat_books['book_id'].unique():
        # creation of variables needed to calculate weighted_rating
        # number of time the book has been rated
        book_count = cat_books[cat_books['book_id'] == book_id]['work_ratings_count'].values[0]
        # average rating of the book by nearest users
        avg_book_rating = cat_books[cat_books['book_id'] == book_id]['average_rating'].values[0]

        # using weighted_rating formula from IMDB
        # https://www.datacamp.com/community/tutorials/recommender-systems-python
        weighted_rating = (book_count * avg_book_rating / (
                book_count + minimum_book_count)) + minimum_book_count * avg_rating / (
                                  book_count + minimum_book_count)
        top_books.append(weighted_rating)
    top_books_dict = {
        'book_id': cat_books['book_id'].unique(),
        'rating': top_books
    }
    df = pd.DataFrame.from_dict(top_books_dict).sort_values(by=['rating'], ascending=False)
    return df['book_id'][:n_books].values


def get_top_n_books(n_books: int, user_id: int = None) -> list:
    """
    get top n  books
    :n_books: int: number of books to return
    :return: list: list of top n_books ids
    """
    # get list of books already read by user (if new user user_id = None and read_books stay empty)
    read_books = []
    if user_id is not None:
        read_books = ratings[ratings['user_id'] == user_id]['book_id'].unique()

    # select books
    best_books = books[books['average_rating'] > 4.5]
    # select only the books which arn't in the read_books list
    best_books = best_books[~best_books['book_id'].isin(read_books)]

    top_books = []

    # minimum count numbers for each book
    minimum_book_count = 3
    # total number of ratings of nearest users
    nb_rating = len(ratings)
    # average rating of all nearest users
    avg_rating = ratings['rating'].sum(axis=0) / nb_rating

    for book_id in best_books['book_id'].unique():
        # creation of variables needed to calculate weighted_rating
        # number of time the book has been rated
        book_count = best_books[best_books['book_id'] == book_id]['work_ratings_count'].values[0]
        # average rating of the book by nearest users
        avg_book_rating = best_books[best_books['book_id'] == book_id]['average_rating'].values[0]

        # using weighted_rating formula from IMDB
        # https://www.datacamp.com/community/tutorials/recommender-systems-python
        weighted_rating = (book_count * avg_book_rating / (
                book_count + minimum_book_count)) + minimum_book_count * avg_rating / (
                                  book_count + minimum_book_count)
        top_books.append(weighted_rating)
    top_books_dict = {
        'book_id': best_books['book_id'].unique(),
        'rating': top_books
    }
    df = pd.DataFrame.from_dict(top_books_dict).sort_values(by=['rating'], ascending=False)
    return df['book_id'][:n_books].values


def get_top_author(user_id: int, n: int = 1) -> str:
    """
    get top author for a user
    :user_id: int: id of user
    :n: int: number of author to return
    :return: str: top author
    """
    user_rating = ratings[ratings["user_id"] == user_id]

    # merge dataframe
    df = user_rating.merge(books, on="book_id", suffixes=('_left', '_right'))

    df_by_author = df.groupby("authors").mean()
    df_by_author = df_by_author.rename(columns={"rating": "rating_moyen_par_user"})

    df = df[["book_id", "authors"]].groupby("authors").count().sort_values(by=['book_id'], ascending=False)
    df["pourcentage-occurence"] = df.apply(lambda row: (row["book_id"] / (len(user_rating)) * 100), axis=1)

    # merge dataframe with dataframe modified
    df = df.merge(df_by_author, on="authors", suffixes=('_left', '_right'))
    df["note_x_occurence"] = df["rating_moyen_par_user"] * df["pourcentage-occurence"]
    df.sort_values(by=['note_x_occurence'], ascending=False)

    # deplace feature "note_x_occurence" at the beginning
    note_x_occurence = df['note_x_occurence']
    df.drop(labels=['note_x_occurence'], axis=1, inplace=True)
    df.insert(0, 'note_x_occurence', note_x_occurence)

    # keep N best author for the user
    result = df.note_x_occurence[:n].index

    return result[0]


def get_top_n_books_by_author(author: str, user_id: int, n_books: int) -> list:
    """
    get top n nearest books in a specific category
    :author: str: author of the book
    :user_id: int: id of user
    :n_books: int: number of books to return
    :return: list: list of top n_books ids
    """
    # get list of books already read by user (if new user user_id = None and read_books stay empty)
    read_books = []
    if user_id is not None:
        read_books = ratings[ratings['user_id'] == user_id]['book_id'].unique()

    # select books by the required author
    df_books_auteur = books[books["authors"] == author]
    # select only the books which arn't in the read_books list
    df_books_auteur = df_books_auteur[~df_books_auteur['book_id'].isin(read_books)]

    top_books = []

    # minimum count numbers for each book
    minimum_book_count = 3
    # total number of ratings of nearest users
    nb_rating = len(ratings)
    # average rating of all nearest users
    avg_rating = ratings['rating'].sum(axis=0) / nb_rating

    for book_id in df_books_auteur['book_id'].unique():
        # creation of variables needed to calculate weighted_rating
        # number of time the book has been rated
        book_count = df_books_auteur[df_books_auteur['book_id'] == book_id]['work_ratings_count'].values[0]
        # average rating of the book by nearest users
        avg_book_rating = df_books_auteur[df_books_auteur['book_id'] == book_id]['average_rating'].values[0]

        # using weighted_rating formula from IMDB
        # https://www.datacamp.com/community/tutorials/recommender-systems-python
        weighted_rating = (book_count * avg_book_rating / (
                book_count + minimum_book_count)) + minimum_book_count * avg_rating / (
                                  book_count + minimum_book_count)
        top_books.append(weighted_rating)
    top_books_dict = {
        'book_id': df_books_auteur['book_id'].unique(),
        'rating': top_books
    }
    df = pd.DataFrame.from_dict(top_books_dict).sort_values(by=['rating'], ascending=False)
    return df['book_id'][:n_books].values


def get_book_name(books_id: list) -> list:
    books_name = []
    for book_id in books_id:
        book_name = books['title'][books['book_id'] == book_id].values
        books_name.append(book_name[0])
    return books_name


categories = ['action & adventure', 'fantasy', 'romance', 'mystery & thriller', 'classic',
              'memoir & autobiography', 'historical fiction', 'graphic novel & comic',
              'science fiction', 'history', 'horror', "children's", 'science', 'humor',
              'self development', 'dystopia', 'paranormal romance', 'anthology', 'poetry',
              'cookbooks', 'essay', 'drama', 'other']

HTML = """
        <html>
            <head>
                <title>Some HTML in here</title>
                <link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/3.4.1/css/bootstrap.min.css">
            </head>
            <body>
                <a href="http://127.0.0.1:8000/recommandation" class="btn btn-info" role="button">Home page</a>
        """

END = """
        </body>
    </html>
"""

NEAREST_USER_HTML = """
                    <div class="text-center">
                    <hr/>
                        <p class="h3">
                            Top books based on your nearest users
                        </p>
                    <hr/>
                    </div>
                        """

GENERAL_HTML = """
                    <div class="text-center">
                    <hr/>
                        <p class="h3">
                            General Top books
                        </p>
                    <hr/>
                    </div>
                        """


def get_pictures(book_list: list) -> str:
    """
    create the html for displaying the picture of books
    :param book_list: list: list of book ids
    :return: str: html book pictures
    """
    html = """
            <div class="form-group row">
                <div class="col-sm-1"></div>
    """
    for id in range(len(book_list)):
        html += f"""
                        <div class="col-sm-2">
                                <img src="{books[books['book_id'] == book_list[id]]['image_url'].values[0]}" class="center-block">
                        </div>
                        """
    html += """
                <div class="col-sm-1"></div>
            </div>
    """
    return html


def get_html_names(book_list: list) -> str:
    """
    create html book titles
    :param book_list: list: list of books title
    :return: str: html book names
    """
    html = """
            <div class="form-group row">
                <div class="col-sm-1"></div>
    """
    for id in range(len(book_list)):
        html += f"""
                    <div class="text-center">
                        <div class="col-sm-2">
                            {book_list[id]}
                        </div>
                    </div>
                """
    html += """
                <div class="col-sm-1"></div>
            </div>
    """
    return html


def get_html_author(author: str) -> str:
    """
    create html header for author
    :param author: str: author name
    :return: str: html title for author
    """
    return f"""
                <div class="text-center">
                <hr/>
                    <p class="h3">
                        Top books based on your favorite author {author}
                    </p>
                <hr/>
                </div>
                """


def get_html_category(category: list, cat_row: int = 0) -> str:
    """
    create the html header for category
    :param category: list: list of book categories
    :param cat_row: int: index of category row (used for displaying all categories)
    :return: str: html title for category
    """
    if len(category) == 1:
        return f"""
                <div class="text-center">
                <hr/>
                    <p class="h3">
                        Top books based on the {category[0]} category
                    </p>
                <hr/>
                </div>
                """
    else:
        html = ''
        if cat_row == 0:
            html += f"""
                <div class="text-center">
                <hr/>
                    <p class="h3">
                        Top books by category
                    </p>
                <hr/>
                </div>
                """
        html += """
                <div class="form-group row">
                    <div class="col-sm-1"></div>
                """
        for cat in category:
            html += f"""
                    <div class="text-center">
                        <div class="col-sm-2">
                            <p class="h4">
                                {cat}
                            </p>
                        </div>
                    </div>"""
        html += """
                    <div class="col-sm-1"></div>
                </div>
                """
        return html


def get_html(user_id: int, category: str, all_cat: bool) -> str:
    """
    create an HTML page
    :param user_id: int: id of user (can be None)
    :param category: str: book category (can be None)
    :param all_cat: bool: if True get one book for all category else top 5 categories
    :return: str: html page
    """
    html = HTML
    # check if user_id is in database
    if user_id not in ratings['user_id'].unique() and user_id is not None:
        return str(user_id)

    if user_id:
        # get nearest_users
        nearest_users = get_n_nearest_users(user_id, 5)
        # get suggested books from nearest users
        nearest_users_suggested_books = get_top_n_books_nearest_users(nearest_users, 5)
        # get books names from list ok book_id
        books_name_nu = get_book_name(nearest_users_suggested_books)
        # convert to html
        html += NEAREST_USER_HTML + get_pictures(nearest_users_suggested_books) + get_html_names(books_name_nu)
        # get top author
        author = get_top_author(user_id)
        # get books from top author
        books_id_from_top_author = get_top_n_books_by_author(author, user_id, 5)
        # get books name from author
        books_from_top_author = get_book_name(books_id_from_top_author)
        # convert to html
        html += get_html_author(author) + get_pictures(books_id_from_top_author) + get_html_names(books_from_top_author)

        if category:
            # get suggested books from category
            list_of_books = get_top_n_books_by_category(category, 5, user_id)
            # get books names from list of book_id
            books_name_cat = get_book_name(list_of_books)
            # convert to html
            html += get_html_category([category]) + get_pictures(list_of_books) + get_html_names(books_name_cat)
            return html + END
        else:
            if all_cat:
                list_of_cat = categories
            else:
                # get top 5 categories
                list_of_cat = categories[:5]
            # initialize list
            list_of_books = []
            # get list of book ids (1 per category)
            for cat in list_of_cat:
                list_of_books.append(get_top_n_books_by_category(cat, 1, user_id)[0])
            # get book names from book list
            books_name_cat = (get_book_name(list_of_books))
            # convert to html
            remain = 0
            if len(list_of_cat) % 5 != 0:
                remain = 1
            for i in range(0, len(list_of_cat) // 5 + remain):
                start = i * 5
                end = start + 5
                html += get_html_category(list_of_cat[start:end], i) + get_pictures(
                    list_of_books[start:end]) + get_html_names(books_name_cat[start:end])
            return html + END
    else:
        # get the id of top books for whole users
        list_of_books = get_top_n_books(5)
        # get books names based on book ids
        books_name_all = get_book_name(list_of_books)
        # convert to html
        html += GENERAL_HTML + get_pictures(list_of_books) + get_html_names(books_name_all)
        if category:
            # get suggested books from category
            list_of_books = get_top_n_books_by_category(category, 5)
            # get books names from list of book_id
            books_name_cat = get_book_name(list_of_books)
            # convert to html
            html += get_html_category([category]) + get_pictures(list_of_books) + get_html_names(books_name_cat)
            return html + END
        else:
            print(all_cat)
            if all_cat:
                list_of_cat = categories
            else:
                # get top 5 categories
                list_of_cat = categories[:5]
            # initialize list
            list_of_books = []
            # get list of book ids (1 per category)
            for cat in list_of_cat:
                list_of_books.append(get_top_n_books_by_category(cat, 1)[0])
            # get list of book names
            books_name_cat = get_book_name(list_of_books)
            # convert to html
            remain = 0
            if len(list_of_cat) % 5 != 0:
                remain = 1
            for i in range(0, len(list_of_cat)//5 + remain):
                start = i * 5
                end = start + 5
                html += get_html_category(list_of_cat[start:end], i) + get_pictures(list_of_books[start:end]) + get_html_names(books_name_cat[start:end])
            return html + END
