from notion_client import Client
import pprint

class NotionHelper:
    """
    Class NotionHelper
    ------------------
    A class to assist in interfacing with the Notion API.

    Methods:
    - __init__(self): Initializes an instance of the class and invokes the authenticate method.
    - authenticate(self): Sets the `notion_token` property equal to the `ac.notion_api_key` and creates a `Client` instance with the `notion_token` property to be used for queries.
    - notion_search_db(self, database_id='e18e2d110f9e401eb1adf3190e51a21b', query=''): Queries a Notion database and returns the page title and url of the result(s) page. If there are multiple results, pprint module is used to pretty print the results.
    - notion_get_page(self, page_id): Retrieves a Notion page and returns the heading and an array of blocks on that page.
    - create_database(self, parent_page_id, database_title, properties): Creates a new database in Notion.
    - new_page_to_db(self, database_id, page_properties): Adds a new page to a Notion database.
    - append_page_body(self, page_id, blocks): Appends blocks of text to the body of a Notion page.

    Usage:
    - Instantiate a `NotionHelper` object.
    - Call the `notion_search_db` method to search for pages in a Notion database.
    - Call the `notion_get_page` method to retrieve a page and its blocks.
    - Call the `create_database` method to create a new database in Notion.
    - Call the `new_page_to_db` method to add a new page to a Notion database.
    - Call the `append_page_body` method to append blocks of text to a Notion page.
    """

    def __init__(self):
        self.authenticate()

    def authenticate(self):
        # Authentication logic for Notion
        self.notion_token = "secret_AUqFdk1kzS6qe7iw0LVlPDQXJ1TrDxnM7n9ZIB5fOlB"
        self.notion = Client(auth=self.notion_token)

    def get_database(self, database_id):
        # Fetch the database schema
        response = self.notion.databases.retrieve(database_id=database_id)
        return response

    def notion_search_db(
        self, database_id="e18e2d110f9e401eb1adf3190e51a21b", query=""
    ):
        my_pages = self.notion.databases.query(
            **{
                "database_id": database_id,
                "filter": {
                    "property": "title",
                    "rich_text": {
                        "contains": query,
                    },
                },
            }
        )

        page_title = my_pages["results"][0]["properties"][
            "Code / Notebook Description"
        ]["title"][0]["plain_text"]
        page_url = my_pages["results"][0]["url"]

        page_list = my_pages["results"]
        count = 1
        for page in page_list:
            try:
                print(
                    count,
                    page["properties"]["Code / Notebook Description"]["title"][0][
                        "plain_text"
                    ],
                )
            except IndexError:
                print("No results found.")

            print(page["url"])
            print()
            count = count + 1

        # pprint.pprint(page)

    def notion_get_page(self, page_id):
        """Returns the heading and an array of blocks on a Notion page given its page_id."""

        page = self.notion.pages.retrieve(page_id)
        blocks = self.notion.blocks.children.list(page_id)
        heading = page["properties"]["Subject"]["title"][0]["text"]["content"]
        content = [block for block in blocks["results"]]

        print(heading)
        return content

    def create_database(self, parent_page_id, database_title, properties):
        """Creates a new database in Notion."""

        # Define the properties for the database
        new_database = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [
                {
                    "type": "text",
                    "text": {
                        "content": database_title
                    }
                }
            ],
            "properties": properties
        }

        response = self.notion.databases.create(**new_database)
        return response

    def new_page_to_db(self, database_id, page_properties):
        """Adds a new page to a Notion database."""

        new_page = {
            "parent": {"database_id": database_id},
            "properties": page_properties
        }

        response = self.notion.pages.create(**new_page)
        return response

    def append_page_body(self, page_id, blocks):
        """Appends blocks of text to the body of a Notion page."""

        new_blocks = {
            "children": blocks
        }

        response = self.notion.blocks.children.append(block_id=page_id, **new_blocks)
        return response

# Usage example:
# parent_page_id = "your_parent_page_id"
# database_title = "My New Database"
# properties = {
#     "Name": {
#         "title": {}
#     },
#     "Date": {
#         "date": {}
#     },
#     "Email Count": {
#         "number": {}
#     }
# }

# notion_helper = NotionHelper()
# notion_helper.create_database(parent_page_id, database_title, properties)

# # Assuming the database was created and you have its ID
# database_id = "your_database_id"

# page_properties = {
#     "Name": {
#         "title": [
#             {
#                 "text": {
#                     "content": "Example Page"
#                 }
#             }
#         ]
#     },
#     "Date": {
#         "date": {
#             "start": "2024-08-01"
#         }
#     },
#     "Email Count": {
#         "number": 10
#     }
# }

# notion_helper.new_page_to_db(database_id, page_properties)

# # Assuming the page was created and you have its ID
# page_id = "your_page_id"

# blocks = [
#     {
#         "object": "block",
#         "type": "paragraph",
#         "paragraph": {
#             "text": [
#                 {
#                     "type": "text",
#                     "text": {
#                         "content": "This is the first paragraph of text."
#                     }
#                 }
#             ]
#         }
#     },
#     {
#         "object": "block",
#         "type": "paragraph",
#         "paragraph": {
#             "text": [
#                 {
#                     "type": "text",
#                     "text": {
#                         "content": "This is the second paragraph of text."
#                     }
#                 }
#             ]
#         }
#     }
# ]

# notion_helper.append_page_body(page_id, blocks)
