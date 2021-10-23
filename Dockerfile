FROM python:3
FROM ruby:2.7.1
RUN gem install bundler
ADD src
RUN pip install -r ./requirements.txt
CMD [ "python", "./src/my_script.py" ]
