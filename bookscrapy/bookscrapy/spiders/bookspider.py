import scrapy


class BookspiderSpider(scrapy.Spider):
    name = "bookspider"
    allowed_domains = ["books.toscrape.com"]
    start_urls = ["https://books.toscrape.com"]

    def parse(self, response):
        books =  response.css("article.product_pod") #* list of books
        
        for book in books:
            yield {
                'title': book.css("h3 a::text").get(), #* title
                'price': book.css(".product_price .price_color::text").get(), #* price
                'link': book.css("h3 a").attrib['href'] #* link
            }

        # scrapy for all page
        next_page = response.css("li.next a::attr('href')").get() #* next page
        if next_page is not None:
            if "catalogue/" in next_page:
                next_page_url = 'https://books.toscrape.com/' + next_page
            else:
                next_page_url = 'https://books.toscrape.com/catalogue/' + next_page
            yield response.follow(next_page_url, callback = self.parse)