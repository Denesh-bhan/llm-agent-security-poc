FROM python:3.12-slim
WORKDIR /work
RUN useradd --create-home --uid 10001 appuser
USER appuser
CMD ["python", "-c", "print('Sandbox ready: do not mount host secrets or sensitive directories.')"]
