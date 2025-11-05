from pydantic import BaseModel

class TicketIn(BaseModel):
    ticket_text: str