# README
# Author: Benjamin Song, Xiaohan Jia, Jingya Yu, Xinyu He, Jeremy Dou

## Data Folder
  | - train_data
  |  | - Barcelona
  |  | - Paris
  |  | - NewOrleans
  |  | - Bali
  |  | - Cancun
  |  | - Tokyo
  |  | - AmalfiCoast
  |  | - Sydney
  |  | - Phuket
  |  | - BoraBora
  |  | - Florence
  |  | - Maui
  |  | - Vancouver
  |  | - London
  |  | - Dubai
  |  | - NewYorkCity
  |  | - Rome
  |  | - SanFrancisco
  |  | - Tulum
  |  | - RioDeJaneiro
  |  | - Amsterdam
  | - data
  |  | - BestSeason
  |  | - Winter
  |  | - Fall
  |  | - Summer
  |  | - Spring

## Code files

```
code of web-crawler
Foler: TripAdvisor Code

code
├── preprocess.py
├── season_keywords.py
├── vectorspace.py
├── evaluation.py
└── stem.py

```


## Run
Step0: Use TripAdvisor Code as web-crawler to collect data
Step1: Get Season keywords
```
$ python3 season_keywords.py 30
```
output:
season_queries.output
```
Parameter '30' is the number of words you want to get.

Step2: Build the model and get result output
```
$ python3 vectorspace.py
```
output:
training_result.output
```


