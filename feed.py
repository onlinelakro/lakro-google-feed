import pandas as pd
import requests
from xml.sax.saxutils import escape

FEED_URL = "https://www.lakro.nl/product-feed-jw/j2jIqFr-XQ"

csv_data = requests.get(FEED_URL).content.decode('utf-8')

from io import StringIO

df = pd.read_csv(StringIO(csv_data))

# prijzen goed formatteren
if 'price' in df.columns:
    df['price'] = df['price'].fillna(0).astype(float).map(lambda x: f"{x:.2f} EUR")

if 'sale_price' in df.columns:
    df['sale_price'] = df['sale_price'].fillna(0).astype(float)
    df['sale_price'] = df['sale_price'].map(lambda x: f"{x:.2f} EUR" if x > 0 else "")

xml = []
xml.append('<?xml version="1.0" encoding="UTF-8"?>')
xml.append('<rss version="2.0" xmlns:g="http://base.google.com/ns/1.0">')
xml.append('<channel>')
xml.append('<title>Lakro Feed</title>')
xml.append('<link>https://www.lakro.nl</link>')
xml.append('<description>Google Shopping Feed</description>')

for _, row in df.iterrows():
    xml.append('<item>')

    xml.append(f"<g:id>{escape(str(row.get('id', '')))}</g:id>")
    xml.append(f"<title>{escape(str(row.get('title', '')))}</title>")
    xml.append(f"<link>{escape(str(row.get('link', '')))}</link>")
    xml.append(f"<description>{escape(str(row.get('description', '')))}</description>")

    availability = row.get('availability', 'in stock')
    xml.append(f"<g:availability>{escape(str(availability))}</g:availability>")

    xml.append(f"<g:price>{escape(str(row.get('price', '0.00 EUR')))}</g:price>")

    if row.get('sale_price', ''):
        xml.append(f"<g:sale_price>{escape(str(row.get('sale_price')))}</g:sale_price>")

    image = row.get('image_link', '')
    if image:
        xml.append(f"<g:image_link>{escape(str(image))}</g:image_link>")

    brand = row.get('brand', '')
    if brand:
        xml.append(f"<g:brand>{escape(str(brand))}</g:brand>")

    xml.append('<g:condition>new</g:condition>')
    xml.append('</item>')

xml.append('</channel>')
xml.append('</rss>')

with open('feed.xml', 'w', encoding='utf-8') as f:
    f.write('\n'.join(xml))

print('feed.xml gemaakt')
