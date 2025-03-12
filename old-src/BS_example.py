from bs4 import BeautifulSoup

html = """
<html>
    <body>
        <div class="home">
            <h2 class="title">Beautiful Home</h2>
            <span class="price">$500,000</span>
        </div>
    </body>
</html>
"""

soup = BeautifulSoup(html, "html.parser")

# Find the title
title = soup.find("h2", class_="title").text
print(title)  # Output: Beautiful Home

# Find the price
price = soup.find("span", class_="price").text
print(price)  # Output: $500,000
