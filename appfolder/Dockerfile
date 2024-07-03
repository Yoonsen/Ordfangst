FROM python:3.8
        EXPOSE 8501
        WORKDIR /wildcards.py
        COPY requirements.txt ./requirements.txt
        RUN pip3 install -r requirements.txt
        COPY . .
        CMD streamlit run wildcards.py
        