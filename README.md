# Final project of bootcamp EDVai 2023

## Description

This is the final project of the bootcamp EDVai 2023. 

The project is divide in several parts:
- notebooks: contains the notebooks used to data exploration, data cleaning, data analysis and model creation.
- api: contains the code of the api. The api is used to predict frauds. This code is realized with FastAPI.
- app: contains the code of the web application realized with Gradio.

Other files:
- data: contains the data used in the project.
- model: contains the models used in the project.
- docs: contains the documentation of the project.

## Installation

To install the project, you need to clone the repository and install the requirements.
The requirements are in the three files: notebooks_requirements.txt, api_requirements.txt and app_requirements.txt.

Depends on you the part of the project you want to use, you need to install the requirements of the part.

```bash
python -m venv venv
pip install -r notebooks_requirements.txt
pip install -r api_requirements.txt
pip install -r app_requirements.txt
```

## Usage
If you want to use the notebooks, you need to run the notebooks in the following order:
- 01__Adaptacion.ipynb
- 02__Correlacion.ipynb
- 03__Preparacion.ipynb
- 04__Clustering.ipynb
- 05__Modelo.ipynb

If you want to use the api, you need to run the following command:
```bash
python main.py
```

If you want to use the app, you need to run the following command:
```bash
python app.py
```

## Deploy


