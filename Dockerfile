# init a base image (Alpine is small Linux distro)
FROM python:3.8
EXPOSE 5000
# define the present working directory
WORKDIR /PRICEPREDICT
# copy the contents into the working dir
ADD . /PRICEPREDICT
# run pip to install the dependencies of the flask app
RUN pip install -r requirements.txt
# define the command to start the container
CMD ["python","app.py"]