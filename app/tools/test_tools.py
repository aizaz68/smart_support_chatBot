from db.database import init_db
from app.tools.tools import (
    book_appointment,
    check_calendar_availability,
    create_support_ticket,
    send_confirmation,
    retrieve_company_knowledge
)

init_db()

# Test booking
print(book_appointment("Aizaz", "aizaz@test.com", "2026-04-10 10:00"))

# Test calendar
print(check_calendar_availability("2026-04-10"))

# Test ticket
print(create_support_ticket("My cloud migration is failing at step 3"))

# Test confirmation
print(send_confirmation({"name": "Aizaz", "datetime": "2026-04-10 10:00"}))

# Test RAG tool
docs = retrieve_company_knowledge("what services do you offer?")
print(docs[0])
