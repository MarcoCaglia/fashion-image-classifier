# Fashion Image Classifier

## Purpose & Description
The purpose of this repository is to train a binary image classifier, which can predict of a piece of clothing on an image is worn by a model, or if the piece is displayed by itself.

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

NEED TO MAKE HERE A REMARK HOW THE IMAGE LABELER IS WORKING.


### Step 1: Labeling Images (for Training)

The scraper will not scrape the images themselves, but rather the URLs of those images, which will then be stored in the DB (table: images).

To load, label and store the data, the user can use the jupyter notebook scripts/label_images.ipynb. The code will load a random sample of images from the database, present them in the notebook for labeling and will the safe them in the appropriate folder, depending of the user's input.


### Step 2: Running the DVC pipeline

The DVC pipeline is already created and stored in the dvc.yaml file. To reproduce the original model training, the user shoudl run `dvc repro`.
The trained and evaluated model will be saved to the `workdir`.

By default, DVC will store added files in a local minio bucket. Minio can be started by navigating into the `workdir` of this repo and running `docker-compose up`. Note that when running this command for the first time, the user would need to create a bucket called `image-classification`, which is the bucket, that DVC will store files in. By default the minio container runs on port 9000 and the credentials are loaded from the .env file in the `workdir` folder (not the main folder).


### Step 3: Applying the Model

To apply the model, that the dvc pipeline created, run the following code in the console:

```
python3 fashion_image_classifier/label_images.py --model_path=workdir/model.joblib --db_path=workdir/project.db --brand=YOUR_BRAND
```

If the location of the model or the project DB was changed, that would need to be reflected in the function call.
At this moment it is also necessary to pass a specific `brand` for which the images should be labeled.