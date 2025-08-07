# Prediccion App

## Environment Variables

- `SECRET_KEY`: secret used to sign JWT tokens. Set this to a strong random value before running the application.

## Running with Docker

1. Build the image:

   ```bash
   docker build -t prediccion-app .
   ```

2. Run the container:

   ```bash
   docker run -e SECRET_KEY=your-secret -p 8000:8000 prediccion-app
   ```

The application will be available at `http://localhost:8000`.
