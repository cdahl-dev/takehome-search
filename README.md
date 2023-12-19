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


