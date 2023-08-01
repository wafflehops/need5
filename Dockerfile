FROM python:3.11.0-alpine

WORKDIR /app


COPY requirements.txt /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/


CMD sh -c 'if [ "$ENVIRONMENT" = "prod" ]; then \
              export CHAT_CHANNEL=1110385416021999707; \
              export GUI_CHANNEL=1129462597087924265; \
           else \
              export CHAT_CHANNEL=989947070985162795; \
              export GUI_CHANNEL=1129428972715901102; \
           fi && python3 main.py'

