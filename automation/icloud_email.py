import sys
import chilkat
from bs4 import BeautifulSoup
from datetime import datetime
import os

icloud_email_pass = os.environ.get("ICLOUD_EMAIL_PASSWORD")

# Local Imports
from notion_api.notionhelper import NotionHelper
from llm.ollama import ask_ollama


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
                "title": [
                    {
                        "text": {
                            "content": f"iCloud Email - {today_string}"
                        }
                    }
                ]
            },
            "Date": {
                "date": {
                    "start": today_string
                }
            },
            "Email Count": {
                "number": numMessages
            }
        }
        response = nh.new_page_to_db(database_id=database_id, page_properties=page_properties)
        page_id = response.get('id')
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
                log_to_file_and_console("- Plain Text Body:")
                encoded_ptBody = cleaned_ptBody.encode("utf-8", "ignore").decode("utf-8")
                log_to_file_and_console(encoded_ptBody)
                log_to_file_and_console(" --------")
                ollama_output = ask_ollama(
                    f"<email_body>{cleaned_ptBody}</email_body>\nSummarize the above email body content in no more than 3 sentences."
                )
                log_to_file_and_console(f"🤖 {ollama_output}")
                ollama_category = ask_ollama(
                    f"<email_body>{cleaned_ptBody}</email_body>\nClassify this email in to one of the following categories {categories}. Only return the category in upper case. Do not output any explanatory text."
                )
                log_to_file_and_console(f"🅾️ - {ollama_category}")

                blocks = [
                    {
                        "object": "block",
                        "type": "heading_2",
                        "heading_2": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": f"{subject}"
                                    }
                                }
                            ]
                        }
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
                                    }
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
                                                "text": {
                                                    "content": f"{email_body}"
                                                }
                                            }
                                        ]
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": f"🤖 - {ollama_output}"
                                    },
                                    "annotations": {
                                        "color": "blue"
                                    }
                                }
                            ]
                        }
                    },
                    {
                        "object": "block",
                        "type": "paragraph",
                        "paragraph": {
                            "rich_text": [
                                {
                                    "type": "text",
                                    "text": {
                                        "content": f"🅾️ - {ollama_category}"
                                    },
                                    "annotations": {
                                        "color": "red",
                                        "bold": True,
                                    }
                                }
                            ]
                        }
                    }
                ]

                nh.append_page_body(page_id, blocks=blocks)

            ollama_summaries_list.append(ollama_output)

        log_to_file_and_console(ollama_summaries_list)
        ollama_summary = ask_ollama(
                        f"\n<summary_of_emails>{ollama_summaries_list}</summary_of_emails>\nAbove is a list of email summaries you have created. Return a bullet list (markdown format) of the key insights and information."
                    )
        log_to_file_and_console(f"\nOllama Summary of all Emails _-----------------------------")
        log_to_file_and_console(f"{ollama_summary}")

        blocks = [
                {
                "object": "block",
                "type": "heading_1",
                "heading_1": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"💥 Summary of Email Chain"
                            }
                        }
                    ]
                }
            },
            {
                "object": "block",
                "type": "paragraph",
                "paragraph": {
                    "rich_text": [
                        {
                            "type": "text",
                            "text": {
                                "content": f"{ollama_summary[:1999]}"
                            },
                            "annotations": {
                                "color": "default",
                            }
                        }
                    ]
                }
            },
        ]

        nh.append_page_body(page_id, blocks=blocks)

    else:
        log_to_file_and_console(f"❌ Inbox Empty")


    # Disconnect from the IMAP server.
    success = imap.Disconnect()

    log_to_file_and_console("\n🎉 Success: https://www.notion.so/janduplessis/PyNotion-c18faada67074eb2b39f4cb41390b521?pvs=4\n")


# Execute the main function.
if __name__ == "__main__":
    email()
