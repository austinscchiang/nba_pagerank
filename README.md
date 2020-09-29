# NBA Pagerank
@ronnyweasle and i attempt to bet on nba games :basketball: :dollar:

## Installation

Install pip dependencies:
```
$ ./install.sh
```

## Run

```
$ source .env/bin/activate
$(.env) python3 src/nba_pagerank.py
```

You should see some example output similar to:
```
Top 5 in regular season (desc):
('Philadelphia 76ers', 0.011342068952168117)
('Houston Rockets', 0.011220608066890538)
('Golden State Warriors', 0.011218920207841456)
('Portland Trail Blazers', 0.01116438983647992)
('Milwaukee Bucks', 0.011150255412696063)

Top 5 in playoffs (desc):
('Toronto Raptors', 0.018790852863348317)
('Golden State Warriors', 0.017500406827584886)
('Milwaukee Bucks', 0.016370632043035415)
('Boston Celtics', 0.014150194947316022)
('Philadelphia 76ers', 0.013864573328212434)
```

## Lint

We use [`mypy`](https://github.com/python/mypy) for static type-checking.
```
$ source .env/bin/activate
$(.env) mypy src/
```

## Formatting 

We use [`black`](https://github.com/psf/black) for linting.
```
$ source .env/bin/activate
$(.env) black src/
```
