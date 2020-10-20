FROM python:3.8-slim as build
COPY . /hoard
RUN cd /hoard && python setup.py bdist_wheel


FROM python:3.8-slim
ENV PIP_NO_CACHE_DIR yes
ENV LD_LIBRARY_PATH /usr/local/lib

RUN \
  apt-get update -yqq && \
  apt-get install -yqq libaio1 && \
  pip install --upgrade pip pipenv

COPY Pipfile* /
RUN pipenv install --deploy --system --ignore-pipfile
COPY lib/* /usr/local/lib/
COPY --from=build /hoard/dist/hoard-*-py3-none-any.whl .
RUN pip install hoard-*.whl

ENTRYPOINT ["hoard"]
