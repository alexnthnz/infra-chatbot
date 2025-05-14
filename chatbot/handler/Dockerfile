FROM public.ecr.aws/lambda/python:3.13

# Copy requirements.txt and install dependencies
COPY requirements.txt ${LAMBDA_TASK_ROOT}/
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire src directory
COPY src/ ${LAMBDA_TASK_ROOT}/src/

# Set the Lambda handler
CMD ["src.lambda_handler.handler"]
