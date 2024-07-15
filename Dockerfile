#ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24


# Use Python 3.10 base image
FROM python:3.10

# Set working directory inside the container
WORKDIR /app

# Copy everything from the current directory to the /app directory inside the container
COPY . /app/

# Install required packages specified in requirements.txt
RUN pip install -r requirements.txt

# Install libmediainfo
RUN apt-get update && apt-get install -y libmediainfo0v5 libmediainfo-dev

# Specify the command to run your application
CMD ["python", "bot.py"]

# TG: @Sunrises_24
# ALL FILES UPLOADED - CREDITS 🌟 - @Sunrises_24


