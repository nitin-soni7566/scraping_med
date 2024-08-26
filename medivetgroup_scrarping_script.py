from bs4 import BeautifulSoup
import requests
import pandas as pd
import logging

URL = "https://www.medivetgroup.com/vet-practices/?address=Λονδίνο,+Ηνωμένο+Βασίλειο&longitude=-0.1275862&latitude=51.5072178&isEmergency=False&"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:94.0) Gecko/20100101 Firefox/94.0",
    "Accept-Language": "en-US,en;q=0.5",
}

# Setup logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def get_page_numbers(url, headers, class_name, element_name):
    try:
        r = requests.get(url, headers=headers)
        r.raise_for_status()
        soup = BeautifulSoup(r.content, "html.parser")
        result = soup.find_all(element_name, class_=class_name)

        l = []
        for i in range(1, len(result) - 1):
            l.append(int(result[i].text))
        pages = max(l) if l else 0
        return pages
    except requests.RequestException as e:
        logging.error(f"Error fetching page numbers: {e}")
        return 0
    except ValueError as e:
        logging.error(f"Error parsing page numbers: {e}")
        return 0


def fetch_data(page_no):
    try:
        res = requests.get(f"{URL}page={page_no}", headers=HEADERS)
        res.raise_for_status()
        soup = BeautifulSoup(res.content, "html.parser")
        result = soup.find_all("div", class_="innerWrap")
        logging.info(f"Page {page_no} data fetching ...")
        return result
    except requests.RequestException as e:
        logging.error(f"Error while fetching data from page {page_no}: {e}")
        return []


def parse_data(result):
    data = []
    try:
        for i in result:
            name = i.h3.text.strip() if i.h3 else ""
            address = " ".join(
                addr.text.strip() for addr in i.find_all("span", class_="nowrap")
            )

            phone_no_elem = i.find("div", class_="innerWrap--content")
            phone_no = (
                phone_no_elem.find_all("p")[1].text.strip()
                if phone_no_elem and len(phone_no_elem.find_all("p")) > 1
                else ""
            )

            link_elem = i.find("a", class_="button cta reverse")
            link = link_elem.get("href").strip() if link_elem else ""

            data.append(
                {
                    "Name": name,
                    "Full Address": address,
                    "Phone no": phone_no,
                    "Web site": link,
                    "Email": "",
                }
            )
        return data
    except Exception as e:
        logging.error(f"Error parsing data: {e}")
        return []


def save_to_excel(data):
    try:
        df = pd.DataFrame(data)
        df.to_excel("medivetgroup.xlsx", index=False)
        logging.info("Data successfully saved to medivetgroup.xlsx")
    except Exception as e:
        logging.error(f"Error saving data to Excel: {e}")


def main():
    pages = get_page_numbers(f"{URL}page=1", HEADERS, "ajaxLink", "a")
    if pages == 0:
        logging.error("No pages to fetch.")
        return

    logging.info(f"Total pages: {pages}")
    all_data = []
    for page_no in range(1, pages + 1):
        result = fetch_data(page_no)
        if result:
            data = parse_data(result)
            all_data.extend(data)

    if all_data:
        save_to_excel(all_data)


if __name__ == "__main__":
    main()
