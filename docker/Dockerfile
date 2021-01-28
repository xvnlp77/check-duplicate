FROM python:3.6

COPY ./install_files/* /root/check-duplicate/

ENV LANG "en_US.UTF-8"

RUN chmod +x /root/check-duplicate/start_server \
    && pip install --no-cache-dir -r /root/check-duplicate/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ \
    && pip install --no-cache-dir gunicorn -i https://mirrors.aliyun.com/pypi/simple/ \
    && pip install --no-cache-dir /root/check-duplicate/check_duplicate-0.0.1-py3-none-any.whl

# ignore command line args
ENTRYPOINT /root/check-duplicate/start_server