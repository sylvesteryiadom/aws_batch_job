FROM python
RUN pip3 install boto3
RUN mkdir /source
COPY . /source 
CMD [“python”, “/source/batch_upload.py”]