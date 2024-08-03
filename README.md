# Quotes

[Issue #1](https://github.com/lexhouk/goit-pyweb-hw-08/issues/1)

## Deployment

```bash
$ docker run -d --name lexhouk-hw-08-redis -p 6379:6379 redis
$ python seed.py
```

## Usage

```bash
$ python search.py
```

# Delivery

[Issue #2](https://github.com/lexhouk/goit-pyweb-hw-08/issues/2)

## Deployment

```bash
$ docker run -d --name lexhouk-hw-08-rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.13.6-management-alpine
$ python producer.py
```

## Usage

```bash
$ python consumer.py
```
