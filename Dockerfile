FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    FTIRFUN_API_BASE_URL=https://ftir.fun \
    FTIRFUN_MCP_TRANSPORT=streamable-http \
    FTIRFUN_MCP_HOST=0.0.0.0 \
    FTIRFUN_MCP_PORT=8001

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY ftirfun_mcp_server.py /app/ftirfun_mcp_server.py

EXPOSE 8001

CMD ["python", "ftirfun_mcp_server.py", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8001"]
