# easyemail

A production-ready bulk cold email sender built with **FastAPI** (Python) and **Next.js**. Upload an Excel file of leads, paste or upload your email body, hit Send — easyemail does the rest over plain SMTP. No third-party email APIs. No vendor lock-in.

---

## Features

- Upload `.xlsx` or `.csv` files containing email addresses
- Paste email body directly or upload a `.docx` file
- Sends emails one-by-one via your own SMTP server
- Real-time progress updates (sent count, failures) via Server-Sent Events
- Configurable delay between sends to avoid spam filters
- Downloadable CSV log of sent / failed results after each campaign
- Stores SMTP credentials securely in `.env` — nothing hardcoded

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Next.js (React) |
| Backend | FastAPI (Python) |
| File parsing | pandas, python-docx |
| Email sending | Python smtplib (SMTP) |
| Live updates | Server-Sent Events (SSE) |

---

## Project Structure

```
easyemail/
├── backend/
│   ├── main.py              # FastAPI app entry point
│   ├── parser.py            # Excel + docx file parsing
│   ├── mailer.py            # SMTP connection and send logic
│   ├── queue.py             # Async send queue with rate limiting
│   ├── logger.py            # Result logging to CSV
│   └── .env                 # SMTP credentials (not committed)
│
├── frontend/
│   ├── pages/
│   │   └── index.tsx        # Main UI page
│   ├── components/
│   │   ├── FileUpload.tsx   # Excel file uploader
│   │   ├── EmailBody.tsx    # Body input + docx upload
│   │   └── Progress.tsx     # Live progress bar
│   └── .env.local           # Frontend env vars
│
└── README.md
```

---

## Getting Started

### Prerequisites

- Python 3.10+
- Node.js 18+
- An SMTP account (Gmail App Password, Outlook, or your own mail server)

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/easyemail.git
cd easyemail
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Create a `.env` file in the `backend/` folder:

```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=465
SMTP_USER=you@gmail.com
SMTP_PASSWORD=your_app_password
SENDER_NAME=Your Name
```

Start the FastAPI server:

```bash
uvicorn main:app --reload
```

### 3. Frontend setup

```bash
cd frontend
npm install
npm run dev
```

The app runs at `http://localhost:3000`.

---

## How to Use

1. Open the app in your browser
2. Upload your Excel file — it should have a column named `email` (or you can select the column in the UI)
3. Paste your cold email body in the text area, or upload a `.docx` file
4. Enter a subject line
5. Click **Send** and watch the real-time progress bar
6. When done, download the results log (CSV) to see which emails succeeded or failed

---

## Excel File Format

Your `.xlsx` or `.csv` file should contain at least one column with email addresses:

| name | email |
|---|---|
| John Smith | john@example.com |
| Jane Doe | jane@example.com |

The `name` column is optional but can be used for personalisation.

---

## SMTP Configuration

easyemail works with any standard SMTP provider:

| Provider | Host | Port |
|---|---|---|
| Gmail | smtp.gmail.com | 465 |
| Outlook | smtp.office365.com | 587 |
| Yahoo | smtp.mail.yahoo.com | 465 |
| Custom server | your.mail.server | 25 / 465 / 587 |

---

## Rate Limiting

By default, easyemail waits **2 seconds** between each email to reduce the chance of being flagged as spam. You can adjust this in `backend/.env`:

```env
SEND_DELAY_SECONDS=2
```

For large lists (1000+ emails), consider increasing the delay to 3–5 seconds.

---

## Roadmap

- [ ] Email personalisation using `{{name}}` placeholders
- [ ] Schedule campaigns for a specific time
- [ ] Unsubscribe link injection
- [ ] DKIM / SPF guidance in docs
- [ ] Docker Compose setup for one-command deploy

---

## Contributing

Pull requests are welcome. For major changes, open an issue first to discuss what you'd like to change.

---

## License

[MIT](LICENSE)