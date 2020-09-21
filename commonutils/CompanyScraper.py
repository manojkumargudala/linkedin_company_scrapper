import time
from .Scraper import Scraper
import commonutils.utils as utils


class CompanyScraper(Scraper):

    def scrape(self, company):
        self.load_initial(company)
        overview = {}
        overview.update({utils.webSite: self.get_text("//dt[text()='Website']/following-sibling::*[1]")})
        overview.update({utils.industry: self.get_text("//dt[text()='Industry']/following-sibling::*[1]")})
        overview.update({utils.company_size: self.get_text("//dt[text()='Company size']/following-sibling::*[1]")})
        overview.update(
            {utils.people_on_linkedin: self.get_text("//dt[text()='Company size']/following-sibling::*[2]")})
        overview.update({utils.headquarters: self.get_text("//dt[text()='Headquarters']/following-sibling::*[1]")})
        overview.update({utils.type: self.get_text("//dt[text()='Type']/following-sibling::*[1]")})
        overview.update({utils.type: self.get_text("//dt[text()='Founded']/following-sibling::*[1]")})
        overview.update({utils.specialties: self.get_text("//dt[text()='Specialties']/following-sibling::*[1]")})
        return overview

    def load_initial(self, url):
        self.driver.get(url)
        time.sleep(5)
        self.wait_for_el_xpath("//li//a[text()='About']")
        self.driver.find_element_by_xpath("//li//a[text()='About']").click()
        time.sleep(5)

    def get_text(self, xpathString):
        try:
            self.wait_for_el_xpath(xpathString)
            # print(self.driver.find_element_by_xpath(xpathString).get_attribute("innerText"))
            return self.driver.find_element_by_xpath(xpathString).get_attribute("innerText")
        except:
            return ''
