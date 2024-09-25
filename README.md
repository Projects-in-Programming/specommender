# Specommender

This is a Python program that detects face shape from a photograph and recommends glasses based on the shape of the face of the user. The program leverages a face shape detection model from roboflow utilizing its api and scrapes [https://www.eyebuydirect.com/eyeglasses/](https://www.eyebuydirect.com/eyeglasses/) to get the eye glasses for a particular face type.It uses the Selenium WebDriver to navigate the website and BeautifulSoup to parse the HTML. The script extracts details like name, price, available colors and link to the eyeglass which is extracted in a Pandas DataFrame and saved as a CSV file.

### Why specommender ?

I love creating solutions that solve real world problems and this was one of the project that I had wanted to do for so long. This program solves a real world problem and includes effecient data cleaning which suffices the requirements for this assignment.

The data cleansing procedure is done in the file `functions.py` inside the function `clean_data` and can be viewed here.

### Design Choice

* I decided to use selenium here because the website contains JS loader and using just Beautiful soup would not capture the loaded data.

* The code also follows modular design and has different functions and scripts to perfom tasks. 

* The program ask user for number of pages they want to look into and then scrape that many pages.

* Also, the program eventualy filters glasses based on the price requested by the user. 

As a whole, this program provides a justified utility to the user. 

## Code Organization
`functions.py` - contains crutial functions required for the program to run like functions to get face shape and function to clean data
`scrapper.py` - contains function to scrape the data 

## Requirements

* Python 3.x
* Selenium
* BeautifulSoup
* Pandas
* Chrome WebDriver (or another WebDriver of your choice)
* inference-sdk (Roboflow api to get inference from the data)
* astutils (handling a dataframe column containing list)

## Installation

1. Install the required Python packages using pip:

```bash
pip install -r requirements.txt
```

## Usage

1. Clone the repository to your local machine.
2. Open the script in a text editor and modify the `RATE_LIMIT` variable to set the desired rate limit for requests to the website (in seconds).
3. Run the script using Python:

```bash
python main.py
```

4. The script will create a CSV file called `your_face_shape_glasses.csv` in the same directory containing the event data.

## Notes
* This program takes in user input which is an snapshot of the face and gives out glass recommendations. 
* 
* The script uses a rate limit to avoid overloading the website with requests. The default rate limit is 2 second, but you can modify this value as needed.
* The script uses error handling to catch `TimeoutException` errors that may occur when accessing the website. If a `TimeoutException` error occurs, the script will print an error message and continue to the next iteration of the loop.
* The script assumes that the HTML structure of the NYU Events website will not change. If the website's HTML structure changes, the script may need to be modified to continue working correctly.



## Future Work

* Provide a cleaner interface