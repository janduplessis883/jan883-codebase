import sys
import chilkat
from bs4 import BeautifulSoup
from datetime import datetime
import os

icloud_email_pass = os.environ.get("ICLOUD_EMAIL_PASSWORD")

# Local Imports
from notion_api.notionhelper import NotionHelper
from google_sheets.sheethelper import *
from llm.ollama import ask_ollama
from notion_client.errors import APIResponseError

sheethelper = SheetHelper(sheet_url='https://docs.google.com/spreadsheets/d/1k42kAuOIGDg83wP66dbZM9Zm69AdzPDNW6iKusMM6E4/edit?gid=0#gid=0')

today_string = datetime.now().isoformat()


def log_to_file_and_console(message):
    with open("log/icloud_email.log", "a") as f:
        f.write(f"{message}\n")
    sys.stdout.write(f"{message}\n")


log_to_file_and_console("Starting email chain...")


def email():
    imap = chilkat.CkImap()

    # Connect to the iCloud IMAP Mail Server
    imap.put_Ssl(True)
    imap.put_Port(993)
    success = imap.Connect("imap.mail.me.com")
    if success != True:
        log_to_file_and_console(imap.lastErrorText())
        sys.exit()

    # The username is usually the name part of your iCloud email address
    # (for example, emilyparker, not emilyparker@icloud.com).
    success = imap.Login("drjanduplessis", icloud_email_pass)
    if success != True:
        log_to_file_and_console(imap.lastErrorText())
        sys.exit()

    # Select an IMAP folder/mailbox
    success = imap.SelectMailbox("Inbox")
    if success != True:
        log_to_file_and_console(imap.lastErrorText())
        sys.exit()

    # Search for unread emails
    messageSet = imap.Search("UNSEEN", True)
    if imap.get_LastMethodSuccess() != True:
        log_to_file_and_console(imap.lastErrorText())
        sys.exit()

    numMessages = messageSet.get_Count()
    log_to_file_and_console(f"You have {numMessages} unread emails in your inbox.\n")
    numMessages = int(numMessages)

    if numMessages != 0:
        # Created new page in Notion
        nh = NotionHelper()
        database_id = "57681de3f75044dea7d21f597101ff82"
        page_properties = {
            "Name": {
                "title": [{"text": {"content": f"iCloud Email - {today_string}"}}]
            },
            "Date": {"date": {"start": today_string}},
            "Email Count": {"number": numMessages},
        }
        response = nh.new_page_to_db(
            database_id=database_id, page_properties=page_properties
        )
        page_id = response.get("id")
        log_to_file_and_console(f"New page created with ID: {page_id}")

        ollama_summaries_list = []
        for i in range(numMessages):
            msgId = messageSet.GetId(i)
            email = imap.FetchSingle(msgId, True)
            if imap.get_LastMethodSuccess() != True:
                log_to_file_and_console(imap.lastErrorText())
                sys.exit()

            log_to_file_and_console(
                "\n------------------------------------------------------"
            )
            log_to_file_and_console(str(msgId) + ": " + email.ck_from())
            log_to_file_and_console("    " + email.subject() + "\n")

            subject = email.subject()
            email_date = email.getHeaderField("Date")
            # Fetch emails and extract sender's email addresses
            email_addresses = email.ck_from()

            htmlBody = email.body()

            # Parse the HTML body using BeautifulSoup
            soup = BeautifulSoup(htmlBody, "html.parser")

            # Remove all script and style elements from the parsed HTML
            for script in soup(["script", "style"]):
                script.decompose()

            # Get the plain text content from the parsed HTML
            ptBody = soup.get_text()

            # Split ptBody into a list of words with no whitespace
            words = ptBody.split()

            # Join the words back together with no whitespace
            cleaned_ptBody = " ".join(words)
            email_body = cleaned_ptBody
            email_body = email_body[:1995]
            categories = [
                "SPAM",
                "NEWSLETTER",
                "FINANCE",
                "FRIENDS",
                "WORK",
                "CUSTOMER SERVICE - SUPPORT",
                "PROMOTION",
                "BILLS",
                "SUBSCRIPTIONS",
                "ADVERTISEMENTS",
                "CONFIRMATION",
                "IMPORTANT",
                "HEALTH",
            ]

            if ptBody:
                try:
                    log_to_file_and_console("- Plain Text Body:")
                    encoded_ptBody = cleaned_ptBody.encode("utf-8", "ignore").decode(
                        "utf-8"
                    )
                    log_to_file_and_console(encoded_ptBody)
                    log_to_file_and_console(" --------")
                    ollama_output = ask_ollama(
                        f"<email_body>{cleaned_ptBody}</email_body>\nSummarize the above email body in two sentences."
                    )
                    ollama_to_do = ask_ollama(
                        f"""[INSTR]<email_body>{cleaned_ptBody}</email_body>Task: Extract [TO-DO] list items from the provided email text, focusing on items that require action, follow-up, or information.
                        Parameters: 1. **Identify questions**: Extract any sentences or phrases that contain questions, indicating a need for clarification or additional information. 2. **Detect requests**: Find statements that explicitly request something, such as "Please", "Could you", or "I would appreciate it if". 3. **Flag follow-ups**: Highlight any mentions of scheduled meetings, calls, or tasks that require follow-up or completion.
                        4. **Exclude**: Ignore general statements, introductions, conclusions, and sentences that do not contain actionable items. If none of these conditions are met output only 'No To-Do List', only output the To-Do list itself without any explanitory text. Promotional emails and Newsletter email to-do items should only be listed if a direct questions is asked.
                        Only use plain text in your response, do not use markdown or html.[/INSTR]"""
                    )

                    log_to_file_and_console(f"🤖 {ollama_output}")
                    ollama_category = ask_ollama(
                        f"<email_body>{cleaned_ptBody}</email_body>\nClassify this email in to one of the following categories {categories}. Only return the category in upper case. Do not output any explanatory text."
                    )
                    log_to_file_and_console(f"🅾️ - {ollama_category}")
                    log_to_file_and_console(f"✅ - TO-DO list: {ollama_to_do}")
                    blocks = [
                        {
                            "object": "block",
                            "type": "heading_2",
                            "heading_2": {
                                "rich_text": [
                                    {"type": "text", "text": {"content": f"{subject}"}}
                                ]
                            },
                        },
                        {
                            "object": "block",
                            "type": "toggle",
                            "toggle": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {
                                            "content": f"{email_addresses} - {email_date}",
                                            "link": None,
                                        },
                                    }
                                ],
                                "color": "default",
                                "children": [
                                    {
                                        "type": "paragraph",
                                        "paragraph": {
                                            "rich_text": [
                                                {
                                                    "type": "text",
                                                    "text": {"content": f"{email_body}"},
                                                }
                                            ]
                                        },
                                    }
                                ],
                            },
                        },
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {"content": f"🤖 - {ollama_output}"},
                                        "annotations": {"color": "blue"},
                                    }
                                ]
                            },
                        },
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {"content": f"🅾️ - {ollama_category}"},
                                        "annotations": {
                                            "color": "red",
                                            "bold": True,
                                        },
                                    }
                                ]
                            },
                        },
                        {
                            "object": "block",
                            "type": "paragraph",
                            "paragraph": {
                                "rich_text": [
                                    {
                                        "type": "text",
                                        "text": {"content": f"✅ - {ollama_to_do}"},
                                        "annotations": {
                                            "color": "green",
                                            "bold": False,
                                        },
                                    }
                                ]
                            },
                        },
                    ]

                    nh.append_page_body(page_id, blocks=blocks)

                    # Send email to Google Sheet
                    # Clean to_do list for Google Sheet
                    cleaned_todo = ollama_to_do.split()
                    cleaned_todo = " ".join(cleaned_todo)
                    date = email_date
                    subject = subject
                    email = email_addresses
                    summary = ollama_output
                    to_do = cleaned_todo
                    body = encoded_ptBody
                    notion_page_id = page_id
                    chroma_status = 0
                    category = ollama_category

                    email_list = [date, subject, email, summary, to_do, body, category, notion_page_id, chroma_status]
                    sheethelper.append_row(email_list)
                except APIResponseError as e:
                    print(f"APIResponseError {e}")

            ollama_summaries_list.append(ollama_output)

        log_to_file_and_console(ollama_summaries_list)
        ollama_summary = ask_ollama(
            f"\n<summary_of_emails>{ollama_summaries_list}</summary_of_emails>\nSummarize this, highlighting important information."
        )
        log_to_file_and_console(
            f"\nOllama Summary of all Emails _-----------------------------"
        )
        log_to_file_and_console(f"{ollama_summary}")

        blocks = [
            {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": f"💥 Summary of Email Chain"},
                        }
                    ]
                },
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {"content": f"{ollama_summary[:1999]}"},
                            "annotations": {
                                "color": "default",
                            },
                        }
                    ]
                },
            },
        ]

        nh.append_page_body(page_id, blocks=blocks)

    else:
        log_to_file_and_console(f"❌ Inbox Empty")

    # Disconnect from the IMAP server.
    success = imap.Disconnect()

    log_to_file_and_console(
        "\n🎉 Success: https://www.notion.so/janduplessis/PyNotion-c18faada67074eb2b39f4cb41390b521?pvs=4\n"
    )


# Execute the main function.
if __name__ == "__main__":
    email()
