# Fashion Image Classifier

## Purpose & Description
The purpose of this repository is to train a binary classifier

## Getting Started
You can clone this repo by running 
```
git clone https://github.com/MarcoCaglia/yt-content-analysis@[RELEASE]
```
in your terminal.

### Step 0: Sourcing the data
The repo comes with a scraper for zalando data. To run the scraper, navigate to the `sourcing` directory and run the `zalando_crawler`.

For example like this:
```
cd sourcing/

scrapy crawl zalando_crawler
```

Note: For the scraper to run, you need to have a docker container running. For more details, see here:
https://github.com/scrapy-plugins/scrapy-splash 

By default, the scraper will output a log and write to a database, that are located in the `WORKDIR` that was specified in the `.env` file. By default this is set to `workdir`.

The resulting (sqlite3) `project.db` will contain two tables: pieces and images. Pieces will contain various information about the scraped pieces of clothing and images will contain a reference to each piece in the pieces table, alongside with the image_urls that have been sourced for any given piece.

By default, the scraper will source from zalando.nl. As of now, this can only be changed in the spider code itself.


### Step 1: Labeling Images

### Step 2: Running the DVC pipeline