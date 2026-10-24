# main.py
import io
import logging
from pathlib import Path

import pandas as pd
from fastapi import FastAPI, File, HTTPException, Query, UploadFile

from src import CSVInfo, DataStorage, MovieInput, MovieResponse

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Movie API")

# Temporary storage: resets whenever the server restarts or reloads
movies = {
    1: {"id": 1, "title": "Movie A", "release_year": 2020},
    2: {"id": 2, "title": "Movie B", "release_year": 2021},
}

# Class 13: one storage object for the whole app. It lives out here (not inside
# an endpoint) so uploaded datasets are still there for the next request.
storage = DataStorage()


@app.get("/health")
def health_check():
    return {"status": "ok"}


# ---------- Demo endpoints (keep these unchanged) ----------

# a path parameter identifies a resource (movie) to retrieve
@app.get("/demo/movies/{movie_id}")
def demo_get_movie(movie_id: int):  # type annotation: it declares the expected type, int
    return {"requested_id": movie_id}


# a query parameter adjusts a request
@app.get("/demo/movies")
def demo_list_movies(limit: int = Query(default=2, ge=1)):
    # The default is 2 when limit is omitted in the query.
    # ge=1 means greater than or equal to one.
    return {"requested_limit": limit}


@app.post("/demo/movies")
def demo_add_movie(movie: MovieInput):
    return movie.model_dump()  # Converts the model to a Python dictionary.


demo_movie_examples = []


@app.post("/demo/movie-examples", response_model=MovieResponse)
def demo_add_movie_example(movie: MovieInput):
    movie_id = len(demo_movie_examples) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    demo_movie_examples.append(record)
    return record


# Class 13 demo: file upload
@app.post("/demo/inspect-csv")
async def demo_inspect_csv(file: UploadFile = File(...)):
    # ... in File(...) means the upload is required.
    contents = await file.read()  # reads as bytes e.g. b"title,year\nMovie A,2020\n"
    return {"filename": file.filename, "size_bytes": len(contents)}


# Class 13 demo: 404 for a missing movie
@app.get("/demo/movie-lookup/{movie_id}", response_model=MovieResponse)
def demo_lookup_movie(movie_id: int):
    movie = movies.get(movie_id)

    if movie is None:
        logger.warning(f"Movie not found: {movie_id}")
        raise HTTPException(status_code=404, detail="Movie not found")

    return movie


# ---------- Class 12 Try It Yourself: Movie API ----------

@app.get("/movies", response_model=list[MovieResponse])
def list_movies(limit: int = Query(default=2, ge=1)):
    # return up to limit movies as a list
    result = list(movies.values())[:limit]
    logger.info(f"Returned {len(result)} movies")
    return result


@app.post("/movies", response_model=MovieResponse)
def add_movie(movie: MovieInput):
    # turn the movie into a dictionary, add the new ID, and store it
    movie_id = len(movies) + 1
    record = movie.model_dump()
    record["id"] = movie_id
    movies[movie_id] = record
    logger.info(f"Added movie: id={movie_id}")
    return record


# ---------- Class 13 Try It Yourself: upload and retrieve a dataset ----------

@app.post("/inspect-csv", response_model=CSVInfo)
async def inspect_csv(file: UploadFile = File(...)):
    # TODO 2: only accept .csv files
    extension = Path(file.filename or "").suffix.lower()
    if extension != ".csv":
        logger.warning(f"Unsupported file format: {extension}")
        raise HTTPException(status_code=400, detail="Only CSV files are accepted")

    # TODO 3: wait for the file, then turn its bytes into a DataFrame
    contents = await file.read()
    try:
        df = pd.read_csv(io.BytesIO(contents))
    except (pd.errors.EmptyDataError, pd.errors.ParserError, UnicodeDecodeError) as error:
        logger.warning(f"Cannot read CSV: {error}")
        raise HTTPException(status_code=400, detail="Cannot read the uploaded CSV")

    # TODO 4: save it, log it, and send back its info
    dataset_id = storage.save_data(df, file.filename)
    logger.info(f"Stored CSV: id={dataset_id}, filename={file.filename}")
    return CSVInfo(
        filename=file.filename,
        rows=df.shape[0],
        columns=df.shape[1],
        column_names=[str(name) for name in df.columns],
        dataset_id=dataset_id,
    )


@app.get("/datasets/{dataset_id}/shape")
def get_dataset_shape(dataset_id: int):
    # TODO 5: look the dataset up; 404 if that ID doesn't exist
    df = storage.get_data(dataset_id)
    if df is None:
        logger.warning(f"Dataset not found: {dataset_id}")
        raise HTTPException(status_code=404, detail="Dataset not found")

    logger.info(f"Retrieved dataset shape: id={dataset_id}")
    return {"dataset_id": dataset_id, "rows": df.shape[0], "columns": df.shape[1]}