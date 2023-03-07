# Solidity Documentation Generator

This is a Python script that generates HTML documentation for Solidity smart contracts.

## How to use

1. Clone the repository:
```bash
git clone https://github.com/abhinavmir/soldocs.git
```
1. Edit the `src/config.soldoc` file to specify the following:

- `directory`: The directory containing your Solidity files.
- `css`: The path to your CSS file.
- `output`: The path and name of the output HTML file.

Example `config.soldoc` file:
```js
directory = contracts/
css = css/style.css
output = docs/index.html
```

3. Run the script:
```bash
python src/soldocs.py
```

## Features

- Generates HTML documentation for all Solidity contracts in a directory.
- Uses regular expressions to extract comments and function signatures from Solidity code.
- Supports markdown syntax in comments.
- Generates an index of all contracts and functions.
- Uses the Skeleton CSS framework for styling.

## Dependencies

- Python 3
- `os`
- `re`

## License

This code is licensed under the MIT License. See the [LICENSE](https://opensource.org/license/mit/) for details.