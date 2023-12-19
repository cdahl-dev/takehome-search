# Cribl Takehome (Senior Software Engineer, Search)
A small project that provides the ability to retrieve logs from another machine via a REST API.

## Getting Started
### Prerequisites
This project uses Python 3+. Note that it also runs in pipenv (which will be installed in the next section).

### Installation
To install the project and start the pipenv shell:

    make install

Note: If you exit the shell, run the following to enter it again:

    pipenv shell

### Running Tests
To run unit tests (from pipenv shell):

    make test

### Running the App
To run the API locally on [http://127.0.0.1:5000](http://127.0.0.1:5000) (from pipenv shell):

    make run

## Usage
### Log Search Endpoint

The `logs` endpoint returns the most recent log events within a given file in the /var/log/ folder. It assumes the most recent events are at the bottom of the file.

#### Endpoint URL
`GET` http://127.0.0.1:5000/logs/

#### Query Parameters
| **Name**  | **Type**       | **Required**               | **Description**                          |
| --------- | -------------------- | ---------------------- | ---------------------------------------- |
| `filename` | string | Yes | Name of log file to search within /var/log/ folder. |
| `n` | int | No | Number of lines to return. Defaults to 1000. |
| `keyword` | string | No | If provided, only lines matching keyword will be returned. |

#### Example Usage
http://127.0.0.1:5000/logs/?n=100&filename=wifi.log&keyword=kernel

## Bonus Question
To request the logs from multiple machines via a primary server, the primary would support support an endpoint (with the same query parameters) that would in turn call the API on each of the secondary servers.

[<img src="/images/distributed_search.png" width="450"/>]()

As a simple approach, the primary could wait for each of the secondary servers to return their N results, then sort these logs by date to get the top N most recent across all servers. Assuming we're using NodeJS (rather than Python), a Promise could be used for each API call along with Promise.all().

Some more considerations:
- We'd need proper log parsing to extract the date, and ensure that time zones of the secondary machines are taken into account.
- We'd need the primary server to have a list of the secondary servers configured (along with any authorization required).
- We'd need to think about tradeoffs between getting the results to the user faster vs the accuracy of the most recent logs. Some of the machines could be slower to respond than others (or even fail), and we'd need to consider how to best handle that for the end user.
- I'm assuming that the Log Search API is using AWS API Gateway and Lambda, and that the secondary machines could potentially leverage Cribl Edge.







