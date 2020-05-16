from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from lxml import etree
import os
import webbrowser


def cleanup():
    try:
        os.remove("task1.xml")
        os.remove("task2.xml")
        os.remove("task2.xhtml")
    except OSError:
        pass


def scrap_data():
    process = CrawlerProcess(get_project_settings())
    process.crawl('korrespondent')
    process.crawl('hotline')
    process.start()


def task1():
    print("-" * 50 + "\n Task 1")
    root = etree.parse("task1.xml")
    pages = root.xpath("//page")
    print(" Number of text fragments for each document")
    for page in pages:
        url = page.xpath("@url")[0]
        count = page.xpath("count(fragment[@type='text'])")
        print(" %s: %d" % (url, count))


def task2():
    print("-" * 50 + "\n Task 2")
    transform = etree.XSLT(etree.parse("task2.xsl"))
    result = transform(etree.parse("task2.xml"))
    result.write("task2.xhtml", pretty_print=True, encoding="UTF-8")
    print(" Сreated XHTML page will be opened in the browser")
    webbrowser.open('file://' + os.path.realpath("task2.xhtml"))


if __name__ == '__main__':
    print(" Cleanuping files", end='', flush=True)
    cleanup()
    print(" Done!")
    print(" Scrapping data from sites...", end='', flush=True)
    scrap_data()
    print(" Finished!")
    while True:
        print("-" * 50 +"\n Enter task number (1 or 2) to complete, 0 to exit")
        print(" [1] - Task 1")
        print(" [2] - Task 2")
        print(" [0] - Exit")
        print(" Your input: ", end='', flush=True)
        number = input()
        if number == "1":
            task1()
        elif number == "2":
            task2()
        elif number == "0":
            break
        else:
           print(" Wrong input! Try again...")

