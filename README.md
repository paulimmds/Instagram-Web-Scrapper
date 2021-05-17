# Instagram-Web-Scrapper
Instagram Crawler/Scrapper with Python + Selenium WebDriver.

Extract some data about users on Instagram.
  - profile Url
  - profile Name
  - Full Name
  - Followers numbers
  - Following numbers
  - Publication numbers
  - Bio
  - Website

## Requiriments
Instagram Bot was developed using Python 3.

Before you can run the bot, you will need to install a few Python dependencies.
- Selenium     `pip install Selenium`
- ChromeDriver `https://sites.google.com/a/chromium.org/chromedriver/downloads`

## Run
Make sure you are in the correct folder and run the following command: `python main.py`

The execution terminal will guide you through your steps.
On your first run, you will have to log in to an account.
After that, the program will store your cookies for later executions, so you will not have to log in again. 

After that, you will have to choose between 4 options:
  - Hashtags Posts:
    This function will collect the data from a target hashtag, and return you a csv file with the data of users who have posted some content marking that hashtag.

    You must enter:
      - The names of the hashtags you want to scrape. 
        * Enter names separated by commas and without spacing.
           * *Example: hashtag1, hashtag2, hashtag3*
      - Limit of posts you want to scrape in each hashtag

  - Commented Posts:
    This function will collect the data of a target user, and return you a csv file with the data of the users who commented on the posts of the target user.

    You must enter: 
      - Users of the users you want to scrape.
        * Enter users separated by commas and without spacing.
          * *Example: user1, user2, user3*
      - The limit of posts you want to scrape on each profile
      - The limit of users that you want to scratch for each post, in each profile.
  
  - Tagged Posts:
    This function will collect the data of a target user, and return you a csv file with the data of the users who marked the target user in their publications.

    You must enter:
      - Users of the users you want to scrape.
        * *Example: user1, user2, user3*
      - The limit of posts / users that you want to scrape on each profile.
 - Finalize Execution:
        This function will end the execution of the program.

## More

This code only works on the Brazilian version of Instagram. If you want to run it for another version of the website, you will have to change the elements of the webdriver.
For example:

`not_now = WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(), "Agora não")]'))).click()`

The following line will not work on the English version of Instagram, because the text of the element being searched for, should be "Not Now" for the English version.


**I will adapt the code for the English version of the website and will soon bring updates.**

**Feel free to contact me and ask questions.**

**Feel free to contribute.**
