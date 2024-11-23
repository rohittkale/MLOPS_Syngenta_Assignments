from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.iris_data import IrisDataFilter
import matplotlib.pyplot as plt
import os

app = FastAPI()

iris_data_filter = IrisDataFilter(
    file_path='./Iris.csv'  
)

@app.get("/species/")
async def get_filtered_data(species: str):
    # Filter data by species
    filtered_data = iris_data_filter.filter_by_species(species)

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="Species not found")

    image_paths = []
    for column in filtered_data.columns[:-1]: #-1 excludes species column
        plt.figure()
        filtered_data[column].hist(bins=20, figsize=(5, 4))
        plt.title(f'{species} - {column}')
        image_path = f"{species}_{column}.png"
        plt.savefig(image_path)
        plt.close()

        image_paths.append(image_path)

        if not os.path.exists(image_path):
            raise HTTPException(status_code=500, detail="Image generation failed")

    # Return the filtered data and the paths to the visualization images
    return {"data": filtered_data.to_dict(orient="records"), "images": image_paths}


@app.get("/visualize/")
async def visualize_species(species: str, column: str):
    image_path = f"{species}_{column}.png"

    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")
        
    return FileResponse(image_path)



# Searching on google:
# 1. http://127.0.0.1:8000/species/?species=Iris-setosa
# 2. http://127.0.0.1:8000/visualize/?species=Iris-setosa&column=SepalLengthCm

