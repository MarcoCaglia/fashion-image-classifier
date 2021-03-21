# Set Base Image
FROM python:3.9.1

# Set Working Directroy
WORKDIR /home/usr/

# Copy Files
COPY fashion_image_classifier/ /home/usr/fashion_image_classifier/
COPY fashion_dashboard/ /home/usr/fashion_dashboard/
COPY workdir/project.db /home/usr/workdir/project.db
COPY workdir/model.joblib /home/usr/workdir/model.joblib
COPY pyproject.toml /home/usr/pyproject.toml
COPY poetry.lock /home/usr/poetry.lock
COPY .env /home/usr/.env
COPY ./.streamlit ./.streamlit

# Install Poetry and dependencies
RUN pip3 install poetry
RUN poetry env use 3.9.1
RUN poetry install --no-dev

# Spin up Dashboard
CMD poetry run streamlit run fashion_dashboard/fashion_dashboard.py --server.port $PORT