import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging


# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def decode_email(encoded_email):
    r = int(encoded_email[:2], 16)
    email = "".join(
        [
            chr(int(encoded_email[i : i + 2], 16) ^ r)
            for i in range(2, len(encoded_email), 2)
        ]
    )
    return email


def remove_special_char(value):

    value = re.sub("\t", "", value)
    value = re.sub("\n", "", value)
    value = re.sub("\r", "", value)
    return value


URL = "https://findavet.rcvs.org.uk/find-a-vet-practice/?filter-choice=&filter-keyword=&filter-searchtype=practice&filter-pss=true&p=1"

HEADERS = {
    "User_Agent": "Mozilla/5.0 (windows NT 10; Win64; rv:94.0; Gecko/20100101 Firefox/94.0",
    "Accept-Language": "en-US, en;q=0.5",
}

data = []


def get_page_numbers(url, headers, class_name, element_name):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        result = soup.find(element_name, class_=class_name).find_all("li", class_="num")
        l = []
        for i in result:
            l.append(int(i.text))
        return max(l)
    except Exception as e:

        logging.error(f"Error while fetching page numbers : {e}")
        return 0


def fetch_data(page_no):
    try:
        res = requests.get(
            f"https://findavet.rcvs.org.uk/find-a-vet-practice/?filter-choice=&filter-keyword=&filter-searchtype=practice&filter-pss=true&p={page_no}",
            headers=HEADERS,
        )
        res.raise_for_status()

        soup = BeautifulSoup(res.content, "html.parser")
        result = soup.find_all("div", class_="practice")
        logging.info(f"Page no {page_no} data fetching ...")
        return result
    except Exception as e:
        logging.error(f"Error while featching data from page {page_no} ")
        return []


def parsing_data(result):
    try:
        for i in result:

            name = remove_special_char(str(i.h2.text))
            address = remove_special_char(str(i.div.text) + f" {i.div.span.text}")
            address = remove_special_char(str(address))
            address = remove_special_char(str(address))
            content = i.find("div", class_="item-contact")
            if content.find("span", class_="item-contact-tel") is None:

                phone_no = ""
            else:

                phone_no = str(
                    content.find("span", class_="item-contact-tel").text
                ).replace("phone2", "")
                phone_no = remove_special_char(phone_no)

            content = i.find("div", class_="item-contact")
            if content.find("a", class_="item-contact-email") is None:
                email = ""
            else:
                if content.find("span", class_="__cf_email__") is None:
                    email = ""
                else:
                    email = decode_email(
                        content.find("span", class_="__cf_email__")["data-cfemail"]
                    )

            data.append(
                {
                    "Name": name,
                    "Full address": address,
                    "Phone no": phone_no,
                    "Email": email,
                    "Web site": "",
                }
            )
        return data
    except Exception as e:
        logging.error("Error while parsing data.")
        return []


# pages = get_page_numbers(URL, header, "paging", "ol")


def save_to_excel(data):
    try:
        df = pd.DataFrame(data)
        df.to_excel("findavet.xlsx", index=False)
        logging.info("Data successfully saved to findavet.xlsx")
    except Exception as e:
        logging.error(f"Error saving data to Excel: {e}")


def main():
    pages = get_page_numbers(URL, HEADERS, "paging", "ol")
    if pages == 0:
        logging.error("No pages to fetch.")
        return
    logging.info(f"Total pages: {pages}")

    all_data = []
    for page_no in range(1, pages + 1):
        result = fetch_data(page_no)
        if result:
            data = parsing_data(result)
            all_data.extend(data)

    if all_data:
        save_to_excel(all_data)


if __name__ == "__main__":
    main()
