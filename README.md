# books_recommendation
by Imad, Nicolas & Hugo

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

- You have an user id : 
  - Enter user id 
  - You can choose (or not) a category
  - If you don't choose a specific category you can check the checkbox to display all categories (by default only top 5 categories will appear)
  - Click the submit button to have a suggestion of book
  <img src="https://github.com/hugaba/books_recommendation/blob/main/pics/principal.png">
  
- You don't have an user id :
  - leave the user id zone blank
  - You can choose (or not) a category
  - If you don't choose a specific category you can check the checkbox to display all categories (by default only top 5 categories will appear)
  - Click the submit button to have a suggestion of book
- After having some books recommended, you can go back on the first page by clicking the home button on the top left of the page

