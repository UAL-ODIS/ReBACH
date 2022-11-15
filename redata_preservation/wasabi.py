from logging import Logger

from subprocess import run


class Wasabi:

    def __init__(self, access_key: str, secret_key, s3host,
                 s3hostbucket, log: Logger) -> None:
        """
        Initialize Wasabi class with Wasabi connection information

        :param access_key: Wasabi access key
        :param secret_key: Wasabi secret key
        :param s3host: Wasabi s3 host
        :param s3hostbucket: Template for accessing s3 bucket
        :param log: Logger object
        """
        self.s3host = s3host
        self.secret_key = secret_key
        self.access_key = access_key
        self.s3hostbucket = s3hostbucket
        self.log = log

    def list_bucket(self, folder_to_list: str) -> str:
        """
        List contents of a folder within Wasabi bucket

        :param folder_to_list: Folder within bucket to list contents of
        :return: Results of ls operation on folder_to_list
        """
        cmd = ['s3cmd', '--access_key', self.access_key, '--secret_key',
               self.secret_key, '--host', self.s3host, '--host-bucket',
               self.s3hostbucket, 'ls', folder_to_list]

        ls_result = run(cmd, capture_output=True, text=True)
        if ls_result.stderr:
            self.log.warning(f"Wasabi error: {ls_result.stderr}")

        return ls_result.stdout


def get_filenames_from_ls(ls: str) -> list[str]:
    """
    Parse ls output and return filenames

    :param ls: Output of ls command to parse
    :return: List of filenames parsed from ls
    """
    lines = ls.splitlines()
    return [line.split('/')[-1] for line in lines if line.split('/')[-1] != '']