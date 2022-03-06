FROM python
RUN pip3 install boto3
RUN mkdir /source
COPY . /source 
CMD [“python”, “/source/batchload.py”]