FROM alpine
WORKDIR /app
RUN echo '0 * * * * /usr/bin/python /app/main.py' > /etc/crontabs/root
RUN apk update && apk add --no-cache git python3 py3-dotenv py3-pip py3-requests
RUN pip install GitPython --break-system-packages
COPY src/ .
COPY --chmod=755 docker-entrypoint.sh .
ENTRYPOINT ["/app/docker-entrypoint.sh"]