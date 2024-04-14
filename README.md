# Generate-Result-list

Generate-Result-list is a Python project designed to retrieve and analyze student results from JEC (Jabalpur Engineering College) website. It utilizes automation with Selenium, solves Captcha using Pytesseract, and performs data analysis using Pandas and Numpy.

## Features

- Retrieves student results from the JEC website.
- Utilizes automation with Selenium for web scraping.
- Solves Captchas to access result pages.
- Analyzes fetched data using Pandas and Numpy for further processing.

## Prerequisites

Before running the project on your system, make sure you have the following libraries installed:

1. Selenium
2. Pytesseract
3. Requests
4. Pandas
5. Numpy

## Usage

1. Clone the repository to your local machine.
2. Install the required libraries using pip (if not already installed).
3. Ensure you have the necessary drivers (e.g., chromedriver) for Selenium automation.
4. Run the Python script `generate_result_list.py`.
5. Follow the on-screen prompts to retrieve and analyze the student results.

## How it Works

1. The script uses Selenium to navigate to the JEC website and retrieve the required information.
2. Pytesseract is employed to solve any Captchas encountered during the process.
3. Once the data is fetched, it is stored and analyzed using Pandas and Numpy for further insights.

## Contributing

Contributions are welcome! If you have any ideas for improvements, new features, or bug fixes, feel free to open an issue or submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
