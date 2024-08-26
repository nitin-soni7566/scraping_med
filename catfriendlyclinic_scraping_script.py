import re
from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

URL = "https://catfriendlyclinic.org/cat-owners/find-a-clinic/"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Accept-Language": "en-US,en;q=0.5",
}


def get_page_numbers(url, headers, class_name, element_name):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()  # Check for HTTP request errors
        soup = BeautifulSoup(r.content, "html.parser")
        result = soup.find_all(element_name, class_=class_name)
        result.pop()
        pages = max(int(i.text) for i in result)
        return pages
    except requests.RequestException as e:
        logging.error(f"Error fetching page numbers: {e}")
        return 0
    except ValueError as e:
        logging.error(f"Error parsing page numbers: {e}")
        return 0


def fetch_clinic_data(page_no):
    try:
        r = requests.get(f"{URL}page/{page_no}/", headers=HEADERS)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        result = soup.find_all("div", class_="clinic")
        logging.info(f"Page {page_no} data Fetching ...")
        return result
    except requests.RequestException as e:
        logging.error(f"Error fetching data from page {page_no}: {e}")
        return []


def parse_clinic_info(result):
    data = []
    for i in result:
        clinic_name = i.h2.text if i.h2 else ""
        address = re.sub(r"[\n\t]", "", i.section.text if i.section else "")
        tel = i.footer.span.text if i.footer and i.footer.span else ""
        link = i.footer.a.get("href") if i.footer and i.footer.a else ""
        data.append(
            {
                "Clinic name": clinic_name.strip(),
                "Full address": address.strip(),
                "Email": "",
                "Contact No": tel.strip(),
                "Web site": link.strip(),
            }
        )
    return data


def save_to_excel(data):
    try:
        df = pd.DataFrame(data)
        df.to_excel("catfriendlyclinic.xlsx", index=False)
        logging.info("Data successfully saved to catfriendlyclinic.xlsx")
    except Exception as e:
        logging.error(f"Error saving data to Excel: {e}")


def main():
    pages = get_page_numbers(URL, HEADERS, "page-numbers", "a")
    if pages == 0:
        logging.error("No pages to fetch.")
        return
    logging.info(f"Total pages: {pages}")

    all_data = []
    for page_no in range(1, pages + 1):
        result = fetch_clinic_data(page_no)
        if result:
            data = parse_clinic_info(result)
            all_data.extend(data)

    if all_data:
        save_to_excel(all_data)


if __name__ == "__main__":
    main()
