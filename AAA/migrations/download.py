def download(url = 'http://www.wikipedia.org/',
             target_filename = 'download',
             filename_extension = 'txt'):

    # Import the function for opening online documents
    from urllib.request import urlopen

    # Import an exception raised when a web server denies access
    # to a document
    from urllib.error import HTTPError

    import re

    # Open the web document for reading
    try:
        web_page = urlopen(url)
    except ValueError:
        raise Exception("Download error - Cannot find document at URL '" + url + "'")
    except HTTPError:
        raise Exception("Download error - Access denied to document at URL '" + url + "'")
    except:
        raise Exception("Download error - Something went wrong when trying to download " + \
                        "the document at URL '" + url + "'")

    # Read its contents as a Unicode string
    try:
        web_page_contents = web_page.read().decode('UTF-8')
    except UnicodeDecodeError:
        raise Exception("Download error - Unable to decode document at URL '" + \
                        url + "' as Unicode text")

    # Write the contents to a local text file as Unicode
    # characters (overwriting the file if it
    # already exists!)
    try:
        text_file = open(target_filename + '.' + filename_extension,
                         'w', encoding = 'UTF-8')
        TAG_RE = re.compile(r'<[^>]+>') 
        text_file.write(TAG_RE.sub('', web_page_contents))
        text_file.close()
    except:
        raise Exception("Download error - Unable to write to file '" + \
                        target_file + "'")

    # Return the downloaded document to the caller
    TAG_RE = re.compile(r'<[^>]+>') 
    return TAG_RE.sub('', web_page_contents)