# Kalshi - Market Analysis & Visualization

This repository serves as a collection of analyses and visualizations produced by members of [Kalshi](https://kalshi.com/)'s community, using public market data.

If you have anything you'd like to contribute, please open a PR and a member of the team will assist in merging your changes. If possible, follow the directory structure established by existing projects.

## Background

Kalshi is a CFTC regulated exchange for [event contracts](https://kalshi.com/learn/what-is-event-contract) which ask yes or no questions about the future. For example, Kalshi lists contracts on [future interest rates](https://kalshi.com/events/economics), weather events, and scientific discoveries.

As every trader is incentivized to price contracts accurately, the markets become valuable forecasting tools. Projects in this repo try to leverage this data to learn about the future.

## Getting Started

If you'd like to run any of these scripts yourself, or build your own, please start by skimming Kalshi's [API documentation](https://trading-api.readme.io/reference/getting-started). Before following the project-specific steps below, please perform the following steps:

1. Install requirements

* [Python 3.11](https://docs.python.org/3/whatsnew/3.11.html)
* [Pip](https://pip.pypa.io/en/stable/installation/)

2. Run `pip3 install -r requirements.txt`

3. Create an account Kalshi.

4. Create the file `client/credentials.yaml` with the following format:

```
username: [[kalshi-username]]
password: [[kalshi-password]]
```

Note that this file is GitIgnored, to prevent accidental commits.


## Projects

### Oscars 2023 Predictions ([OSCARPIC-23](https://kalshi.com/events/OSCARPIC-23))
