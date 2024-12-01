from bs4 import BeautifulSoup


MAX_LENGTH = 255


def extract_page_data(txt_response, status_code):
    soup = BeautifulSoup(txt_response, "html.parser")
    h1_tag = soup.find("h1")
    title_tag = soup.find("title")
    description_tag = soup.find("meta", attrs={"name": "description"})

    return {
        "h1": h1_tag.text[:MAX_LENGTH] if h1_tag else "",
        "title": title_tag.text[:MAX_LENGTH] if title_tag else "",
        "status_code": status_code,
        "description": (
            description_tag.get("content", "")[
                :MAX_LENGTH] if description_tag else ""
        ),
    }
