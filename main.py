from HertzCar import Hertz


def main():
    # urlEnter = 'https://www.hertzcarsales.com/used-cars-for-sale.htm'
    # https://www.hertzcarsales.com/used-cars-for-sale.htm?start=35&geoRadius=1000&geoZip=48187
    # urlEnter = 'https://www.hertzcarsales.com/used-cars-for-sale.htm?geoZip=48187&geoRadius=1000'
    carInfo = Hertz()
    # carInfo.getCarInfo(urlEnter)

    pageCount = 1923
    for page in range(pageCount):
        curURL = carInfo.parseURL(page, 35)
        carInfo.getCarInfo(curURL)

    carInfo.writeCarInfoToCSV()


if __name__ == '__main__':
    main()
