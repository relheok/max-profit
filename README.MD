# max-profit
A python 3 project to calculate the optimal production according to
limited resources.

## Command

	./max-profit QUANTITY* PRICE*

Where you specifiy the quantity of each resource and the price of each product.

Example:

	./max-profit 10 100 10 0 200 200 200 200 200 -c conf/subject.csv

## Configuration file
The configuration file is a CSV containing:

* First line:
  * First column: Empty / free
  * Others: The names of the products
* Others:
  * First column: The names of the resources (such as time, cost, etc...)
  * Others: The quantity of each resource needed by the product

All the elements are separated by a semicolon.

## Documentation
The project is documented thanks to Sphinx

### Prerequisites
You must have shynx. To install it, run:

	pip install sphinx

### Commands
To generate the documentation, run:

	make -C doc html

An html file is created at `doc/build/html/index.html`.
You can open it in your web browser to see the project documentation.
