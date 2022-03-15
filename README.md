# Bittooth

A senior project about Bitcoin value prediction.

## Description

This project tries to create a model which predicts the value of bitcoin from both statistically analysis and Twitter sentiment on a given period of time. Many different models are designed and tested to see which gives the best results.

Below here is our project structure. One node corresponds to one notebook.

![Bittooth Data-flow](.blob/data-flow.svg)

## Installation

There are two method of installations: with or without virtual environment. You only need to install with virtual environment if you are a developer of the project.

Our project uses [DVC](https://dvc.org/) to source control our data to Google Drive remote. Please refer to [here](https://github.com/kevctae/Bittooth#pulling-data-with-dvc) for more information on pulling data.

### Install without virtual environment

1. Install [Twint](https://github.com/kevctae/twint).

    ```bash
    pip install --upgrade git+https://github.com/kevctae/twint.git
    ```

2. Install dependencies from `requirements.txt`.

    ```bash
    pip install -r ./setup/requirements.txt
    ```

3. Run Jupyter Notebook.

    ```bash
    jupyter notebook
    ```

### Install with virtual environment (Development)

1. Install [pyenv](https://github.com/pyenv/pyenv#installation).
2. Install [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv#installation)
3. Run setup script based on the OS:
    - (macOS) Allow executable on `setup-mac.sh` and run the script.

        ```bash
        cd ./setup
        chmod +x ./setup-mac.sh
        ./setup-mac.sh
        ```

### Pulling data with DVC

In order to pull data from Google Drive, you will first need permission to access the Drive from [kevctae](https://github.com/kevctae/). Once you have permision, you may pull data using command (make sure to install DVC from [here](https://dvc.org/doc/install)):

```bash
dvc pull
```

*It will ask you to get verification code on the first pull. Follow the provided URL and login to your Google account*



## Acknowledgement

* [Twint](https://github.com/twintproject/twint)
* [TvDatafeed](https://github.com/StreamAlpha/tvdatafeed)

## Authors

* [kevctae](https://github.com/kevctae/)
* [minchayisara](https://github.com/minchayisara)
* [pattanadeen](https://github.com/pattanadeen)
* [Julian-Kota-Kikuchi](https://github.com/Julian-Kota-Kikuchi)