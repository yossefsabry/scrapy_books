import scrapy
from bookscrapy.items import BookItem #item for choice the data to scrapy

class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    #* start url for user
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books = response.css("article.product_pod")  #* all of books

        #* loop for every book in bookpage
        for book in books:
            #* scrapy for all page
            relative_url = book.css(
                "h3 a::attr(href)").get()  # * book 

            if "catalogue/" in relative_url:
                book_url = 'https://books.toscrape.com/' + relative_url
            else:
                book_url = 'https://books.toscrape.com/catalogue/' + relative_url
            yield response.follow(book_url, callback=self.parse_book_page)


        """
        #* check for the next page 
        next_page = response.css("li.next a::attr(href)").get() #* next url page
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback=self.parse)
"""
    #* loop for the page for book and collect data for use
    def parse_book_page(self, response):
        table_rows = response.css("table tr")
        book_item = BookItem()


        book_item['url'] = response.url,
        book_item["title"] =  response.css(".product_main h1::text").get(),
        book_item["product_type"] = table_rows[1].css("td ::text").get(),
        book_item["price"] = table_rows[2].css("td::text").get(),
        book_item["price_and_tax"] = table_rows[3].css("td::text").get(),
        book_item["availability"] = table_rows[5].css("td::text").get(),
        book_item["rating_star"] = response.css(".star-rating").attrib['class'],
        book_item["description"] = response.xpath("//div[@class='sub-header']/preceding-sibling::p/text()").get(),
        book_item["categroy"] = response.xpath("//ul[@class='breadcrumb']/li[3]/a/@href").get(),
    
        yield book_item