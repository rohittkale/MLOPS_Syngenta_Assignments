from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from app.iris_data import IrisDataFilter
import matplotlib.pyplot as plt
import os

app = FastAPI()

# Initialize the IrisDataFilter with the path to your dataset
iris_data_filter = IrisDataFilter(
    file_path='D:\\VIIT\\Semester-3\\MLOPS\\IndustrySession\\SyngentaSession\\PracticalAssignments\\Assignment2\\data\\Iris.csv'  # Adjust the file path as needed
)

@app.get("/species/")
async def get_filtered_data(species: str):
    # Filter data by species
    filtered_data = iris_data_filter.filter_by_species(species)

    if filtered_data.empty:
        raise HTTPException(status_code=404, detail="Species not found")

    # Generate and save the visualizations for each column separately
    image_paths = []
    for column in filtered_data.columns[:-1]:  # Exclude the species column
        plt.figure()
        filtered_data[column].hist(bins=20, figsize=(5, 4))
        plt.title(f'{species} - {column}')
        image_path = f"{species}_{column}.png"
        plt.savefig(image_path)
        plt.close()

        # Add the image path to the list
        image_paths.append(image_path)

        # Check if the image was actually saved
        if not os.path.exists(image_path):
            raise HTTPException(status_code=500, detail="Image generation failed")

    # Return the filtered data and the paths to the visualization images
    return {"data": filtered_data.to_dict(orient="records"), "images": image_paths}


@app.get("/visualize/")
async def visualize_species(species: str, column: str):
    # Construct the image path based on species and column
    image_path = f"{species}_{column}.png"

    # Check if the image exists
    if not os.path.exists(image_path):
        raise HTTPException(status_code=404, detail="Image not found")

    # Return the image as a FileResponse
    return FileResponse(image_path)



# Searching on google:
# 1. http://127.0.0.1:8000/species/?species=Iris-setosa
# 2. http://127.0.0.1:8000/visualize/?species=Iris-setosa&column=SepalLengthCm

