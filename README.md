# QA Classification System

A system for classifying questions and answers using OpenAI's API.

## Features

- **Enhanced Logging**: Consistent log file naming and comprehensive logging setup
- **Flexible Configuration**: Support for multiple configuration files
- **Batch Processing**: Configurable batch size and processing parameters
- **Detailed Classification**: Comprehensive prompt template with detailed classification criteria

## Configuration

The system supports configuration through `config.ini` files in the following locations:
- `./config.ini`
- `./classify/config.ini`

### Configuration Parameters

- `api_key`: Your OpenAI API key
- `model`: OpenAI model to use (default: gpt-4)
- `end_row`: Maximum number of rows to process
- `batch_size`: Number of items to process in each batch
- `log_file`: Name of the log file (default: qa_classifier.log)

## Usage

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Configure your API key in `config.ini`:
```ini
[openai]
api_key = your_openai_api_key_here
model = gpt-4
```

3. Run the classifier:
```bash
python qa_classifier.py
```

## Files

- `qa_classifier.py`: Main classification script with enhanced logging
- `config.ini`: Main configuration file
- `classify/config.ini`: Alternative configuration file location
- `prompt_template.txt`: Expanded prompt template with detailed classification criteria
- `requirements.txt`: Python dependencies

## Recent Updates

- Updated OpenAI API key and model configuration for improved functionality
- Enhanced logging setup with consistent log file naming
- Adjusted processing parameters (end_row and batch_size) for better performance
- Expanded prompt template with detailed classification criteria
- Streamlined project structure by removing outdated files