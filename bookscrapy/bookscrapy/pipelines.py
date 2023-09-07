# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import mysql.connector
from itemadapter import ItemAdapter


class BookscrapyPipeline:
    def process_item(self, item, spider):
        return item


class BookscrapyPipeline:
    def process_item(self, item, spider):
        adapter = ItemAdapter(item)

        # * strip all whitespace from the data
        field_names = adapter.field_names()
        for field_name in field_names:
            if field_name != "description":
                value = adapter.get(field_name)
                adapter[field_name] = value[0].strip()

        # * category and product_type convert => to lower case
        lower_case_keys = ["categroy", "product_type"]
        for lower_case in lower_case_keys:
            value = adapter.get(lower_case)
            adapter[lower_case] = value.lower()

        # * convert the price and price_and_tax to float
        price_keys = ["price", "price_and_tax"]
        for price_key in price_keys:
            value = adapter.get(price_key)
            value = value.replace("£", "")
            adapter[price_key] = float(value)

        # * availability convert to int
        availability = adapter.get("availability")
        availability = availability.replace("In stock (", "")
        availability = availability.replace(" available)", "")
        adapter["availability"] = int(availability)

        # * rating_star convert to int
        stars_rating = adapter.get("rating_star")
        split_stars_array = stars_rating.split(" ")
        start_text_value = split_stars_array[1].lower()
        if start_text_value == "one":
            adapter["rating_star"] = 1
        elif start_text_value == "two":
            adapter["rating_star"] = 2
        elif start_text_value == "three":
            adapter["rating_star"] = 3
        elif start_text_value == "four":
            adapter["rating_star"] = 4
        elif start_text_value == "five":
            adapter["rating_star"] = 5

        return item



# ? save data to mysql
# class saveToMySQLPipline:

#     def __init__(self) -> None:
#         self.conn = mysql.connector.connect(
#             host="localhost",
#             user="root",
#             password='',  # * your password
#             database="bookscrapy"
#         )

#         # create a cursor for the database
#         self.curr = self.conn.cursor()

#         # create a table for the database
#         self.curr.execute("""
#             CREATE TABLE IF NOT EXISTS books(
#                 id INT AUTO_INCREMENT PRIMARY KEY,
#                 title TEXT,
#                 price FLOAT,
#                 price_and_tax FLOAT,
#                 availability INT,
#                 rating_star INT,
#                 description TEXT,
#                 categroy TEXT,
#                 product_type TEXT,
#                 url TEXT
#             )
#                 """)

#     def process_item(self, item, spider):

#         # * store the data in the database
#         self.curr.execute("""
#             INSERT INTO books (title, price, price_and_tax, availability, rating_star, description, categroy, product_type, url)
#             VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
#         """, (
#             item["title"],
#             item["price"],
#             item["price_and_tax"],
#             item["availability"],
#             item["rating_star"],
#             item["description"],
#             item["categroy"],
#             item["product_type"],
#             item["url"]
#         ))

#         # * commit the data to the database
#         self.conn.commit()
#         return item
    
#     # clase spider and database
#     def close_spider(self, spider):
#         self.conn.close()
#         self.curr.close()
