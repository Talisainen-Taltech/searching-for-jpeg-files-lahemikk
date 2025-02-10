import os
import requests
import zipfile


def download_and_extract_zip(url, extract_to):
    response = requests.get(url)
    if response.status_code == 200:
        zip_path = os.path.join(extract_to, "random_files_without_extension.zip")
        with open(zip_path, "wb") as f:
            f.write(response.content)

        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)

        print("Files downloaded and extracted successfully.")
        os.remove(zip_path)
    else:
        print(f"Failed to download the file. Status code: {response.status_code}")


def process_files(folder_path):
    jpeg_signature = b"\xFF\xD8"

    for file_name in os.listdir(folder_path):
        file_path = os.path.join(folder_path, file_name)

        if os.path.isfile(file_path):
            with open(file_path, "rb") as f:
                file_header = f.read(2)

            if file_header == jpeg_signature:
                new_file_path = f"{file_path}.jpeg"
                os.rename(file_path, new_file_path)
                print(f"Renamed: {file_name} -> {os.path.basename(new_file_path)}")
            else:
                os.remove(file_path)
                print(f"Deleted: {file_name}")
        else:
            print(f"Skipped: {file_name} (not a file)")


def main():
    url = "https://upload.itcollege.ee/~aleksei/random_files_without_extension.zip"
    extract_to = "random_files"

    os.makedirs(extract_to, exist_ok=True)

    download_and_extract_zip(url, extract_to)

    extracted_items = os.listdir(extract_to)
    if len(extracted_items) == 1 and os.path.isdir(os.path.join(extract_to, extracted_items[0])):
        extract_to = os.path.join(extract_to, extracted_items[0])

    process_files(extract_to)


if __name__ == "__main__":
    main()
