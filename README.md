![Build](https://github.com/word-club/backend/actions/workflows/ci.yml/badge.svg?branch=main)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# Word Club
- a community/publication feeds system.
- built using Django, DRF and Django Channels

## Fresh Start
To run a raw backend version with a SQLite database
```shell script
make fresh
```

### Authentication

We have some public APIs which works without any authentications but for the critical APIs `Token Authentication` system is used.

## Available Apps

| Apps           | Level |
| -------------- | ----- |
| administration | I     |
| account        | I     |
| hashtag        | I     |
| community      | II    |
| publication    | III   |
| comment        | IV    |
| image          | IV    |
| vote           | IV    |
| bookmark       | IV    |
| share          | IV    |
| hide           | IV    |
| block          | IV    |
| report         | IV    |
| notification   | V     |