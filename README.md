# Quotes

Issue #1

## Deployment

```bash
$ python seed.py
```

## Usage

```bash
$ python search.py
```

# Delivery

Issue #2

## Deployment

```bash
$ docker run -d --name lexhouk-hw-08 -p 5672:5672 -p 15672:15672 rabbitmq:3.13.6-management-alpine
$ python producer.py
```
