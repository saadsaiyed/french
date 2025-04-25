# French Listening Practice Game

This project is a web application designed to help users practice their French listening skills through an interactive game. Users will listen to numbers spoken in French and will be prompted to enter the corresponding digits. The application provides real-time feedback on their answers, making it a fun and engaging way to learn.

## Features

- Mobile-friendly interface
- Interactive listening practice
- Real-time feedback on user input
- Multiple user support

## Project Structure

```
french-listening-practice
├── app
│   ├── __init__.py
│   ├── routes.py
│   ├── static
│   │   ├── css
│   │   │   └── styles.css
│   │   └── js
│   │       └── scripts.js
│   └── templates
│       ├── base.html
│       ├── index.html
│       └── game.html
├── requirements.txt
├── run.py
└── README.md
```

## Installation

1. Clone the repository:
   ```
   git clone <repository-url>
   cd french-listening-practice
   ```

2. Create a virtual environment:
   ```
   python -m venv venv
   ```

3. Activate the virtual environment:
   - On Windows:
     ```
     venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```
     source venv/bin/activate
     ```

4. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

## Usage

1. Run the application:
   ```
   python run.py
   ```

2. Open your web browser and go to `http://127.0.0.1:5000`.

3. Follow the on-screen instructions to start practicing your French listening skills!

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for any suggestions or improvements.

## License

This project is licensed under the MIT License. See the LICENSE file for more details.