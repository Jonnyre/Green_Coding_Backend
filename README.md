
# Green Coding Optimization Service

This project provides a Flask-based web service that analyzes Java code for potential improvements or corrections, with a focus on green coding practices. The service utilizes an AI model to suggest optimizations and provide corrected code snippets.

## Features

- **Code Analysis for Green Coding Practices**: Automatically checks Java code for potential optimizations.
- **Correction Suggestions**: Offers detailed corrections and improvements for the given code.
- **Few-Shot Learning**: Uses few-shot examples to enhance the quality of the suggestions.

## Installation

### 1. Clone the Repository

```sh
git clone https://github.com/yourusername/green-coding-optimization-service.git
cd green-coding-optimization-service
```

### 2. Create and Activate a Virtual Environment (Optional, but Recommended)

```sh
python -m venv venv
source venv/bin/activate   # On Windows: `venv\Scripts\activate`
```

### 3. Install Dependencies

```sh
pip install -r requirements.txt
```

### 4. Install Ollama

To run the Ollama model locally, you need to set up the Ollama environment. Follow these steps:

1. **Download Ollama**:

    Visit the Ollama website or repository to download the installer for your operating system.

2. **Install Ollama**:

    Follow the installation instructions on the Ollama website.

3. **Start Ollama Service**:

    After installation, start the Ollama service on your local machine. Ensure it is running on localhost and port 11434.

### 5. Configure the AI Model

Update the `url` variable in the `ask_ollama` function to point to the correct endpoint of the AI model.

```python
url = 'http://localhost:11434/api/chat'
```

### Run the Service

Start the Flask server:

```sh
python app.py
```

The service will be available at `http://127.0.0.1:5000`.

## Usage

### API Endpoint

- **URL**: `/`
- **Method**: `POST`
- **Content-Type**: `application/json`

### Request Body

- `data` (string): The Java code to be analyzed.
- `mode` (string, optional): The operating mode. Default is `few_shot`.

### Example Request:

```json
{
  "data": "1: public static void main(String[] args) { 
 2:    // Filter null values 
 3:    boolean allowNulls = false; 
 4:    for (Integer v : new Integer[] { 0, 1, 23, 2, 27 }) { 
 5:        if (allowNulls) { 
 6:            System.out.println(v); 
 7:        } 
 8:    } 
 9: }",
  "mode": "few_shot"
}
```

### Response

The service returns the corrected code along with an explanation of the changes. Example response:

```json
{
  "content": "#?# Avoid For-each loops if not all elements are accessed. Use while loops instead. #?#\n-!- 1: public static void main(String[] args) {\n 2: // Filter null values \n 3: boolean allowNulls = false; \n 4:  Integer[] values = { 0, 1, 23, 2, 27 };\n5: int length = values.length;\n6:  if (allowNulls) {\n7: for (int i = 0; i < length ; i++) {\n8: System.out.println(values[i]);\n9:}\n10:}\n11:} -!-\n$!$ 4-8 $!$"
}
```
