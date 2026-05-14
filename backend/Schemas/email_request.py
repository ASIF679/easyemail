from pydantic import BaseModel

class EmailRequest(BaseModel):
    emails      : list[str]   # list of email addresses from upload endpoint
    subject     : str         # email subject line
    body        : str         # email body (plain text or HTML)
    delay       : float = 2.0 # seconds to wait between each send
