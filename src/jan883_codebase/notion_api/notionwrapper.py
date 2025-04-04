import requests
import json
import time
from typing import Dict, List, Any, Optional, Union
import pandas as pd

class NotionAPI:
    """
    A wrapper for the Notion API that simplifies common operations.

    This class provides easy-to-use methods for working with Notion databases,
    pages, and blocks, abstracting away much of the complexity of the raw API.
    """

    def __init__(self, api_key: str):
        """
        Initialize the NotionAPI wrapper with your API key.

        Args:
            api_key: Your Notion API key (Integration token)
        """
        self.api_key = api_key
        self.base_url = "https://api.notion.com/v1"
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "Notion-Version": "2022-06-28"  # Update this version as needed
        }

    def _make_request(self, method: str, endpoint: str, data: Optional[Dict] = None) -> Dict:
        """
        Make a request to the Notion API.

        Args:
            method: HTTP method (GET, POST, PATCH, DELETE)
            endpoint: API endpoint
            data: Request data (optional)

        Returns:
            Response from the API as a dictionary
        """
        url = f"{self.base_url}/{endpoint}"
        response = None

        try:
            if method == "GET":
                response = requests.get(url, headers=self.headers)
            elif method == "POST":
                response = requests.post(url, headers=self.headers, json=data)
            elif method == "PATCH":
                response = requests.patch(url, headers=self.headers, json=data)
            elif method == "DELETE":
                response = requests.delete(url, headers=self.headers)
            else:
                raise ValueError(f"Unsupported HTTP method: {method}")

            response.raise_for_status()
            return response.json()

        except requests.exceptions.HTTPError as e:
            error_message = f"HTTP Error: {e}"
            if response is not None:
                try:
                    error_details = response.json()
                    error_message += f"\nDetails: {json.dumps(error_details, indent=2)}"
                except Exception:
                    pass
            raise Exception(error_message)

        except Exception as e:
            raise Exception(f"Error making request: {str(e)}")

    # Database operations

    def create_database(self, parent_page_id: str, title: str, properties: Dict) -> Dict:
        """
        Create a new database in a parent page.

        Args:
            parent_page_id: ID of the parent page
            title: Title of the database
            properties: Database properties schema

        Returns:
            Created database object
        """
        data = {
            "parent": {"type": "page_id", "page_id": parent_page_id},
            "title": [{"type": "text", "text": {"content": title}}],
            "properties": properties
        }

        return self._make_request("POST", "databases", data)

    def query_database(self, database_id: str, filter_obj: Optional[Dict] = None,
                      sorts: Optional[List[Dict]] = None, page_size: int = 100) -> List[Dict]:
        """
        Query a database with optional filters and sorting.

        Args:
            database_id: ID of the database to query
            filter_obj: Filter object (optional)
            sorts: Sort specifications (optional)
            page_size: Number of results per page

        Returns:
            List of page objects matching the query
        """
        data: Dict[str, Any] = {"page_size": page_size}
        if filter_obj:
            data["filter"] = filter_obj
        if sorts:
            data["sorts"] = sorts

        results = []
        has_more = True
        start_cursor = None

        # Handle pagination
        while has_more:
            if start_cursor:
                data["start_cursor"] = start_cursor

            response = self._make_request("POST", f"databases/{database_id}/query", data)
            results.extend(response.get("results", []))

            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor")

            # Avoid rate limiting
            if has_more:
                time.sleep(0.3)

        return results

    def update_database(self, database_id: str, title: Optional[str] = None,
                        properties: Optional[Dict] = None) -> Dict:
        """
        Update a database's title or properties.

        Args:
            database_id: ID of the database to update
            title: New title (optional)
            properties: Updated properties schema (optional)

        Returns:
            Updated database object
        """
        data = {}

        if title:
            data["title"] = [{"type": "text", "text": {"content": title}}]

        if properties:
            data["properties"] = properties

        return self._make_request("PATCH", f"databases/{database_id}", data)

    # Page operations

    def create_page(self, parent_id: str, properties: Dict,
                   content: Optional[List[Dict]] = None, parent_type: str = "database_id") -> Dict:
        """
        Create a new page in a database or as a child of another page.

        Args:
            parent_id: ID of the parent database or page
            properties: Page properties
            content: Page content blocks (optional)
            parent_type: Type of parent ("database_id" or "page_id")

        Returns:
            Created page object
        """
        data = {
            "parent": {parent_type: parent_id},
            "properties": properties
        }

        if content:
            data["children"] = content

        return self._make_request("POST", "pages", data)

    def update_page(self, page_id: str, properties: Dict) -> Dict:
        """
        Update page properties.

        Args:
            page_id: ID of the page to update
            properties: Updated properties

        Returns:
            Updated page object
        """
        return self._make_request("PATCH", f"pages/{page_id}", {"properties": properties})

    def get_page(self, page_id: str) -> Dict:
        """
        Retrieve a page by ID.

        Args:
            page_id: ID of the page

        Returns:
            Page object
        """
        return self._make_request("GET", f"pages/{page_id}")

    # Block operations

    def get_block_children(self, block_id: str, page_size: int = 100) -> List[Dict]:
        """
        Get all children blocks of a block.

        Args:
            block_id: ID of the parent block
            page_size: Number of blocks per page

        Returns:
            List of child block objects
        """
        results = []
        has_more = True
        start_cursor = None

        # Handle pagination
        while has_more:
            endpoint = f"blocks/{block_id}/children"
            if start_cursor:
                endpoint += f"?start_cursor={start_cursor}&page_size={page_size}"
            else:
                endpoint += f"?page_size={page_size}"

            response = self._make_request("GET", endpoint)
            results.extend(response.get("results", []))

            has_more = response.get("has_more", False)
            start_cursor = response.get("next_cursor")

            # Avoid rate limiting
            if has_more:
                time.sleep(0.3)

        return results

    def append_blocks(self, block_id: str, blocks: List[Dict]) -> Dict:
        """
        Append blocks to a page or block.

        Args:
            block_id: ID of the parent block or page
            blocks: List of block objects to append

        Returns:
            Response object with list of appended blocks
        """
        return self._make_request("PATCH", f"blocks/{block_id}/children", {"children": blocks})

    def update_block(self, block_id: str, block_data: Dict) -> Dict:
        """
        Update a block's content.

        Args:
            block_id: ID of the block to update
            block_data: Updated block data

        Returns:
            Updated block object
        """
        return self._make_request("PATCH", f"blocks/{block_id}", block_data)

    def delete_block(self, block_id: str) -> Dict:
        """
        Delete a block (mark as archived).

        Args:
            block_id: ID of the block to delete

        Returns:
            Deleted block object
        """
        return self._make_request("DELETE", f"blocks/{block_id}")

    # Helper methods for creating common blocks

    def create_text_block(self, content: str, type: str = "paragraph", color: str = "default", bold: bool = False, underline: bool = False) -> Dict:
        """
        Create a text block object (paragraph, heading, etc.) with additional styling options.

        Args:
            content: Text content
            type: Block type ("paragraph", "heading_1", "heading_2", "heading_3")
            color: Text color (default "default")
            bold: Whether the text is bold (default False)
            underline: Whether the text is underlined (default False)

        Returns:
            Block object ready to use with append_blocks
        """
        return {
            "object": "block",
            "type": type,
            type: {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content
                        },
                        "annotations": {
                            "bold": bold,
                            "underline": underline,
                            "color": color
                        }
                    }
                ]
            }
        }

    def create_to_do_block(self, content: str, checked: bool = False) -> Dict:
        """
        Create a to-do block object.

        Args:
            content: Text content
            checked: Whether the to-do is checked

        Returns:
            Block object ready to use with append_blocks
        """
        return {
            "object": "block",
            "type": "to_do",
            "to_do": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }
                ],
                "checked": checked
            }
        }

    def create_bullet_list_block(self, content: str) -> Dict:
        """
        Create a bulleted list item block.

        Args:
            content: Text content

        Returns:
            Block object ready to use with append_blocks
        """
        return {
            "object": "block",
            "type": "bulleted_list_item",
            "bulleted_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }
                ]
            }
        }

    def create_numbered_list_block(self, content: str) -> Dict:
        """
        Create a numbered list item block.

        Args:
            content: Text content

        Returns:
            Block object ready to use with append_blocks
        """
        return {
            "object": "block",
            "type": "numbered_list_item",
            "numbered_list_item": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }
                ]
            }
        }

    def create_code_block(self, content: str, language: str = "python") -> Dict:
        """
        Create a code block.

        Args:
            content: Code content
            language: Programming language

        Returns:
            Block object ready to use with append_blocks
        """
        return {
            "object": "block",
            "type": "code",
            "code": {
                "rich_text": [
                    {
                        "type": "text",
                        "text": {
                            "content": content
                        }
                    }
                ],
                "language": language
            }
        }

    def create_database_schema(self) -> Dict:
        """
        Helper to create common database property schemas.

        Returns:
            Dictionary of commonly used database properties
        """
        return {
            "Title": {
                "title": {}
            },
            "Description": {
                "rich_text": {}
            },
            "Status": {
                "select": {
                    "options": [
                        {"name": "Not Started", "color": "red"},
                        {"name": "In Progress", "color": "yellow"},
                        {"name": "Complete", "color": "green"}
                    ]
                }
            },
            "Tags": {
                "multi_select": {
                    "options": [
                        {"name": "Important", "color": "red"},
                        {"name": "Urgent", "color": "yellow"},
                        {"name": "Low Priority", "color": "blue"}
                    ]
                }
            },
            "Due Date": {
                "date": {}
            },
            "Completed": {
                "checkbox": {}
            }
        }

    def database_to_dataframe(self, database_id: str, filter_obj: Optional[Dict] = None,
                             sorts: Optional[List[Dict]] = None) -> pd.DataFrame:
        """
        Convert a Notion database to a pandas DataFrame.

        This method queries all pages in a database and converts the results
        to a pandas DataFrame with columns corresponding to the database properties.

        Args:
            database_id: ID of the database to convert
            filter_obj: Filter to apply (optional)
            sorts: Sort criteria (optional)

        Returns:
            pandas DataFrame containing the database contents
        """
        # Query all pages in the database
        pages = self.query_database(database_id, filter_obj, sorts)

        # Create a list to hold the rows
        rows = []

        # Process each page
        for page in pages:
            row = {}
            page_properties = page.get("properties", {})

            # Process each property
            for property_name, property_data in page_properties.items():
                property_type = property_data.get("type")


                # Extract the value based on property type
                if property_type == "title":
                    title_items = property_data.get("title", [])
                    row[property_name] = " ".join([item.get("plain_text", "") for item in title_items]) if title_items else ""

                elif property_type == "rich_text":
                    text_items = property_data.get("rich_text", [])
                    row[property_name] = " ".join([item.get("plain_text", "") for item in text_items]) if text_items else ""

                elif property_type == "number":
                    row[property_name] = property_data.get("number")

                elif property_type == "select":
                    select_data = property_data.get("select")
                    row[property_name] = select_data.get("name") if select_data else None

                elif property_type == "multi_select":
                    select_items = property_data.get("multi_select", [])
                    row[property_name] = [item.get("name") for item in select_items] if select_items else []

                elif property_type == "date":
                    date_data = property_data.get("date")
                    if date_data:
                        start = date_data.get("start")
                        end = date_data.get("end")
                        row[property_name] = f"{start} to {end}" if end else start
                    else:
                        row[property_name] = None

                elif property_type == "checkbox":
                    row[property_name] = property_data.get("checkbox")

                elif property_type == "url":
                    row[property_name] = property_data.get("url")

                elif property_type == "email":
                    row[property_name] = property_data.get("email")

                elif property_type == "phone_number":
                    row[property_name] = property_data.get("phone_number")

                elif property_type == "formula":
                    formula_data = property_data.get("formula", {})
                    formula_type = formula_data.get("type")
                    row[property_name] = formula_data.get(formula_type)

                elif property_type == "relation":
                    relation_items = property_data.get("relation", [])
                    row[property_name] = [item.get("id") for item in relation_items] if relation_items else []

                elif property_type == "rollup":
                    rollup_data = property_data.get("rollup", {})
                    rollup_type = rollup_data.get("type")

                    if rollup_type == "array":
                        row[property_name] = rollup_data.get("array", [])
                    else:
                        row[property_name] = rollup_data.get(rollup_type)

                elif property_type == "created_time":
                    row[property_name] = property_data.get("created_time")

                elif property_type == "created_by":
                    created_by = property_data.get("created_by", {})
                    row[property_name] = created_by.get("name") if created_by else None

                elif property_type == "last_edited_time":
                    row[property_name] = property_data.get("last_edited_time")

                elif property_type == "last_edited_by":
                    last_edited_by = property_data.get("last_edited_by", {})
                    row[property_name] = last_edited_by.get("name") if last_edited_by else None

                elif property_type == "people":
                    people_items = property_data.get("people", [])
                    row[property_name] = [item.get("name") for item in people_items] if people_items else []

                elif property_type == "files":
                    file_items = property_data.get("files", [])
                    row[property_name] = [item.get("name") for item in file_items] if file_items else []

                else:
                    # Default fallback for unhandled property types
                    row[property_name] = "Unsupported property type: " + property_type

            # Add the page ID as a column
            row["Page ID"] = page.get("id")

            # Add this row to our list
            rows.append(row)

        # Create and return the DataFrame
        return pd.DataFrame(rows)

    def get_database(self, database_id: str) -> Dict:
        """
        Retrieve a database by ID.

        Args:
            database_id: The ID of the database to retrieve

        Returns:
            Dictionary containing the database information
        """
        url = f"{self.base_url}/databases/{database_id}"
        response = requests.get(
            url,
            headers=self.headers
        )
        if response.status_code == 200:
            return response.json()
        else:
            self._handle_error_response(response, f"Failed to retrieve database {database_id}")
            return {}

    def _handle_error_response(self, response, message: str) -> None:
        try:
            error_details = response.json()
            message += f" Details: {json.dumps(error_details, indent=2)}"
        except Exception:
            pass
        raise Exception(message)


    def extract_plain_text(self, notion_json):
        plain_text_list = []

        for block in notion_json:
            if block.get('type') == 'paragraph':
                rich_text = block['paragraph'].get('rich_text', [])
                for text_item in rich_text:
                    if 'plain_text' in text_item:
                        plain_text_list.append(text_item['plain_text'])

        return plain_text_list

# Example usage:


# # Initialize the API wrapper
# notion = NotionAPI("your_api_key_here")

# # Create a new database
# database_properties = notion.create_database_schema()
# database = notion.create_database(
#     parent_page_id="parent_page_id_here",
#     title="My Tasks",
#     properties=database_properties
# )

# # Add a page to the database
# new_page = notion.create_page(
#     parent_id=database["id"],
#     properties={
#         "Title": {"title": [{"text": {"content": "Complete Notion API Project"}}]},
#         "Status": {"select": {"name": "In Progress"}},
#         "Tags": {"multi_select": [{"name": "Important"}]},
#         "Due Date": {"date": {"start": "2023-12-31"}},
#         "Completed": {"checkbox": False}
#     }
# )

# # Add content to the page
# blocks = [
#     notion.create_text_block("Project details:"),
#     notion.create_bullet_list_block("Create a Notion API wrapper"),
#     notion.create_bullet_list_block("Test all functions"),
#     notion.create_bullet_list_block("Write documentation"),
#     notion.create_to_do_block("Update library dependencies", False),
#     notion.create_code_block("import notion_api\napi = notion_api.NotionAPI('key')", "python")
# ]

# notion.append_blocks(new_page["id"], blocks)

# # Query the database
# tasks = notion.query_database(
#     database["id"],
#     filter_obj={
#         "property": "Status",
#         "select": {
#             "equals": "In Progress"
#         }
#     }
# )

# # Update a page
# notion.update_page(
#     tasks[0]["id"],
#     properties={
#         "Status": {"select": {"name": "Complete"}},
#         "Completed": {"checkbox": True}
#     }
# )
