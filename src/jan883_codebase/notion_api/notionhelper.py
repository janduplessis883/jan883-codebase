import notion_client
from notion_client import Client
import pprint
import pandas as pd
import os

# NotionHelper can be used in conjunction with the Streamlit APP: (Notion API JSON)[https://notioinapiassistant.streamlit.app]

class NotionHelper:
    '''
    A helper class to interact with the Notion API.

    Methods
    -------
    __init__():
        Initializes the NotionHelper instance and authenticates with the Notion API.

    authenticate():
        Authenticates with the Notion API using a token from environment variables.

    get_database(database_id):
        Fetches the schema of a Notion database given its database_id.

    notion_search_db(database_id, query=""):
        Searches for pages in a Notion database that contain the specified query in their title.

    notion_get_page(page_id):
        Returns the JSON of the page properties and an array of blocks on a Notion page given its page_id.

    create_database(parent_page_id, database_title, properties):
        Creates a new database in Notion under the specified parent page with the given title and properties.

    new_page_to_db(database_id, page_properties):
        Adds a new page to a Notion database with the specified properties.

    append_page_body(page_id, blocks):
        Appends blocks of text to the body of a Notion page.

    get_all_page_ids(database_id):
        Returns the IDs of all pages in a given Notion database.

    get_all_pages_as_json(database_id, limit=None):
        Returns a list of JSON objects representing all pages in the given database, with all properties.

    get_all_pages_as_dataframe(database_id, limit=None):
        Returns a Pandas DataFrame representing all pages in the given database, with selected properties.
    '''

    def __init__(self):
        self.authenticate()

    def authenticate(self):
        # Authentication logic for Notion
        self.notion_token = os.getenv("NOTION_TOKEN")
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
        """Returns the JSON of the page properties and an array of blocks on a Notion page given its page_id."""

        # Retrieve the page and block data
        page = self.notion.pages.retrieve(page_id)
        blocks = self.notion.blocks.children.list(page_id)

        # Extract all properties as a JSON object
        properties = page.get("properties", {})
        content = [block for block in blocks["results"]]

        # Print the full JSON of the properties
        print(properties)

        # Return the properties JSON and blocks content
        return {"properties": properties, "content": content}

    def create_database(self, parent_page_id, database_title, properties):
        """Creates a new database in Notion."""

        # Define the properties for the database
        new_database = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": database_title}}],
            "properties": properties,
        }

        response = self.notion.databases.create(**new_database)
        return response

    def new_page_to_db(self, database_id, page_properties):
        """Adds a new page to a Notion database."""

        new_page = {
            "parent": {"database_id": database_id},
            "properties": page_properties,
        }

        response = self.notion.pages.create(**new_page)
        return response

    def append_page_body(self, page_id, blocks):
        """Appends blocks of text to the body of a Notion page."""

        new_blocks = {"children": blocks}

        response = self.notion.blocks.children.append(block_id=page_id, **new_blocks)
        return response

    def get_all_page_ids(self, database_id):
        """Returns the IDs of all pages in a given database."""

        my_pages = self.notion.databases.query(database_id=database_id)
        page_ids = [page["id"] for page in my_pages["results"]]
        return page_ids

    def get_all_pages_as_json(self, database_id, limit=None):
        """Returns a list of JSON objects representing all pages in the given database, with all properties.
        You can specify the number of entries to be loaded using the `limit` parameter.
        """

        # Use pagination to remove any limits on number of entries, optionally limited by `limit` argument
        pages_json = []
        has_more = True
        start_cursor = None
        count = 0

        while has_more:
            my_pages = self.notion.databases.query(
                **{
                    "database_id": database_id,
                    "start_cursor": start_cursor,
                }
            )
            pages_json.extend([page["properties"] for page in my_pages["results"]])
            has_more = my_pages.get("has_more", False)
            start_cursor = my_pages.get("next_cursor", None)
            count += len(my_pages["results"])

            if limit is not None and count >= limit:
                pages_json = pages_json[:limit]
                break

        return pages_json

    def get_all_pages_as_dataframe(self, database_id, limit=None):
        """Returns a Pandas DataFrame representing all pages in the given database, with selected properties.
        You can specify the number of entries to be loaded using the `limit` parameter.
        """

        pages_json = self.get_all_pages_as_json(database_id, limit=limit)
        data = []

        # Define the list of allowed property types that we want to extract
        allowed_properties = [
            "title",
            "status",
            "number",
            "date",
            "url",
            "checkbox",
            "rich_text",
            "email",
            "select",
            "people",
            "phone_number",
            "multi_select",
            "created_time",
            "created_by",
            "rollup",
            "relation",
            "last_edited_by",
            "last_edited_time",
            "formula",
            "file",
        ]

        for page in pages_json:
            row = {}
            for key, value in page.items():
                property_type = value.get("type", "")

                if property_type in allowed_properties:
                    if property_type == "title":
                        row[key] = value.get("title", [{}])[0].get("plain_text", "")
                    elif property_type == "status":
                        row[key] = value.get("status", {}).get("name", "")
                    elif property_type == "number":
                        # Ensure number properties are explicitly cast to float
                        number_value = value.get("number", None)
                        row[key] = (
                            float(number_value)
                            if isinstance(number_value, (int, float))
                            else None
                        )
                    elif property_type == "date":
                        date_field = value.get("date", {})
                        row[key] = date_field.get("start", "") if date_field else ""
                    elif property_type == "url":
                        row[key] = value.get("url", "")
                    elif property_type == "checkbox":
                        row[key] = value.get("checkbox", False)
                    elif property_type == "rich_text":
                        rich_text_field = value.get("rich_text", [])
                        row[key] = (
                            rich_text_field[0].get("plain_text", "")
                            if rich_text_field
                            else ""
                        )
                    elif property_type == "email":
                        row[key] = value.get("email", "")
                    elif property_type == "select":
                        select_field = value.get("select", {})
                        row[key] = select_field.get("name", "") if select_field else ""
                    elif property_type == "people":
                        people_list = value.get("people", [])
                        if people_list:
                            person = people_list[0]
                            row[key] = {
                                "name": person.get("name", ""),
                                "email": person.get("person", {}).get("email", ""),
                            }
                    elif property_type == "phone_number":
                        row[key] = value.get("phone_number", "")
                    elif property_type == "multi_select":
                        multi_select_field = value.get("multi_select", [])
                        row[key] = [item.get("name", "") for item in multi_select_field]
                    elif property_type == "created_time":
                        row[key] = value.get("created_time", "")
                    elif property_type == "created_by":
                        created_by = value.get("created_by", {})
                        row[key] = created_by.get("name", "")
                    elif property_type == "rollup":
                        rollup_field = value.get("rollup", {}).get("array", [])
                        row[key] = [
                            item.get("date", {}).get("start", "")
                            for item in rollup_field
                        ]
                    elif property_type == "relation":
                        relation_list = value.get("relation", [])
                        row[key] = [
                            relation.get("id", "") for relation in relation_list
                        ]
                    elif property_type == "last_edited_by":
                        last_edited_by = value.get("last_edited_by", {})
                        row[key] = last_edited_by.get("name", "")
                    elif property_type == "last_edited_time":
                        row[key] = value.get("last_edited_time", "")
                    elif property_type == "formula":
                        formula_value = value.get("formula", {})
                        row[key] = formula_value.get(formula_value.get("type", ""), "")
                    elif property_type == "file":
                        files = value.get("files", [])
                        row[key] = [file.get("name", "") for file in files]

            data.append(row)

        df = pd.DataFrame(data)
        # Prevent numbers from displaying in scientific notation
        pd.options.display.float_format = "{:.3f}".format
        return df
