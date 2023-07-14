# LDAP Integration with Python3

This project demonstrates how to integrate LDAP (Lightweight Directory Access Protocol) with Python 3.

## Installation and Setup

1. Create a virtual environment:
virtualenv -p python venv

2. Activate the virtual environment:
source venv/bin/activate

3. Install the project requirements:
pip install -r requirements.txt

4. Create a `.env` file similar to the `.env.example` provided and add your LDAP credentials.

5. Set the `ACCESS_GROUP` and `PERMISSION_ACCESS_GROUP` in the `.env` file to configure the desired access groups.

## Usage

Run the following command to start the server:
python server.py

## Contributing

Contributions are welcome! If you would like to contribute to this project, please follow these guidelines:

1. Fork the repository and clone it locally.

2. Create a new branch for your feature or bug fix.

3. Make your changes, ensuring that your code follows the project's style guide.

4. Write tests to cover any new functionality or changes.

5. Commit your changes and push your branch to your forked repository.

6. Submit a pull request with a detailed description of your changes.

## License

This project is licensed under the [MIT License](LICENSE).

Enjoy using LDAP integration with Python! If you have any questions or feedback, please don't hesitate to reach out.
