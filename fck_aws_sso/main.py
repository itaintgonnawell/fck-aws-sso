from typing import Optional
from fck_aws_sso.authorize_sso import authorize_sso
from fck_aws_sso.io import read_stdin_until_data_is_extracted
import typer
import logging
from pathlib import Path

app = typer.Typer()


@app.command()
def main(
    headless: bool = True,
    verbose: bool = False,
    user_data_dir: Optional[Path] = None,
):
    """
    A tool to automate AWS SSO login.
    Example: aws sso login --no-browser | fck-aws-sso
    """
    if verbose:
        logging.basicConfig(level=logging.DEBUG)
    extracted_url, extracted_code = read_stdin_until_data_is_extracted()
    authorize_sso(extracted_url, extracted_code, headless, user_data_dir)


if __name__ == "__main__":
    app()
