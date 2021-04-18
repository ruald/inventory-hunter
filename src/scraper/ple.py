import os


from scraper.common import ScrapeResult, Scraper, ScraperFactory


class PLEScrapeResult(ScrapeResult):
    def parse(self):
        alert_subject = 'In Stock'
        alert_content = ''

        # get name of product
        tag = self.soup.body.find('div', class_='itemName')
        if tag:
            alert_content += tag.text.strip() + '\n'
        else:
            self.logger.warning(f'missing title: {self.url}')

        # get listed price
        tag = self.soup.body.select_one('div.itemPrice')
        price_str = self.set_price(tag)
        if price_str:
            alert_subject = f'In Stock for {price_str}'
        else:
            self.logger.warning(f'missing price: {self.url}')

        # check for add to cart button
        tag = self.soup.body.find('div', class_='viewItemAvailabilityStatusWrapper')
        if tag and 'In Stock' in tag.text.lower():
            self.alert_subject = alert_subject
            self.alert_content = f'{alert_content.strip()}\n{self.url}'


@ScraperFactory.register
class BestBuyScraper(Scraper):
    @staticmethod
    def get_domain():
        return 'ple'

    @staticmethod
    def get_driver_type():
        return 'lean_and_mean'

    @staticmethod
    def get_result_type():
        return PLEScrapeResult
