# Dockerfile
FROM public.ecr.aws/lambda/python:3.11

# Upgrade pip and install dependencies
RUN pip install --upgrade pip

# Copy application code and requirements file
COPY app app
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Set the Lambda handler
CMD ["app.lambda_handler.handler"]
