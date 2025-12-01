"""
@author: Gabriel Decker, with lots of help from https://wiki.earthdata.nasa.gov/display/EL/How+To+Access+Data+With+Python

This program will download files from EarthData using my login. As of now, the files are put into the same folder as this script.
The URLs are obtained from a txt file from the website that will need to be in the same directory as this program
and make sure that the filenames are consistent with the links
"""

import requests
import os
from os.path import exists
from os import mkdir
from os import remove
from os.path import getsize


class DownloadingException(Exception):
    def __init__(self, message):
        super().__init__(message)
        self.message = message


class SessionWithHeaderRedirection(requests.Session):

    AUTH_HOST = 'urs.earthdata.nasa.gov'

    def __init__(self, username, password):

        super().__init__()

        self.auth = (username, password)



    # Overrides from the library to keep headers when redirected to or from

    # the NASA auth host.

    def rebuild_auth(self, prepared_request, response):

        headers = prepared_request.headers

        url = prepared_request.url



        if 'Authorization' in headers:

            original_parsed = requests.utils.urlparse(response.request.url)

            redirect_parsed = requests.utils.urlparse(url)



            if (original_parsed.hostname != redirect_parsed.hostname) and \
                    redirect_parsed.hostname != self.AUTH_HOST and \
                    original_parsed.hostname != self.AUTH_HOST:

                del headers['Authorization']



        return


def get_month_from_filename(filename):
    month_int = int(filename[31:33])
    months_list = ["January", "February", "March", "April", "May", "June", "July", "August", "September",
                   "October", "November", "December"]
    return months_list[month_int - 1]


def make_month_directory(path, month):
    new_path = path + month + "//"
    if exists(new_path):
        return
    else:
        mkdir(new_path)
        mkdir(new_path + "IDL_data_exports//")
        return


def get_URL_list(urls_filename):
    '''
    EDIT THE FOLLOWING LINE!!
    Make sure that the filename below matches the name of the file with the URLs in it, and that the file is in
    the same folder as this script
    '''
    file = open(urls_filename, 'r')

    URLs = []
    for line in file:
        line_no_whitespace = line.rstrip()
        # The README file is skipped
        if "README" in line_no_whitespace:
            continue
        URLs.append(line_no_whitespace)

    print(URLs)
    print()

    file.close()
    return URLs


def write_file(filename, save_count, path, response):
    if path != "This_dir":
        filename = path + filename

    if not exists(filename):
        with open(filename, 'wb') as fd:
            print("Writting to " + filename + " ...")
            for chunk in response.iter_content(chunk_size=1024 * 1024):
                fd.write(chunk)
            print("File #" + str(save_count + 1) + " finished")
        if getsize(filename) > 900_000_000:
            print("There is a size error")
            raise DownloadingException("This file was too big. Retry")
        if getsize(filename) < 600_000_000:
            print("There is a size error")
            raise DownloadingException("This file was too small. Retry")
    else:
        print("This file is already present!")


def connect_and_download_from_url(session, url, path, file_count):
    # This supports the new links I seem to be getting. They start with https://opendap instead of https://goldsmr5.
    # For the old one, use url[81:124]
    filename = url[96:143]
    file_month = get_month_from_filename(filename)
    make_month_directory(path, file_month)
    path += file_month + "//"
    if exists(path + filename):
        print("This file is already present!")
        return

    print("Trying to access URL #" + str(file_count + 1) + " ...")
    successfully_downloaded = False
    while not successfully_downloaded:
        try:
            response = session.get(url, stream=True)
            print(response.status_code)

            # raise an exception in case of http errors
            response.raise_for_status()

            # save the file
            write_file(filename, file_count, path, response)
            successfully_downloaded = True
        except (requests.exceptions.HTTPError, requests.exceptions.ConnectionError) as e:
            print(e)
            if exists(path + filename):
                remove(path + filename)
            print("Trying again...")
        except DownloadingException as e:
            if exists(path + filename):
                remove(path + filename)
            print(e.message)
            raise DownloadingException(e.message)
        except requests.exceptions.ChunkedEncodingError:
            if exists(path + filename):
                remove(path + filename)
            message = "There was a chunking error, trying again."
            raise DownloadingException(message)


def get_username_password():
    """
    The file containing the uname and password should be like this:
    Username: vjk;alfjek;lsajfksa
    Password: fjekafvjka;jefa

    It should be located in the same directory as this script.
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    path = os.path.join(script_dir, "EarthDataLogin.txt")
    file = open(path)
    lines = file.readlines()

    username = lines[0].split(": ")[1].strip("\n")
    password = lines[1].split(": ")[1].strip("\n")

    return username, password


def get_urls_and_download(urls_filename, path):
    URLs = get_URL_list(urls_filename)

    username, password = get_username_password()
    session = SessionWithHeaderRedirection(username, password)

    # Iterate through each URL
    for i in range(len(URLs)):

        url = URLs[i]
        '''
        EDIT THE FOLLOWING LINE!! Make sure that the filename iterating makes sense.
        The code right now adds the day to the stub that includes the year and month. For the first URL, it will add 01, making 
        20190601
        '''
        successful_download = False
        while not successful_download:
            try:
                connect_and_download_from_url(session, url, path, i)
                successful_download = True
            except DownloadingException as e:
                print (e.message)
                print("Reestablishing Connection...\n")
                session = SessionWithHeaderRedirection(username, password)
        print()
        if i % 15 == 0:
            print("Reestablishing Connection...\n")
            session = SessionWithHeaderRedirection(username, password)


def main():
    urls_filename = "subset_M2I3NVASM_5.12.4_20231227_213223_.txt"
    path_to_files = "F://MERRA-2_Data//2023//"
    # path_to_files = "This_dir"   # Use this if you want the files downloaded into this directory
    get_urls_and_download(urls_filename, path_to_files)


main()
