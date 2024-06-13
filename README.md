# IPL Statistics Scraper

## Overview

This project is a comprehensive web scraping solution designed to gather detailed statistics about the Indian Premier League (IPL) from the ESPN Cricinfo website. The data collected by this project provides a deep insight into the performance of teams and players in the IPL, making it a valuable resource for cricket enthusiasts, sports analysts, and data scientists alike.

The project uses Scrapy, a powerful and flexible open-source framework for extracting data from websites. Scrapy spiders are used to navigate the ESPN Cricinfo website, follow links, and extract structured data from the web pages. This data is then processed and stored in a MongoDB database for easy access and analysis.

## Spiders

The project includes several different spiders, each designed to scrape a specific type of data:

- `team_results`: Gathers data about the performance of each team in the IPL, including the number of matches played, won, lost, and more.
- `batting_avg`: Collects data about the batting averages of players.
- `bowling_avg`: Collects data about the bowling averages of players.

## Pipelines

The data scraped by these spiders is processed by Scrapy pipelines. These pipelines clean and format the data, handle any necessary conversions, and store the data in the MongoDB database.

## Utilities

In addition to the Scrapy spiders and pipelines, the project also includes various utility scripts and modules that assist with tasks such as managing the database connection, handling errors, and more.

## Conclusion

Overall, this project represents a complete solution for gathering and storing detailed IPL statistics. It showcases the power of web scraping with Scrapy and provides a solid foundation for any project that requires reliable and up-to-date cricket data.
