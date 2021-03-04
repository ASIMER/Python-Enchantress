link = "http://socrates.vsau.org/wiki/index.php/%D0%A1%D0%BF%D0%B8%D1%81" \
       "%D0%BE%D0%BA_%D0%B0%D0%B4%D1%80%D0%B5%D1%81_%D0%B5%D0%BB%D0%B5" \
       "%D0%BA%D1%82%D1%80%D0%BE%D0%BD%D0%BD%D0%B8%D1%85_%D0%BF%D0%BE%D1" \
       "%88%D1%82%D0%BE%D0%B2%D0%B8%D1%85_%D1%81%D0%BA%D1%80%D0%B8%D0%BD" \
       "%D1%8C_%D1%81%D1%82%D1%80%D1%83%D0%BA%D1%82%D1%83%D1%80%D0%BD%D0" \
       "%B8%D1%85_%D0%BF%D1%96%D0%B4%D1%80%D0%BE%D0%B7%D0%B4%D1%96%D0%BB" \
       "%D1%96%D0%B2_%D1%83%D0%BD%D1%96%D0%B2%D0%B5%D1%80%D1%81%D0%B8%D1" \
       "%82%D0%B5%D1%82%D1%83"


def load_site(address: str) -> bytes:
    from requests import request

    response = request(method="GET", url=address)

    return response.content


def parse(text: bytes, grab_headers=False):
    """

    :param text: site content
    :param grab_headers: site content
    :return:
    """
    from bs4 import BeautifulSoup
    from re import findall

    soup = BeautifulSoup(text, 'html.parser')
    counter = 0
    header = ''
    emails = []
    result = {} if grab_headers else []
    for child in soup.find(id='mw-content-text'):
        if child == '\n':
            continue
        elif child.name == 'h2':
            header = findall('[^\d. ][\w\- ]*', child.text)[0]
        elif child.name == 'p':
            email = findall('([ \w]*).([\w\-]*@[\w\-.]*)', child.text)
            if email:
                email = email[0]
            else:
                continue
            if grab_headers:
                if header in result:
                    result[header].append((email[0], email[1]))
                else:
                    result[header] = [(email[0], email[1])]
            else:
                result.append((email[0], email[1]))

    return result

if __name__ == '__main__':

    site = load_site(link)
    print(parse(site, grab_headers=True))
