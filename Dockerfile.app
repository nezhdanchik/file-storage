FROM python:3.12-slim
WORKDIR /code
COPY . .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
ENTRYPOINT ["gunicorn", "run:app"]
CMD ["--bind", "0.0.0.0:8000"]
