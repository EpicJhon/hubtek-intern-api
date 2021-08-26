FROM python:3.9-alpine3.14
# AS ROOT
RUN adduser -D worker
WORKDIR /home/worker


# Install python deps
COPY --chown=worker:worker requirements.txt requirements.txt
# Install build deps
RUN apk add --no-cache --virtual .build-deps g++ gcc musl-dev python3-dev libffi-dev openssl-dev cargo &&\
    # Install deps
    apk add --no-cache runuser &&\
    # Install packages (for what virtualenv? we run on Docker)
    runuser -l worker -c 'pip install --no-cache-dir --user -r requirements.txt' &&\
    # Uninstall build deps
    apk del .build-deps


# Copy app content to workdir
COPY --chown=worker:worker . .

# AS USER
USER worker

VOLUME ["/home/worker/db"]
EXPOSE 9050

# Add python packages to env
ENV PATH="/home/worker/.local/bin:${PATH}"

# Fix permissions
RUN chmod +x /home/worker/entrypoint.sh
RUN chmod +x /home/worker/bootstrap.sh

# Run bootstrap script
USER root
ENTRYPOINT ["/bin/sh", "/home/worker/entrypoint.sh"]
CMD ["/home/worker/bootstrap.sh"]
