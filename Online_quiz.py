import mysql.connector

# 🔗 DATABASE CONNECTION
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="1111",   # 
    database="quiz_app"
)

cursor = conn.cursor()

# 👤 REGISTER
def register():
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, password))
    conn.commit()
    print("✅ Registered successfully!")


# 🔐 LOGIN
def login():
    username = input("Enter username: ")
    password = input("Enter password: ")

    cursor.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
    user = cursor.fetchone()

    if user:
        print(f"✅ Login successful! Welcome {username}")
        return user[0], username
    else:
        print("❌ Invalid credentials")
        return None, None


# ❓ ADD QUESTIONS
def add_questions():
    cursor.execute("DELETE FROM questions")

    questions = [

        # PYTHON
        ("Python is?", "Language", "Car", "Game", "Food", "Language", "Python"),
        ("Keyword for function?", "def", "fun", "define", "function", "def", "Python"),
        ("List symbol?", "[]", "{}", "()", "<>", "[]", "Python"),
        ("Loop in python?", "for", "repeat", "loop", "iterate", "for", "Python"),
        ("File extension?", ".py", ".java", ".sql", ".txt", ".py", "Python"),

        # SQL
        ("SQL stands for?", "Structured Query Language", "Simple Query", "System Query", "None", "Structured Query Language", "SQL"),
        ("Fetch data command?", "SELECT", "GET", "FETCH", "SHOW", "SELECT", "SQL"),
        ("Delete command?", "DELETE", "REMOVE", "DROP", "CLEAR", "DELETE", "SQL"),
        ("Update command?", "UPDATE", "MODIFY", "CHANGE", "EDIT", "UPDATE", "SQL"),
        ("Primary key?", "Unique", "Duplicate", "Null", "None", "Unique", "SQL"),

        # GK
        ("Capital of India?", "Delhi", "Mumbai", "Chennai", "Kolkata", "Delhi", "GK"),
        ("Sun rises from?", "East", "West", "North", "South", "East", "GK"),
        ("National animal?", "Tiger", "Lion", "Elephant", "Dog", "Tiger", "GK"),
        ("Currency?", "Rupee", "Dollar", "Euro", "Yen", "Rupee", "GK"),
        ("India continent?", "Asia", "Europe", "Africa", "America", "Asia", "GK"),

        # HISTORY
        ("First PM of India?", "Nehru", "Gandhi", "Modi", "Patel", "Nehru", "History"),
        ("Independence year?", "1947", "1950", "1945", "1930", "1947", "History"),
        ("Who discovered India?", "Columbus", "Vasco da Gama", "Cook", "None", "Vasco da Gama", "History"),
        ("Taj Mahal by?", "Shah Jahan", "Akbar", "Babur", "Aurangzeb", "Shah Jahan", "History"),
        ("Father of Nation?", "Gandhi", "Nehru", "Patel", "Bose", "Gandhi", "History"),
    ]

    query = """INSERT INTO questions 
    (question, option1, option2, option3, option4, correct_answer, topic)
    VALUES (%s, %s, %s, %s, %s, %s, %s)"""

    cursor.executemany(query, questions)
    conn.commit()

    print("✅ Questions added successfully!")


# 🧪 START QUIZ
def start_quiz(user_id):
    print("\n📚 Select Topic:")
    print("1. Python")
    print("2. SQL")
    print("3. GK")
    print("4. History")

    choice = input("Enter choice: ")

    topics = {
        "1": "Python",
        "2": "SQL",
        "3": "GK",
        "4": "History"
    }

    if choice not in topics:
        print("❌ Invalid choice!")
        return

    topic = topics[choice]

    cursor.execute("SELECT * FROM questions WHERE topic=%s LIMIT 5", (topic,))
    questions = cursor.fetchall()

    score = 0

    for i, q in enumerate(questions, 1):
        print(f"\n📌 Q{i}: {q[1]}")
        print("1.", q[2])
        print("2.", q[3])
        print("3.", q[4])
        print("4.", q[5])

        try:
            ans = int(input("Enter option (1-4): "))
            options = [q[2], q[3], q[4], q[5]]

            if options[ans - 1] == q[6]:
                score += 1
        except:
            print("❌ Invalid input!")

    print("\n🎯 Your Score:", score)

    cursor.execute(
        "INSERT INTO results (user_id, score, topic, played_at) VALUES (%s, %s, %s, NOW())",
        (user_id, score, topic)
    )
    conn.commit()


# 📊 VIEW RESULTS (FINAL PERFECT OUTPUT)
def view_results(user_id, username):
    cursor.execute("""
        SELECT score, topic, played_at 
        FROM results 
        WHERE user_id=%s 
        ORDER BY played_at DESC
    """, (user_id,))
    
    data = cursor.fetchall()

    if not data:
        print("\n❌ No quiz history found!")
        return

    print(f"\n👤 User: {username}")
    print("📊 ===== YOUR QUIZ HISTORY =====")

    for i, (score, topic, time) in enumerate(data, 1):
        print(f"""
Attempt {i}
📚 Topic  : {topic}
🎯 Score  : {score}/5
⏰ Played : {time}
-----------------------------""")


# MAIN PROGRAM
current_user = None
current_username = None

while True:
    print("\n===== QUIZ SYSTEM =====")
    print("1. Register")
    print("2. Login")
    print("3. Start Quiz")
    print("4. Add Questions (Run Once)")
    print("5. View Results")
    print("6. Exit")

    choice = input("Enter choice: ")

    if choice == "1":
        register()

    elif choice == "2":
        current_user, current_username = login()

    elif choice == "3":
        if current_user:
            start_quiz(current_user)
        else:
            print("❌ Please login first!")

    elif choice == "4":
        add_questions()

    elif choice == "5":
        if current_user:
            view_results(current_user, current_username)
        else:
            print("❌ Please login first!")

    elif choice == "6":
        break