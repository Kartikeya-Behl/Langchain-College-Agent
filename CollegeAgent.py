from langchain_ollama import ChatOllama 
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.tools import tool
from langchain_classic.agents import create_tool_calling_agent, AgentExecutor

# ======== LLM ========
llm = ChatOllama(model="qwen2.5:3b", temperature=0)


# ======== TOOL DEFINITIONS (Using LangChain @tool decorator) ========
@tool
def calculate_attendance(total_classes: int, attended_classes: int) -> str:
    """Calculates the student's attendance percentage and exam eligibility status."""
    if total_classes <= 0:
        return "Error: Total classes must be greater than 0."
    
    percentage = (attended_classes / total_classes) * 100
    eligible = "Eligible for Exam" if percentage >= 75 else "Not Eligible for Exam"
    
    return f"Attendance: {percentage:.2f}% | Status: {eligible}"

@tool
def calculate_result(marks_list: list[float]) -> str:
    """Calculates average marks, grade, and pass/fail status from a list of 5 subject marks."""
    if len(marks_list) != 5:
        return "Error: Please provide exactly 5 subject marks as a list."
    
    average = sum(marks_list) / 5
    
    if average >= 90:
        grade = "A"
    elif average >= 75:
        grade = "B"
    elif average >= 60:
        grade = "C"
    else:
        grade = "D"
        
    status = "Pass" if average >= 50 else "Fail"
    
    return f"Average Marks: {average:.2f} | Grade: {grade} | Status: {status}"

@tool
def calculate_fee_balance(total_fee: float, amount_paid: float) -> str:
    """Calculates the pending course fee balance amount."""
    pending = total_fee - amount_paid
    return f"Pending Fee Amount: ₹{pending:.2f}"

@tool
def calculate_library_fine(delayed_days: int) -> str:
    """Calculates the library fine amount based on the number of delayed days."""
    fine = 5 * delayed_days
    return f"Library Fine: ₹{fine:.2f} (₹5 per day for {delayed_days} days)"

@tool
def calculate_hostel_fee(monthly_fee: float, months_stayed: int) -> str:
    """Calculates the total hostel fee based on monthly rate and duration of stay."""
    total_fee = monthly_fee * months_stayed
    return f"Total Hostel Fee: ₹{total_fee:.2f} for {months_stayed} months"


# BONUS CHALLENGE: STUDENT INFORMATION TOOL

# Defining a mock student database
STUDENT_DB = {
    "S101": {"name": "Aravind", "department": "Computer Science", "year": "3rd"},
    "S102": {"name": "Sneha", "department": "Electronics", "year": "2nd"},
    "S103": {"name": "Rahul", "department": "Mechanical", "year": "4th"}
}

@tool
def get_student_info(student_id: str) -> str:
    """Retrieves student registration details from the secure database using their Student ID."""
    student_id = student_id.upper().strip()
    if student_id in STUDENT_DB:
        info = STUDENT_DB[student_id]
        return f"Student Found -> Name: {info['name']} | Dept: {info['department']} | Year: {info['year']}"
    return f"Error: Student ID '{student_id}' not found in the campus database."


# ======== AGENT SETUP ========

# Grouping all tools into a list
tools_list = [
    calculate_attendance,
    calculate_result,
    calculate_fee_balance,
    calculate_library_fine,
    calculate_hostel_fee,
    get_student_info
]

# Constructing the System Prompt Template
prompt = ChatPromptTemplate.from_messages([
    ("system", "You are an advanced AI Campus Assistant for a university. "
               "You have access to specialized tools to look up statistics, records, and calculations. "
               "Always rely strictly on tool outputs to formulate your final answers. "
               "Be helpful, polite, and precise."),
    MessagesPlaceholder(variable_name="chat_history"),
    ("human", "{input}"),
    MessagesPlaceholder(variable_name="agent_scratchpad"),
])

# Creating the Agent
agent = create_tool_calling_agent(llm, tools_list, prompt)
agent_executor = AgentExecutor(agent=agent, tools=tools_list, verbose=True)


# ======== TEST CASES ========

test_queries = [
    "I attended 72 classes out of 90. Am I eligible for exams?",
    "My marks are 95, 90, 88, 91 and 87. What is my grade?",
    "My course fee is 50000 and I have paid 35000. How much fee is pending?",
    "I returned a library book 8 days late. What is the fine amount?",
    "Hostel fee is 6000 per month and I stayed for 5 months. Calculate my hostel fee.",

    "I attended 80 classes out of 100. My marks are 90, 85, 88, 92 and 95. My course fee is 60000 and I paid 45000. Provide: 1. Attendance Status, 2. Grade, and 3. Pending Fee.",
    # Bonus Challenge Query
    "Can you check the student information details for Student ID S101?"
]

if __name__ == "__main__":
    print("=" * 70)
    print("         LANGCHAIN COLLEGE ASSISTANT AGENT EXECUTION")
    print("=" * 70)
    
    for idx, query in enumerate(test_queries, start=1):
        print(f"\n\n>>> RUNNING TEST CASE #{idx}: '{query}'")
        print("-" * 70)
        
        # Execute agent query
        response = agent_executor.invoke({"input": query, "chat_history": []})
        
        print("\n[FINAL CONSOLIDATED RESPONSE]")
        print(response["output"])
        print("=" * 70)