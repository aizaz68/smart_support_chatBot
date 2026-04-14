from db.database import get_connection
from app.rag.retriever import retrieve_relevant_docs

def retrieve_company_knowledge(query: str) -> list:
    return retrieve_relevant_docs(query)

def check_calendar_availability(date_range: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT datetime FROM appointments WHERE datetime LIKE ?", (f"%{date_range}%",))
    booked = [row["datetime"] for row in cursor.fetchall()]
    conn.close()
    return {"date_range": date_range, "booked_slots": booked}

def book_appointment(name: str, email: str, datetime: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO appointments (name, email, datetime) VALUES (?, ?, ?)",
        (name, email, datetime)
    )
    conn.commit()
    appointment_id = cursor.lastrowid
    conn.close()
    return {"status": "booked", "id": appointment_id, "name": name, "email": email, "datetime": datetime}

def create_support_ticket(issue: str) -> dict:
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO support_tickets (issue) VALUES (?)", (issue,))
    conn.commit()
    ticket_id = cursor.lastrowid
    conn.close()
    return {"status": "created", "ticket_id": ticket_id, "issue": issue}

def send_confirmation(details: dict) -> dict:
    print(f"Confirmation sent: {details}")
    return {"status": "sent", "details": details}


def log_conversation(session_id: str, user_input:str, intent:str, response:str, escalated:bool)-> dict:
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute(
        "INSERT INTO conversation_logs (session_id, user_input, intent, response, escalated) Values (?,?,?,?,?)",
        (session_id,user_input,intent,response,int(escalated))
    )
    conn.commit()
    conn.close()
    return {"status": "logged"
    }