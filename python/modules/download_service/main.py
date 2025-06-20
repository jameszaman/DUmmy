import os
import httpx
from tqdm import tqdm


class DownloadService:
    __content_type_to_file_format = {
        # Image formats
        "image/jpeg": "jpeg",
        "image/png": "png",
        "image/gif": "gif",
        "image/bmp": "bmp",
        "image/webp": "webp",
        "image/svg+xml": "svg",
        "image/tiff": "tiff",
        "image/heif": "heif",

        # Document formats
        "application/pdf": "pdf",
        "application/msword": "doc",
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document": "docx",
        "application/vnd.ms-excel": "xls",
        "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet": "xlsx",
        "application/vnd.ms-powerpoint": "ppt",
        "application/vnd.openxmlformats-officedocument.presentationml.presentation": "pptx",
        "application/rtf": "rtf",

        # Archive formats
        "application/zip": "zip",
        "application/x-tar": "tar",
        "application/x-rar-compressed": "rar",
        "application/x-7z-compressed": "7z",
        "application/x-gzip": "gz",

        # Text formats
        "text/plain": "txt",
        "text/html": "html",
        "text/css": "css",
        "text/javascript": "js",
        "application/javascript": "js",

        # Data formats
        "application/json": "json",
        "application/xml": "xml",
        "application/octet-stream": "bin",

        # Audio formats
        "audio/mpeg": "mp3",
        "audio/wav": "wav",
        "audio/ogg": "ogg",
        "audio/flac": "flac",

        # Video formats
        "video/mp4": "mp4",
        "video/x-msvideo": "avi",
        "video/x-matroska": "mkv",
        "video/quicktime": "mov",
        "video/x-flv": "flv",
    }

    @staticmethod
    async def download_file(url, destination_folder=None, filename=None, file_format=None, ignore_completed=True, redownload_broken=True):
        # Default to current directory if no destination folder is provided
        if destination_folder is None:
            destination_folder = os.getcwd()

        # Make sure the destination folder exists
        os.makedirs(destination_folder, exist_ok=True)

        # Determine the filename if not provided
        if filename is None:
            # Extract filename from URL
            filename = url.split("/")[-1]

        # A HEAD request to get basic information about the file.
        # This is will be used in multiple places, so we do it here.
        async with httpx.AsyncClient() as client:
            head_response = await client.head(url)

        # If format is not provided, use head request data to get the content type
        if file_format is None:
            content_type = head_response.headers.get('Content-Type', '')
            if content_type:
                # Determine file extension from content type
                file_format = content_type.split('/')[-1]
                # In case there are qs scores, remove those.
                file_format = file_format.split(";")[0]
                # If the content type is not in the dictionary, use the content type as the file format
                file_format = DownloadService.__content_type_to_file_format.get(content_type, file_format)
                # Add the file format to the filename if not already present
                if not filename.endswith(file_format):
                    filename += f'.{file_format}'
            else:
                print("Warning: Could not determine file format from content type. Using URL to determine file extension.")
                # If content type is not provided, use the URL to determine the file extension
                filename += os.path.splitext(url)[-1]

        # Full path for the file to be saved
        file_path = os.path.join(destination_folder, filename)

        # First check if the file already exists. If it exists, check the size of the file.
        # If the size does not match the size of the file and redownload_broken is True, then we will redownload the file.
        # If the size does match and ignore_completed is True, then we will skip the download.
        if os.path.exists(file_path):
            existing_file_size = os.path.getsize(file_path)
            total_size = int(head_response.headers.get('Content-Length', 0))

            if existing_file_size == total_size:
                if ignore_completed:
                    print(f"File Exists - Skipping - : {file_path}")
                    return file_path
                else:
                    print(f"File Exists - Re-downloading - : {file_path}")
            elif redownload_broken:
                print(f"File Exists - Size Mismatch - Re-downloading - : {file_path}")
            else:
                print(f"File Exists - Size Mismatch - Skipping - : {file_path}")
                return file_path

        # Stream the download and show progress
        async with httpx.AsyncClient() as client:
            # Use the correct stream method here
            async with client.stream("GET", url) as response:
                total_size = int(response.headers.get('content-length', 0))

                with open(file_path, 'wb') as file, tqdm(
                    desc=filename,
                    total=total_size,
                    unit='iB',
                    unit_scale=True,
                    unit_divisor=1024,
                ) as bar:
                    async for data in response.aiter_bytes(chunk_size=1024):
                        bar.update(len(data))
                        file.write(data)

        print(f"File downloaded: {file_path}")
