from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
import pandas as pd
import matplotlib.pyplot as plt
import os
from typing import Optional

app = FastAPI()
templates = Jinja2Templates(directory="index")  # Create a directory named "index"

class IrisDataFilter:
    def __init__(self, file_path):
        self.data = pd.read_csv(file_path)

    def filter_by_species(self, species):
        filtered_data = self.data[self.data['Species'] == species]
        return filtered_data

    def plot_feature_distribution(self, filtered_data, feature, output_file):
        plt.figure(figsize=(8, 6))
        plt.hist(filtered_data[feature], bins=10, color='blue', alpha=0.7)
        plt.title(f'Distribution of {feature} for {filtered_data["Species"].iloc[0]}')
        plt.xlabel(feature)
        plt.ylabel('Frequency')
        plt.grid(True)
        plt.savefig(output_file)
        plt.close()

# Initialize the IrisDataFilter with the path to your dataset
iris_data_filter = IrisDataFilter(file_path='./datasets/Iris.csv')

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/species/")
async def get_filtered_data(species: str, feature: Optional[str] = None):
    filtered_data = iris_data_filter.filter_by_species(species)

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="Species not found")

    response = {
        "data": filtered_data.to_dict(orient="records")
    }

    if feature:
        if feature not in filtered_data.columns:
            raise HTTPException(status_code=400, detail="Feature not found in dataset.")
        
        image_path = f"{species}_{feature}_distribution.png"
        iris_data_filter.plot_feature_distribution(filtered_data, feature, image_path)

        if not os.path.exists(image_path):
            raise HTTPException(status_code=500, detail="Image generation failed")

        response["image"] = image_path

    return response

@app.get("/visualize/")
async def visualize_species(species: str, feature: str):
    image_path = f"{species}_{feature}_distribution.png"

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    return FileResponse(image_path)
