# books_recommendation
by Imad, Nicolas & Hugo
<br/>link to colab used to make recommandation system : [colab](https://colab.research.google.com/drive/1RgHvqMhhhpD9kAAPoGrU5kRfyjHpVKMa?usp=sharing)

# content
- data folder: contains data.sh file to load the csv
- pics: contains pics for README.md
- templates: contains html template for main page
- api.py: main file for the api
- functions.py: functions used to make the recommandation book
- requirements.txt: requirements to make the virtual environments
- database.ipynb : ipynb file to create the sql database

<img src="https://github.com/hugaba/books_recommendation/blob/main/pics/sql_database.png">


# Getting Started
## prerequisite:
### Create your virtual environment
Open the folder in which you import the github files

Open a terminal and create a new virtual environment : python3 -m venv env

Install the required libraries: pip3 install -r requirements.txt

### Download files
Open the data folder

Open a terminal in the folder and make the file data.sh executable by : chmod 744 data.sh

Execute data.sh with the command line: sh -x ./data.sh

(If executing the .sh file doesn't work, you can directly download the books_withcat.csv, ratings.csv and csr_matrix.npz files and add them to the data folder: [data folder](https://drive.google.com/drive/folders/1xJYsbrK_x0ATZ6xh6uBakyPnpW-N1MDY?usp=sharing "Drive link"))

## Start program
open a terminal in the main folder

activate your virtual environment with the command line: source venv/bin/activate

start the api with the command line: uvicorn api:app --reload

go on this url: http://127.0.0.1:8000/recommandation

<img src="https://github.com/hugaba/books_recommendation/blob/main/pics/principal.png">

- You have an user id : 
  - Enter user id 
  - You can choose (or not) a category
  - If you don't choose a specific category you can check the checkbox to display all categories (by default only top 5 categories will appear)
  - Click the submit button to have a suggestion of book:
    - top 5 books from nearest users
    - top 5 books from favourite author
    - top 5 books from choosen category (if no category selected top one book from top 5 category)
  
<img src="https://github.com/hugaba/books_recommendation/blob/main/pics/id_nearest_users.png">
<img src="https://github.com/hugaba/books_recommendation/blob/main/pics/id_fav_author.png">
<img src="https://github.com/hugaba/books_recommendation/blob/main/pics/id_top5_cats.png">
  
  
- You don't have an user id :
  - leave the user id zone blank
  - You can choose (or not) a category
  - If you don't choose a specific category you can check the checkbox to display all categories (by default only top 5 categories will appear)
  - Click the submit button to have a suggestion of book:
    - top 5 books from goodreads database
    - top 5 books from choosen category (if no category selected top one book from top 5 category)

<img src="https://github.com/hugaba/books_recommendation/blob/main/pics/general_top5cats.png">

- After having some books recommended, you can go back on the first page by clicking the home button on the top left of the page

