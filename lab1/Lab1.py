import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import os, time

def upload_reviews(starting_url, page_count):
    if not os.path.exists("dataset"):
        os.makedirs("dataset")       
    for page in range(1, page_count + 1):
        ua = UserAgent()
        user_agent = ua.random
        print("User-Agent: ", user_agent)
        page_url = f"{starting_url}{page}"
        time.sleep(60)
        response = requests.get(page_url, headers = {"User-Agent": user_agent})
        print(response.status_code)
        if response.status_code == 200:
            print("Отзыв получен")
            soup = BeautifulSoup(response.content, 'html.parser')
            titles = soup.find_all('a', class_='review-title')
            ratings = soup.find_all('div', class_='product-rating tooltip-right')
            for title, rating in zip(titles, ratings):
                rating_text = rating['title']
                number_stars = rating_text[-1]
                review_text = title.text
                rating_folder = os.path.join("dataset", number_stars)
                if not os.path.exists(rating_folder):
                    os.makedirs(rating_folder)
                file_folder = os.listdir(rating_folder)
                file_number = len(file_folder) + 1
                file_name = f"{file_number:04d}.txt"
                with open(os.path.join(rating_folder, file_name), "w", encoding="utf-8") as file:
                    file.write(review_text)
        else:
            print("Отзыв не получен")

if __name__ == "__main__":
    starting_url = "https://otzovik.com/reviews/set_magazinov_pyaterochka_russia/"
    page_count = 250
    upload_reviews(starting_url, page_count)