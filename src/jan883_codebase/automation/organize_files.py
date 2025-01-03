import os
import shutil


def organize_files_by_extension(directory):
    print(f"\n🅾️ - Organizing: {directory}\n")
    # List all files in the specified directory
    for filename in os.listdir(directory):
        # Construct the full file path
        file_path = os.path.join(directory, filename)

        # Check if it is a file (skip if it's a directory)
        if os.path.isfile(file_path):
            # Split the file into name and extension
            _, extension = os.path.splitext(filename)

            # Skip files without an extension
            if extension:
                # Remove the leading dot from the extension (e.g., '.jpg' -> 'jpg')
                extension = extension[1:]

                # Create a directory for the extension if it does not exist
                extension_dir = os.path.join(directory, extension)
                if not os.path.exists(extension_dir):
                    os.mkdir(extension_dir)

                # Move the file to the new directory
                shutil.move(file_path, os.path.join(extension_dir, filename))
                print(f"↪️ - Moved: {filename} -> {extension}/")


if __name__ == "__main__":
    # Specify the path to your Downloads folder
    downloads_path = "/Users/janduplessis/Downloads/"
    # Call the function to organize files by extension
    organize_files_by_extension(downloads_path)
