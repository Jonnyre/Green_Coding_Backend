import requests
import random

def ask_ollama(question):
    url = 'http://localhost:11434/api/generate'

    data = {
        "model": "llama3",
        "prompt": question,
        "stream": False,
        "system": "You are a Senior Developer for Green Coding. Give only the explanation for the improvement in one sentence first and only the better version of the given Code Input second and dont give me anything else. Apply the following rule Avoid function calls in loop headers"
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Fehler beim Senden der Anfrage:", e)
        return None

bad_codes = [
    '''public void processFiles() {
    for (int i = 0; i < calculateFileSize("file1.txt"); i++) {
        // Process each file
        System.out.println("Processing file...");
    }
}''',

    '''public void generateReport() {
    for (int i = 0; i < getReportData().length; i++) {
        // Generate report
        System.out.println("Generating report...");
    }
}''',

    '''public void calculateTotal() {
    int sum = 0;
    for (int i = 0; i < calculateSumValues(10); i++) {
        sum += i;
    }
    System.out.println("Total: " + sum);
}''',

    '''public void processElements() {
    for (int i = 0; i < getElements().length; i++) {
        // Process each element
        System.out.println("Processing element...");
    }
}''',

    '''public void generateCode() {
    for (int i = 0; i < getCodeAtSize() * 2; i++) {
        // Generate code
        System.out.println("Generating code...");
    }
}''',

    '''public void processArrays() {
    int[][] array = getArray();
    for (int i = 0; i < array.length; i++) {
        for (int j = 0; j < array[i].length; j++) {
            // Process each element
            System.out.println("Processing element...");
        }
    }
}''',

    '''public void generateGraph() {
    for (int i = 0; i <= someFunction(); i++) {
        // Generate graph
        System.out.println("Generating graph...");
    }
}''',

    '''public void calculateStatistics() {
    double average = calculateAverage();
    for (int i = 0; i < average; i++) {
        // Calculate statistics
        System.out.println("Calculating statistics...");
    }
}''',

    '''public void processList() {
    List elements = getElements();
    for (int i = 0; i < elements.size(); i++) {
        // Process each element
        System.out.println("Processing element...");
    }
}''',

    '''public void generateMatrix() {
    double[][] matrix = new double[getMatrixSize()][getMatrixSize()];
    for (int i = 0; i < getMatrixSize(); i++) {
        for (int j = 0; j < getMatrixSize(); j++) {
            matrix[i][j] = calculateValue(i, j);
        }
    }
}'''
]

if __name__ == "__main__":
    question = random_code = random.choice(bad_codes)
    answer = ask_ollama(question)
    if answer:
        print("Answer:", answer['response'])
    else:
        print("There was an error.")