"""
Name: Kaleab Alemu and Manogya Aryal
DSC 200
Lab 7: Web Scraping
Description:

Due Date: Nov 8, 2023
"""

# import necessary modules
import csv
import requests as req
from bs4 import BeautifulSoup


class Lab6:
    def task3a(self):
        # url to scrape from
        url = "https://vincentarelbundock.github.io/Rdatasets/datasets.html"

        # HTTP get request to the url
        page = req.get(url)

        # Parse the HTML content using BeautifulSoup
        parsed_Info = BeautifulSoup(page.content, 'html.parser')

        # get header
        header = []
        firstLine = parsed_Info.find_all('th')

        # get the header information
        for headers in firstLine:
            header.append(headers.text.replace(' ', ''))

        # get data
        table = parsed_Info.find('table', 'dataframe')
        parsed_rows = table.find_all('tr')
        rows = [header]

        # extract and format the data rows
        for parsed_row in parsed_rows:
            data = parsed_row.find_all('td', 'cellinside')
            row = []

            # process and extract data, handling special cases
            for datum in data:
                text = datum.text.replace('\n', '')

                # remove spaces for specific columns
                if len(row) >= 3:
                    text = text.replace(' ', '')

                # extract the download link for the CSV and DOC files
                if text == 'CSV' or text == 'DOC':
                    anchor = datum.find('a')
                    text = anchor.get('href')

                row.append(text)
            if row:
                rows.append(row)

        # write the extracted data to a csv file
        self.write_csv('part3a-output.csv', rows)

    def task3b(self):
        # url to scrape
        url = 'https://realpython.github.io/fake-jobs/'

        # HTTP GET request to url
        page = req.get(url)

        # parse the HTML content of the page using BeautifulSoup
        parsed_Info = BeautifulSoup(page.content, 'html.parser')

        # get header
        header = ['job_title', 'company_name', 'city', 'state', 'posting_date']

        # get data
        data = [header]

        # find all job card elements
        cards = parsed_Info.find_all('div', 'card-content')

        # extract and format job information from each card
        for card in cards:
            mediaContent = card.find('div', 'media-content')
            job_title = mediaContent.find('h2').text
            company_name = mediaContent.find('h3').text
            content = card.find('div', 'content')
            location = content.find('p', 'location').text.replace('\n', '')
            location = location.replace(' ', '')
            [city, state] = location.split(',')
            posting_date = content.find('p', 'is-small has-text-grey').text.replace(' ', '')
            posting_date = posting_date.replace('\n', '')

            # append the extracted job data to the list
            data.append([job_title, company_name, city, state, posting_date])

        # write the extracted job data to a CSV file
        self.write_csv('part3b-output.csv', data)

    @staticmethod
    def write_csv(filename, data):
        # Write the provided data to a CSV file
        with open('./output/' + filename, 'w') as fptr:
            writer = csv.writer(fptr)
            writer.writerows(data)
        fptr.close()


if __name__ == '__main__':
    # Create an instance of the Lab7 class
    lab6 = Lab6()

    # Execute the task3a method to scrape data and write it to a CSV file
    lab6.task3a()

    # Execute the task3b method to scrape job data and write it to a CSV file
    lab6.task3b()
