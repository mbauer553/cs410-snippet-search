#!/bin/bash

# Name of the Lambda runtime
LAMBDA_RUNTIME="amazonlinux:2"

# Create a Docker container with the Lambda runtime
docker run -v $PWD:/var/task -it $LAMBDA_RUNTIME /bin/bash -c "
  # Install development tools
  yum groupinstall -y 'Development Tools'

  # Install Python 3.11 from source
  yum install -y wget openssl-devel bzip2-devel libffi-devel
  wget https://www.python.org/ftp/python/3.11.0/Python-3.11.0.tgz
  tar xzf Python-3.11.0.tgz
  cd Python-3.11.0
  ./configure --enable-optimizations
  make altinstall
  cd ..
  rm -rf Python-3.11.0*
  
  # Set up a virtual environment
  python3.11 -m venv venv
  source venv/bin/activate

  # Install necessary dependencies
  pip install -r /var/task/requirements.txt -t /var/task/lambda_layer/python/lib/python3.11/site-packages/

  # Deactivate the virtual environment
  deactivate
"

# Zip the Lambda layer
cd lambda_layer
zip -r python.zip *
cd ..

# Clean up: Remove the virtual environment
rm -rf venv

# rm -rf lambda_layer
# mkdir -p lambda_layer/python/
# pip3 install -r requirements.txt -t lambda_layer/python/

# # cp -r /path/to/your/virtualenv/tree_sitter lambda_layer/python/

# cd lambda_layer
# zip -r python.zip *
# cd ..