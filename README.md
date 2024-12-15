# Stock-Snap

Stock-Snap is a Python library for extracting real-time stock market data. It provides an easy-to-use interface for fetching stock quote details across various exchanges.

## Features

- **Fetch Real-Time Data**: Retrieve real-time stock quotes for any ticker symbol.
- **Multi-Exchange Support**: Get stock data from multiple exchanges.
- **Easy Integration**: Simple and efficient methods to integrate into your projects.

## Installation

Install the package using pip:

```bash
pip install stock-snap
```
Fetching Stock Details
```python
ticker_symbol = 'AAPL'
details = stock_snap.fetch_details(ticker_symbol)
print(details)
```
### Example Output

The `fetch_details` method returns a dictionary with exchange symbols as keys and their corresponding stock quote details as values.

## Requirements

- Python 3.12

## Contributing

Contributions are welcome! Follow these steps to contribute:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature-branch`).
3. Make your changes and commit them (`git commit -m 'Add new feature'`).
4. Push to the branch (`git push origin feature-branch`).
5. Create a pull request.

## Demo
[Youtube Tutorial](https://youtu.be/kFupzwhbY5I?si=wQEbURStkkrEs57B)

This project is licensed under the MIT License.

## Contact

For any issues or questions, please open an issue on this repository.
