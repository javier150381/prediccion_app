from fastapi import FastAPI
import ee

# Initialize Earth Engine
try:
    ee.Initialize()
except Exception:
    ee.Authenticate()
    ee.Initialize()

app = FastAPI()

@app.get("/history")
def history(lat: float, lon: float, fecha_inicio: str, fecha_fin: str):
    """Return precipitation history for a point."""
    point = ee.Geometry.Point([lon, lat])
    collection = (
        ee.ImageCollection('UCSB-CHG/CHIRPS/DAILY')
        .filterDate(fecha_inicio, fecha_fin)
        .filterBounds(point)
        .select('precipitation')
    )
    region = collection.getRegion(point, scale=1000).getInfo()
    header = region[0]
    data = [dict(zip(header, row)) for row in region[1:]]
    return data
