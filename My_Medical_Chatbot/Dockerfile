# Use official Python image as base
FROM python:3.10

# Set the working directory inside the container
WORKDIR /app

# Copy project files to the container
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r hf/requirements.txt

# Expose the port your application runs on
EXPOSE 7860

# Command to run the application
CMD ["python", "hf/app.py"]
