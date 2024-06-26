from flask import Flask, request, jsonify
import requests


few_shot_examples = [
    {
      "role": "user",
      "content": "1: public static void main(String[] args) { \n 2:    // Filter null values \n 3:    boolean allowNulls = false; \n 4:    for (Integer v : new Integer[] { 0, 1, 23, 2, 27 }) { \n 5:        if (allowNulls) { \n 6:            System.out.println(v); \n 7:        } \n 8:    } \n 9: }"
    },
    {
      "role": "system",
      "content": "#?# Avoid For-each loops if not all elements are accessed. Use while loops instead. #?#\n-!- 1: public static void main(String[] args) {\n 2: // Filter null values \n 3: boolean allowNulls = false; \n 4:  Integer[] values = { 0, 1, 23, 2, 27 };\n5: int length = values.length;\n6:  if (allowNulls) {\n7: for (int i = 0; i < length ; i++) {\n8: System.out.println(values[i]);\n9:}\n10:}\n11:} -!-\n$!$ 4-8 $!$"
    },
    {
      "role": "user",
      "content": "1: public static void main(String[] args) {\n 2:\n 3:     int counter = 0;\n 4:\n 5:     ArrayList<Integer> elements = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10));\n 6:\n 7:     for (int element : elements) {\n 8:         if (counter > 5) {\n 9:             System.out.print(element);\n 10:         }\n 11:         counter++;\n 12:     }\n 13: }"
    },
    {
      "role": "system",
      "content": "#?# Avoid For-each loops if not all elements are accessed. Use while loops instead. #?#\n-!- 1:     public static void main(String[] args) { 2: 3:         int counter = 0; 4: 5:         ArrayList<Integer> elements = new ArrayList<>(Arrays.asList(1, 2, 3, 4, 5, 6, 7, 8, 9, 10)); 6: 7:         if (counter > 5) { 8:             for (int i = 0; i < elements.size(); i++) { 9:                 System.out.print(elements.get(i)); 10:             } 11:         } 12:     }  -!-\n$!$ 7-12 $!$"
    },
    {
      "role": "user",
      "content": "1: public static void main(String[] args) {\n 2:     Integer number = 10;\n 3:     Integer divisor = 5;\n 4:     Integer result = 0;\n 5:     result = number / divisor;\n 6:     System.out.println(\"Result: \" + result);\n 7: }"
    },
    {
      "role": "system",
      "content": "#?# Avoid automatic boxing and unboxing. If a variable is changed, a primitive data type should always be used instead of a boxed/wrapper data type. #?#\n-!- 1:     public static void main(String[] args) { 2:         int number = 10; 3:         int divisor = 5; 4:         int result = 0; 5:         result = number / divisor; 6:         System.out.println(\"Result: \" + result); 7:     }  -!-\n$!$ 4-5 $!$"
    },
    {
      "role": "user",
      "content": "1: public static void main(String[] args) {\n 2:     Short myShort = 10;\n 3:     System.out.println(\"Initial value: \" + myShort);\n 4:     myShort = 20;\n 5:     System.out.println(\"After first change: \" + myShort);\n 6:     myShort++;\n 7:     System.out.println(\"After increment: \" + myShort);\n 8:     myShort = (short) (myShort * 2);\n 9: }"
    },
    {
      "role": "system",
      "content": "#?# Avoid automatic boxing and unboxing. If a variable is changed, a primitive data type should always be used instead of a boxed/wrapper data type. #?#\n-!- 1:     public static void main(String[] args) { 2:         short myShort = 10; 3:         System.out.println(\"Initial value: \" + myShort); 4:         myShort = 20; 5:         System.out.println(\"After first change: \" + myShort); 6:         myShort++; 7:         System.out.println(\"After increment: \" + myShort); 8:         myShort = (short) (myShort * 2); 9:     } -!-\n$!$ 1,4,6,8 $!$"
    },
    {
      "role": "user",
      "content": "1:public static void main(String[] args) { \n 2:String[] fruits = {\"apple\", \"banana\", \"orange\", \"grape\", \"pineapple\", \"watermelon\", \"kiwi\", \"strawberry\", \"blueberry\", \"mango\"}; \n 3:Map<String, Integer> map = new HashMap<>(); \n 4:Random random = new Random(); \n 5:for (String fruit : fruits) { \n 6:map.put(fruit, random.nextInt(10) + 1); \n 7:} \n 8:}"
    },
    {
      "role": "system",
      "content": "#?# Do not create Map, List or Stack without size. Initializing the size at the beginning helps avoid unnecessary memory allocation. #?#\n-!- 1:public static void main(String[] args) { \n 2:String[] fruits = {\"apple\", \"banana\", \"orange\", \"grape\", \"pineapple\", \"watermelon\", \"kiwi\", \"strawberry\", \"blueberry\", \"mango\"}; \n 3:Map<String, Integer> map = new HashMap<>(fruits.length); \n 4:Random random = new Random(); \n 5:for (String fruit : fruits) { \n 6:map.put(fruit, random.nextInt(10) + 1); \n 7:} \n 8:} \n 9:public static void main(String[] args) { \n 10:ArrayList<Integer> list = new ArrayList<>(10); \n 11:for (int i = 5; i < 15; i++) { \n 12:list.add(i); \n 13:}; \n 14:} -!-\n$!$ $!$"
    },
    {
      "role": "user",
      "content": "1:public static void main(String[] args) { \n 2:String[] userInfos = { \n 3:\"135|bend|bend@gmail.com\", \n 4:\"246|airfry|airfry@gmail.com\", \n 5:\"357|leela|leela@gmail.com\" \n 6:}; \n 7:for (String userInfo : userInfos) { \n 8:System.out.println(getUserEmail(userInfo)); \n 9:} \n 10:} \n 11:static String getUserEmail(String userInfo) { \n 12:String[] data = userInfo.split(\"\\|\"); \n 13:return data[2]; \n 14:}"
    },
    {
      "role": "system",
      "content": "#?# Do not use the Java split method. Instead, create a separate split method that fits your application exactly.  #?#\n-!- 1:public static void main(String[] args) { \n 2:String[] userInfos = { \n 3:\"135|bend|bend@gmail.com\", \n 4:\"246|airfry|airfry@gmail.com\", \n 5:\"357|leela|leela@gmail.com\" \n 6:}; \n 7:for (String userInfo : userInfos) { \n 8:System.out.println(getUserEmail(userInfo)); \n 9:} \n 10:} \n 11:static String getUserEmail(String userInfo) { \n 12:String[] data = customSplit(userInfo, '|'); \n 13:return data[2]; \n 14:} \n 15:static String[] customSplit(String str, char delimiter) { \n 16:int count = 1; \n 17:for (char ch : str.toCharArray()) { \n 18:if (ch == delimiter) { \n 19:count++; \n 20:} \n 21:} \n 22:String[] result = new String[count]; \n 23:int index = 0; \n 24:int start = 0; \n 25:for (int i = 0; i < str.length(); i++) { \n 26:if (str.charAt(i) == delimiter) { \n 27:result[index++] = str.substring(start, i); \n 28:start = i + 1; \n 29:} \n 30:} \n 31:result[index = str.substring(start); \n 32:return result; \n 33:} -!-\n$!$ 14 $!$"
    },
    {
      "role": "user",
      "content": "1: public static void main(String[] args) { \n 2:String data = \"dog,cat,bird,fish,lion,tiger\"; \n 3:String[] animals = data.split(\",\"); \n 4:ArrayList<String> animalList = new ArrayList<>(Arrays.asList(animals)); \n 5:System.out.println(animalList); \n 6:}"
    },
    {
      "role": "system",
      "content": "#?# Do not use the Java split method. Instead, create a separate split method that fits your application exactly.  #?#\n-!- 1: public static void main(String[] args) { \n 2:String data = \"dog,cat,bird,fish,lion,tiger\"; \n 3:String[] animals = customSplit(data, \",\"); \n 4:ArrayList<String> animalList = new ArrayList<>(Arrays.asList(animals)); \n 5:System.out.println(animalList); \n 6:} \n 7:public static String[] customSplit(String input, String delimiter) { \n 8:ArrayList<String> result = new ArrayList<>(); \n 9:int start = 0; \n 10:int end = input.indexOf(delimiter); \n 11:while (end != -1) { \n 12:result.add(input.substring(start, end)); \n 13:start = end + delimiter.length(); \n 14:end = input.indexOf(delimiter, start); \n 15:} \n 16:result.add(input.substring(start)); \n 17:return result.toArray(new String[0]); \n 18:} -!-\n$!$ 4 $!$"
    },
    {
      "role": "user",
      "content": "1: public void processFiles() {  \n 2:     for (int i = 0; i < calculateFileSize(\"file1.txt\"); i++) {  \n 3:         // Process each file  \n 4:         System.out.println(\"Processing file...\");  \n5 .     }  \n6 . } "
    },
    {
      "role": "system",
      "content": "#?# Avoid function calls in loop headers. Function calls are expensive operations that can significantly impact performance. #?#\n-!- 1: public void processFiles() {  \n 2:     int fileSize = calculateFileSize(\"file1.txt\");  \n 3:     for (int i = 0; i < fileSize; i++) {  \n 4:         // Process each file  \n 5:         System.out.println(\"Processing file...\");  \n 6:     }  \n 7: }  \n  -!-\n$!$ 2 $!$"
    },
    {
      "role": "user",
      "content": "1: public void generateReport() {  \n 2:     for (int i = 0; i < getReportData().length; i++) {  \n 3:         // Generate report  \n 4:         System.out.println(\"Generating report...\");  \n 5:     }  \n 6: } "
    },
    {
      "role": "system",
      "content": "#?# Avoid function calls in loop headers. Function calls are expensive operations that can significantly impact performance. #?#\n-!- 1: public void generateReport() {  \n 2:     String[] reportData = getReportData();  \n 3:     for (int i = 0; i < reportData.length; i++) {  \n 4:         // Generate report  \n 5:         System.out.println(\"Generating report...\");  \n 6:     }  \n 7: }  -!-\n$!$ 2 $!$"
    },
    {
      "role": "user",
      "content": "1: public class exampl6_0 {  \n 2:     public static final List<String> LIST = new ArrayList<>();  \n 3:     public static final Set<String> SET = new HashSet<>();  \n 4:  \n 5:     public static void main(String[] args) {  \n 6:         LIST.add(\"hello\");  \n 7:         SET.add(\"world\");  \n 8:         // ...  \n 9:     }  \n 10: }  \n"
    },
    {
      "role": "system",
      "content": "#?# Avoid shared static collections: Static collections shared across multiple instances or modules can lead to concurrency issues and memory leaks. #?#\n-!- 1: public class Example6_0 {  \n 2:     private final List<String> list = new ArrayList<>();  \n 3:     private final Set<String> set = new HashSet<>();  \n 4:  \n 5:     public void addItems() {  \n6 .         list.add(\"hello\");  \n 7:         set.add(\"world\");  \n 8:     }  \n 9:  \n 10:     public void displayContents() {  \n 11:         System.out.println(\"List: \" + list);  \n 12:         System.out.println(\"Set: \" + set);  \n 13:     }  \n 14:  \n 15:     public static void main(String[] args) {  \n 16:         Example6_0 example = new Example6_0();  \n 17:         example.addItems();  \n 18:         example.displayContents();  \n 19:     }  \n 20: }  \n 21:  \n -!-\n$!$ 2-3 $!$"
    },
    {
      "role": "user",
      "content": "1: public class exampl6_1 {  \n 2:     public static final List<String> LIST = new ArrayList<>();  \n 3:  \n 4:     public void addElement() {  \n 5:         LIST.add(\"new element\");  \n 6:     }  \n 7: } "
    },
    {
      "role": "system",
      "content": "#?# Avoid shared static collections: Static collections shared across multiple instances or modules can lead to concurrency issues and memory leaks. #?#\n-!- 1: public class Example6_1 {  \n 2:     private final List<String> list = new ArrayList<>();  \n 3:  \n 4:     public void addElement() {  \n 5:         list.add(\"new element\");  \n 6:     }  \n 7:  \n 8:     public List<String> getList() {  \n 9:         return list;  \n 10:     }  \n 11:  \n 12:     public static void main(String[] args) {  \n 13:         Example6_1 example = new Example6_1();  \n 14:         example.addElement();  \n 15:         System.out.println(\"List: \" + example.getList());  \n 16:     }  \n 17: } -!-\n$!$ 2 $!$"
    },
    {
      "role": "user",
      "content": "1:private static void selectAllUsers(Connection conn, String table) throws SQLException { \n 2:    Statement stmt = conn.createStatement(); \n 3:    String query = \"SELECT * FROM \" + table; \n 4:    try (ResultSet rs = stmt.executeQuery(query)) { \n 5:        while (rs.next()) { \n 6:            String username = rs.getString(\"username\"); \n 7:            String email = rs.getString(\"email\"); \n 8:            System.out.println(\"Username: \" + username + \", Email: \" + email); \n 9:        } \n 10:    } \n 11:}"
    },
    {
      "role": "system",
      "content": "#?# Do not use the asterisk symbol (*) in SQL queries to select all columns of a table. Instead, you should specifically query only those fields that are required for your application. #?# \n-!- 1:private static void selectAllUsers(Connection conn, String table) throws SQLException { \n 2: Statement stmt = conn.createStatement(); \n 3: String query = \"SELECT username, email FROM \" + table; \n 4: try (ResultSet rs = stmt.executeQuery(query)) { \n 5: while (rs.next()) { \n 6: String username = rs.getString(\"username\"); \n 7: String email = rs.getString(\"email\"); \n 8: System.out.println(\"Username: \" + username + \", Email: \" + email); \n 9: } \n 10: } \n 11:} -!-\n$!$ 3-9 $!$"
    },
    {
      "role": "user",
      "content": "1:private static void selectProductsWithCondition(Connection conn) throws SQLException { \n 2: String query = \"SELECT * FROM Products WHERE Price > 100\"; \n 3: try (PreparedStatement pstmt = conn.prepareStatement(query); ResultSet rs = pstmt.executeQuery()) { \n 4: while (rs.next()) { \n 5: String productName = rs.getString(\"product_name\"); \n 6: double price = rs.getDouble(\"price\"); \n 7: System.out.println(\"Product: \" + productName + \", Price: \" + price); \n 8: } \n 9: } \n 10:}"
    },
    {
      "role": "system",
      "content": "#?# Do not use the asterisk symbol (*) in SQL queries to select all columns of a table. Instead, you should specifically query only those fields that are required for your application. #?#\n-!- 1:private static void selectProductsWithCondition(Connection conn) throws SQLException { \n 2: String query = \"SELECT product_name, price FROM Products WHERE Price > 100\"; \n 3: try (PreparedStatement pstmt = conn.prepareStatement(query); ResultSet rs = pstmt.executeQuery()) { \n 4: while (rs.next()) { \n 5: String productName = rs.getString(\"product_name\"); \n 6: double price = rs.getDouble(\"price\"); \n 7: System.out.println(\"Product: \" + productName + \", Price: \" + price); \n 8: } \n 9: } \n 10:}  -!-\n$!$ 2-8 $!$"
    },
    {
      "role": "user",
      "content": "1: private static void repeatSimpleSelect(Connection conn) throws SQLException {  \n 2: Statement stmt = conn.createStatement();  \n 3: for (int i = 0; i < 1000; i++) {  \n 4: String query = \"SELECT salary FROM Employees\";  \n 5: try (ResultSet rs = stmt.executeQuery(query)) {  \n 6: while (rs.next()) {  \n 7: // Process results  \n 8: }  \n 9: }  \n 10: }  \n 11: }"
    },
    {
      "role": "system",
      "content": "#?# Avoid executing SQL queries in a loop #?#\n-!-  1: private static void repeatSimpleSelect(Connection conn) throws SQLException {  \n 2: Statement stmt = conn.createStatement();  \n 3: String query = \"SELECT salary FROM Employees\";  \n 4:  \n 5: try (ResultSet rs = stmt.executeQuery(query)) {  \n 6: while (rs.next()) {  \n 7: // Process results  \n 8: }  \n 9: }  \n 10: } -!-\n$!$ 3-6 $!$"
    },
    {
      "role": "user",
      "content": "1: private static void repeatCountQuery(Connection conn) throws SQLException {  \n 2: int i = 0;  \n 3: while (i < 100) {  \n 4: String query = \"SELECT COUNT(id) FROM Products\";  \n 5: try (  \n 6: PreparedStatement pstmt = conn.prepareStatement(query);  \n 7: ResultSet rs = pstmt.executeQuery()) {  \n 8: if (rs.next()) {  \n 9: int count = rs.getInt(1);  \n 10: }  \n 11: }  \n 12: i++;  \n 13: }  \n 14: }"
    },
    {
      "role": "system",
      "content": "#?# Avoid executing SQL queries in a loop #?#\n-!- 1: private static void repeatCountQuery(Connection conn) throws SQLException {  \n 2: String query = \"SELECT COUNT(id) FROM Products\";  \n 3: int count = 0;  \n 4:  \n 5: try (PreparedStatement pstmt = conn.prepareStatement(query);  \n 6: ResultSet rs = pstmt.executeQuery()) {  \n 7: if (rs.next()) {  \n 8: count = rs.getInt(1);  \n 9: }  \n 10: }  \n 11:  \n 12: for (int i = 0; i < 100; i++) {  \n 13: // use count  \n 14: }  \n 15: } -!-\n$!$ 3-7 $!$"
    },
    {
      "role": "user",
      "content": "1: public void processFile() { \n 2:     int i = 0; \n 3:     File file = new File(\"example.txt\"); \n 4:     FileInputStream fis = new FileInputStream(file); \n 5:     try { \n 6:         while ((i = fis.read()) != -1) { \n 7:             System.out.print((char) i); \n 8:          } \n 9:      } catch (IOException e) { \n 10:         e.printStackTrace(); \n 11:      } finally { \n 12:         if (fis != null) { \n 13:             try { \n 14:                 fis.close(); \n 15:              } catch (IOException e) { \n 16:                 e.printStackTrace(); \n 17:              } \n 18:          } \n 19:      } \n 20: } "
    },
    {
      "role": "system",
      "content": "#?# Utilizing 'try with resources' for handling 'AutoCloseable' interfaces, promoting efficient resource management and minimizing environmental impact. #?#\n-!- 1: public void processFile() { \n 3:     int i = 0; \n 4:     File file = new File(\"example.txt\"); \n 4: \n 5:     try (FileInputStream fis = new FileInputStream(file)) { \n 6:        while ((i = fis.read()) != -1) { \n 7:             System.out.print((char) i); \n8:         } \n9:     } catch (IOException e) { \n10:        e.printStackTrace(); \n11:     } \n 12: } \n 13: -!-\n$!$ 3-5 $!$"
    },
    {
      "role": "user",
      "content": "1: public void writeToFile() { \n 2:     try { \n 3:         PrintWriter writer = new PrintWriter(new FileWriter(\"example.txt\")); \n 4:         writer.println(\"Hello World!\"); \n 5:      } catch (IOException e) { \n 6:         e.printStackTrace(); \n 7:      } finally { \n 8:         if (writer != null) { \n 9:             writer.close(); \n 10:          } \n 11:      } \n 12: }"
    },
    {
      "role": "system",
      "content": "#?# Utilizing 'try with resources' for handling 'AutoCloseable' interfaces, promoting efficient resource management and minimizing environmental impact. #?#\n-!- 1: public void writeToFile() { \n 2:     try (PrintWriter writer = new PrintWriter(new FileWriter(\"example.txt\"))) { \n 3:         writer.println(\"Hello World!\"); \n 4:     } catch (IOException e) { \n 5:         e.printStackTrace(); \n 6:     } \n 7: } \n 8: -!-\n$!$ 2-3 $!$"
    },
    {
      "role": "user",
      "content": "1:public class Main { \n2:    public static void main(String[] args) { \n3: \n4:        for (Integer v : new Integer[] { 0, 1, 23, 2, 27 }) { \n5:            if (v % 2 != 0) { \n6:                System.out.println( v + \" is odd\"); \n7:            } \n8:        } \n9:    } \n10:}"
    },
    {
      "role": "system",
      "content": "#?# No green coding optimisation necessary. #?#\n-!-  1:public class Main { \n2:    public static void main(String[] args) { \n3: \n4:        for (Integer v : new Integer[] { 0, 1, 23, 2, 27 }) { \n5:            if (v % 2 != 0) { \n6:                System.out.println( v + \" is odd\"); \n7:            } \n8:        } \n9:    } \n10:} \n  -!-\n$!$ $!$"
    },
    {
      "role": "user",
      "content": "1:import java.util.ArrayList; \n2: \n3:class Main { \n4: \n5:    public static void main(String[] args) { \n6: \n7:        int number = 10; \n8:        int divisor = 5; \n9:        int result = 0; \n10:        result = number / divisor; \n11:        System.out.println(\"Result: \" + result); \n12: \n13:        ArrayList<Integer> myNumbers = new ArrayList<Integer>(); \n14:        myNumbers.add(1); \n15:        myNumbers.add(2); \n16:        myNumbers.add(3); \n17:        myNumbers.add(4); \n18: \n19:    } \n20: \n21:} \n22:"
    },
    {
      "role": "system",
      "content": "#?# No green coding optimisation necessary. #?#\n-!- 1:import java.util.ArrayList; \n2: \n3:class Main { \n4: \n5:    public static void main(String[] args) { \n6: \n7:        int number = 10; \n8:        int divisor = 5; \n9:        int result = 0; \n10:        result = number / divisor; \n11:        System.out.println(\"Result: \" + result); \n12: \n13:        ArrayList<Integer> myNumbers = new ArrayList<Integer>(); \n14:        myNumbers.add(1); \n15:        myNumbers.add(2); \n16:        myNumbers.add(3); \n17:        myNumbers.add(4); \n18: \n19:    } \n20: \n21:} \n22: -!-\n$!$ $!$"
    }
]


def ask_ollama(code, mode):
    url = 'http://localhost:11434/api/chat'

    system_prompt = """
                You are a green coding expert. When provided with a piece of code, your task is to:

                Analyze the code for potential improvements or corrections.
                Provide a very short explanation of what was corrected or improved, surrounded by #?#.
                Present the corrected code, surrounded by -!-.
                Name the lines where the changes where made, each line must be named separately, separated by a comma, surrounded by $!$.
                Use the following format:


                #?# Explanation of the corrections or improvements #?#

                -!- Corrected code -!-

                $!$ line numbers where corrections were made $!$


                Here is an example input and output to demonstrate the format:

                Input:
                1: public void add_numbers(int a, int b) {
                2:        int result = a + b;
                3:        System.out.println(result);
                4: }
                
                
                Output:
                #?# Improved the function to return the result instead of printing it for better reusability and testability #?#

                -!-
                1: public int add_numbers(int a, int b) {
                2:        return a + b;
                3: }
                -!-

                $!$
                2,3
                $!$

                Correct the next given code and remember to apply the markers '#?#' , '-!-' , '$!$' correctly."""


    messages = [{"role": "system", "content": system_prompt}]
    if mode == "few_shot":
        messages += few_shot_examples
         
    messages.append({"role": "user", "content": code})

    data = {
        "model": "llama3",
        "messages": messages,
        "stream": False
    }

    try:
        response = requests.post(url, json=data)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print("Fehler beim Senden der Anfrage:", e)
        return None

app = Flask(__name__)

@app.route('/', methods=['POST'])
def handle_request():
    data = request.json
    input_strings = data.get('data')
    mode = data.get('mode', 'few_shot')
    
    answer = ask_ollama(input_strings, mode)
    content = answer.get("message", {}).get("content", "")

    if content:
        return content
    else:
        return jsonify({"error": "Failed to get a response from Ollama"}), 500
     


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)