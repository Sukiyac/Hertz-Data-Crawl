from urllib.request import urlopen
from bs4 import BeautifulSoup as soup
from xlwt import Workbook
import datetime


class Hertz:
    def __init__(self):
        self.resTable = [
            ["car vin", "car maker", "model", "year", "fuel economy", "driveLine", "mileage", "no haggle price",
             "address"]]

    def getHTML(self, url):
        uClient = urlopen(url)
        html_content = uClient.read()
        uClient.close()
        soup(html_content, "html.parser")

    # https://www.hertzcarsales.com/used-cars-for-sale.htm?start=0&geoRadius=1000&geoZip=48187
    def parseURL(self, pageCount, itemPerPage):
        return "https://www.hertzcarsales.com/used-cars-for-sale.htm?start={startIdx}&geoRadius=2485&geoZip=48187".format(startIdx = pageCount*itemPerPage)

    def getCarInfo(self, url):
        uClient = urlopen(url)
        html_content = uClient.read()
        uClient.close()
        html_object = soup(html_content, "html.parser")
        containers = html_object.find_all("li", {"class": "item hproduct clearfix closed certified primary"})
        # data-make, data-model, data-bodystyle, data-drivetrain, data-city, data-zipcode, data-state, data-address
        for container in containers:
            car_vin = container["data-vin"]
            year = container["data-year"]
            maker = container["data-make"]
            model = container["data-model"]
            zip = container["data-zipcode"]
            city = container["data-city"]
            state = container["data-state"]
            address = container["data-address"]

            detailed_address = ", ".join([address, city, state, zip])

            simple_info = container.find("div", {"class": "gv-description"})
            odometer = simple_info.find("span", {"data-name": "odometer"}).get_text()
            # odo = odometer.get_text()
            if simple_info.find("span", {"data-name": "cityFuelEconomy"}):
                fuel_economy = simple_info.find("span", {"data-name": "cityFuelEconomy"}).get_text()
            else:
                fuel_economy = 'N/A'
            if simple_info.find("span", {"data-name": "driveLine"}):
                drive_line = simple_info.find("span", {"data-name": "driveLine"}).get_text()
            else:
                drive_line = 'N/A'

            # get price
            car_price = container.find("div", {"class": "detailed-pricing"}).find("span", {"class": "value"}).get_text()

            car_info_row = [car_vin, maker, model, year, fuel_economy, drive_line, odometer, car_price, detailed_address]
            self.resTable.append(car_info_row)

    def writeCarInfoToCSV(self):
        file_name = "Hertz Car for Sell "+datetime.datetime.now().strftime('%Y_%m_%d')+".xls"
        wb = Workbook()
        sheet1 = wb.add_sheet('Hertz car for sell')
        row, col = len(self.resTable), len(self.resTable[0])

        for r in range(row):
            for c in range(col):
                sheet1.write(r, c, self.resTable[r][c])

        wb.save(file_name)