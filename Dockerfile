# Set Base Image
FROM python:3.9.1

# Install Poetry (system dependecy)
RUN pip3 install poetry

# Run as non-root user
RUN adduser heroku_user
USER heroku_user

# Set Workdir
WORKDIR /home/heroku_user

# Copy Files
COPY fashion_image_classifier/ ./fashion_image_classifier/
COPY fashion_dashboard/ ./fashion_dashboard/
COPY workdir/project.db ./workdir/project.db
COPY workdir/model.joblib ./workdir/model.joblib
COPY pyproject.toml ./pyproject.toml
COPY poetry.lock ./poetry.lock
COPY .env ./.env
# Note that heroku_user would not have write access by default to the
# below directory
COPY --chown=heroku_user:heroku_user ./.streamlit/ ./.streamlit/

# Install dependecies (project dependecies)
RUN poetry install --no-dev

# Spin up Dashboard
CMD poetry run streamlit run fashion_dashboard/fashion_dashboard.py --server.port $PORT