#!/bin/sh
# A setup script for constructing the dataset

# Determine mode: valid modes are train, validation, test
if [ -n "$1" ]; then
    MODE=$1
else
    MODE="train"
fi

# Initialize directories
INSTALL_DIR="./data_v6/"
TEMP_DIR="./temp/"
IMAGE_DIR="$INSTALL_DIR$MODE/images/"
MASK_DIR="$INSTALL_DIR$MODE/masks/"

mkdir $INSTALL_DIR $TEMP_DIR $INSTALL_DIR$MODE $IMAGE_DIR $MASK_DIR


download_files() {
    # Download the image URLs (note: not currently being used)
    if [ $MODE = "train" ]; then
        for i in `seq 0 9`; do
            wget -P $TEMP_DIR 'https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-'"$MODE$i"'.tsv'
        done
    else
        wget -P $TEMP_DIR 'https://storage.googleapis.com/cvdf-datasets/oid/open-images-dataset-'"$MODE"'.tsv'
    fi


    # Download the labels
    wget -P $TEMP_DIR 'https://storage.googleapis.com/openimages/v5/'"$MODE"'-annotations-human-imagelabels-boxable.csv'

    # Download the IDs
    wget -P $TEMP_DIR 'https://storage.googleapis.com/openimages/2018_04/'"$MODE/$MODE"'-images-boxable-with-rotation.csv'

    # Download the segmentation IDs
    wget -P $TEMP_DIR 'https://storage.googleapis.com/openimages/v5/'"$MODE"'-annotations-object-segmentation.csv'

    # Download the segmentation masks
    for i in `seq 0 15`; do
        i=`printf "%x\n" $i`
        wget -P $TEMP_DIR 'https://storage.googleapis.com/openimages/v5/'"$MODE"'-masks/'"$MODE"'-masks-'"$i"'.zip'
    done
}

# Download smaller files manually
echo "Downloading files..."
download_files

# Transform the input CSV files
echo "Compiling dataset..."
python compile_dataset.py $MODE

# Download, organize, and clean the images
echo "Downloading images..."
python download_images.py $MODE
python separate_by_class.py $MODE
python clean_data.py $MODE

# Unzip and organize the object masks
echo "Organizing masks..."
python organize_masks.py $MODE


# Delete scratch files
rm -rf $TEMP_DIR
