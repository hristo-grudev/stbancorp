import scrapy

from scrapy.loader import ItemLoader

from ..items import StbancorpItem
from itemloaders.processors import TakeFirst


class StbancorpSpider(scrapy.Spider):
	name = 'stbancorp'
	start_urls = ['https://www.stbancorp.com/press-releases']

	def parse(self, response):
		post_links = response.xpath('//span[@class="html-link"]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//a[@rel="next"]/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//div[@class="field__item"]/text()').get()
		description = response.xpath('//div[@class="xn-content"]//text()[normalize-space()]|//article/div[@class="node__content"]//text()[normalize-space() and not(ancestor::div[class="field__item"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="dateformat"]/text()').get()

		item = ItemLoader(item=StbancorpItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
