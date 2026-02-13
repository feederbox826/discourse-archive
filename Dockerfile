FROM alpine
WORKDIR /app
RUN apk update && apk add --no-cache git python3 py3-dotenv py3-pip py3-requests
RUN pip install GitPython --break-system-packages
COPY src/ .
CMD ["python", "/app/main.py"]