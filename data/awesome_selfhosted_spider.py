import scrapy

class AwesomeSelfHostedSpider(scrapy.Spider):
    name = "awesome_selfhosted"
    start_urls = ['https://awesome-selfhosted.net/platforms/docker.html']

    def parse(self, response):
        for section in response.css('section'):
            item = {
                'Name': section.css('h3::text').get().strip(),
                'Description': section.css('p::text').get().strip(),
                'Source Code': section.css('a[href*="github.com"]::attr(href)').get(),
                'License': section.css('span.license-box a.license-link::text').get(),
                'Tag': section.css('span.tag a::text').get()
            }
            yield item

# To run the spider and save the output as JSON, use the following command:
# scrapy runspider awesome_selfhosted_spider.py -o output.json