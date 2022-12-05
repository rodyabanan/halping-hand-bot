import requests
from bs4 import BeautifulSoup
from datetime import datetime

URL = "https://rasp.sgugit.ru/?ii=1&fi=1&c=3&gn=59&"

def get_lesson_data(date):

    convert_date = datetime.strftime(date, '%d.%m')
    
    response = requests.get(URL)

    soup = BeautifulSoup(response.text, 'lxml')

    days = soup.find_all('div', class_='one-day')

    lesson_dict = {}

    for day in days:
        date_value = day.select_one('.everD').text.strip()

        day_lessons = day.find_all('div', class_='one_lesson')

        lesson_info_list = []

        for day_lesson in day_lessons:
            start_time = day_lesson.find(class_='starting_less').text
            finish_time = day_lesson.find(class_='finished_less').text

            lesson_info = day_lesson.find(class_="clearfix")

            lesson_string = f"{start_time}-{finish_time} "
            
            for child in lesson_info.children:
                if len(child.text) > 1:
                    lesson_string += child.text.strip() + " "

            if len(lesson_string) > 12:
                lesson_info_list.append("\N{Clipboard}" + lesson_string)

                lesson_dict[date_value] = lesson_info_list
        
    a = '\n\n'.join(lesson_dict[convert_date])
    return a

if __name__ == "__main__":
    get_lesson_data()

