from bs4 import BeautifulSoup

def extract_text(html):
    soup = BeautifulSoup(html, 'html.parser')
    # Using .get_text() method to extract all the text 
    text = soup.get_text()
    return text

html_data = """
<html>
    <head>
        <title>Test Page</title>
    </head>
    <body>
        <h1>Welcome to the Test Page</h1>
        <p>This is a test paragraph.</p>
    </body>
</html>
"""

print(extract_text(html_data))
