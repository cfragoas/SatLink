FROM python:3.8
WORKDIR /Satlink
COPY ./ ./
RUN pip install -r requirements_web.txt
EXPOSE 8501
COPY satlink_web.py ./satlink_web.py
ENTRYPOINT [ "streamlit", "run" ]
CMD ["satlink_web.py"]