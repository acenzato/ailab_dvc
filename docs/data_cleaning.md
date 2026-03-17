# Data preparation

Most of the time in a real production scenario we don't have clean curated data. Data comes in many forms and fashions:

- the client already has some data but it was never meant for ML training
- there's no data at all, we need to collect it ourselves
- there's already a good public dataset but was collected with another task in mind so labels/data format are not quite what we would like

In any case, chances are that the data is not ready to use for training.  
Cleaning and preparing raw data can involve lots of steps and is very project specific. This is not a course on Data Engineering so we will focus just on some very basic example to showcase DVC usage.

## Data Lineage

When transforming/modifying data it is essential that all transformation steps are reproducible, reversible, reviewable. You should always be able to answer this questions:

- which dataset originates from?
- what transformations where applied to it?
- why did we modify it?

This is called Data Lineage: the full Directed Acyclic Graph of data + transforms that produced this specific piece of data.

Since today's goal is just to illustrate some basic DVC capability and why it can be useful we will not try to achieve full data lineage.  
This is a common tradeoff between exploratory design/development speed and overall process reliability.  
Keep in mind though that an ML-based product without full Data Lineage will eventually bite you in the... back

## Raw dataset

Let's then start making it easy to retrieve the raw data even if we later modify it:

```bash
dvc mv datasets/pokemon datasets/pokemon_raw
git commit -m "Rename raw data: pokemon -> pokemon_raw"
git push
```

We just renamed the dataset directory. We did it through DVC because it automatically handles the creation/deletion of `.gitignore` files for `datasets/pokemon` and `datasets/pokemon_raw`

Notice that when we push data to the remote DVC is actually pushing just the metadata since the files themselves didn't change. Even with a huge dataset the rename is very fast.

> **NOTE:** suffixing the dataset with `_raw` is not necessarily "the best practice", it is a "sufficently good enough practice". We could have achieved the same thing leaving the name intact, adding a git tag `data/pokemon/v0.1.0` and then modifying it in-place.  
>There's tradeoffs to be made:
> - do I need to have both raw and clean data on the filesystem at the same time?
> - while working on the project how often do I need to switch back and forth from raw to clean data?
> - does it make sense to make the raw data fit into the "versioning" paradigm as "the first version" or should we treat it as a completely different entity?

## Uniform image format

Now we start working on data cleaning. This can get messy and we don't want to pollute our `main` branch with the intermediate steps of data cleaning.  
It is a good practice to create a git branch where we can perform data transformations and experiment a bit, until we are satisfied. We can then merge back in the `main` branch.

```bash
git checkout -b data/pokemon-cleaning
```

Let's use pillow to convert all images to `.png`

```bash
# add missing deps
uv add pillow

# change dataset format
python src/preprocessing/unify_img_format.py datasets/pokemon_raw/images datasets/pokemon/images --format png
cp datasets/pokemon_raw/labels.csv datasets/pokemon/labels.csv

# commit the new dataset
dvc add datasets/pokemon
git commit -m "Init new pokemon dataset in .png format"
```

Now we want all of them to be square

```bash
python src/preprocessing/crop.py datasets/pokemon/images datasets/pokemon/images
dvc add datasets/pokemon
git commit -m "Crop to square with size = min(h, w)"
```

Notice how this time we didn't create a new dataset like `pokemon_v1`, we simply overwrote the existing pokemon dataset. No need to keep multiple copies of the data, git and DVC take care of that for us. We can yolo our way through transformations, deleting/overwriting data.

Speaking of which... Ops, we messed-up: there's one image where quirtle is not centered as we would like. And we overwrote the source image!  

![](squirtle_crop_bad.png)

Easy enough, we can revert the previous commit:

```bash
git revert HEAD
dvc checkout datasets/pokemon
```

> **NOTE:** `git revert` is one of those commands that are not auto-synched with DVC commands, we therefore need to manually call `dvc checkout`

All the image edits are now rolled-back and we can manually crop the special case image

![](squirtle_crop_ok.png)

Let's get back to script-processing the images

```bash
python src/preprocessing/crop.py datasets/pokemon/images datasets/pokemon/images
dvc add datasets/pokemon
git commit -m "square-crop images"
```

## INTERRUPTION! 

New data just came in! You have to stop working on Pokémons to dedicate your full attention to Disney Princesses! Top priority.

We where mid-way with our Pokémon preprocessing, but that's not a big deal, we just switch to another branch!

```bash
git checkout main
```

Notice how the work-in-progress Pokémon dataset just disappeared! DVC and git are synched and in the `main` branch we don't have a Pokémon dataset yet; DVC therefore removed the Pokémon dataset from the filesystem.  
All the Pokémon data is safely backed-up in cloud storage and locally persisted on your local filesystem in the DVC cache, it can easily be restored.

Now we create a new branch for Disney Princesses and add the new raw data there

```bash
git checkout -b data/disney-princesses
dvc add datasets/disney_princesses
git commit -m "Add raw data for disney_princesses dataset"
```

Nevermind, Disney Princesses were not that high priority, you can revert back to Pokémon

## Back to Pokémon

Let's resize all images to 128x128

```bash
# back to pokemon branch
git checkout data/pokemon-cleaning

# resize to 128x128
python src/preprocessing/resize.py --size 128 datasets/pokemon/images datasets/pokemon/images
dvc add datasets/pokemon
git commit -m "square-crop images"
```

We can now rename all the images to have a consistent naming convention

```bash
python src/preprocessing/rename.py datasets/pokemon
dvc add datasets/pokemon
git commit -m "Rename images with progressive zero-padded numbers"
```

## Merge to main

Ok now Pokémon dataset is done, we can merge it back to `main` and assign a version number to it

```bash
git switch main
git merge data/pokemon-cleaning
git push
git tag -a data/pokemon/v1.0.0 -m "pokemon: crop, resize to 128x128 and progressive image names"
git push origin data/pokemon/v1.0.0
```
