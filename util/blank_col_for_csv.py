import logging

import click
import click_log

import pandas as pd

logger = logging.getLogger(__name__)
click_log.basic_config(logger)


@click.command()
@click_log.simple_verbosity_option(logger)
@click.option("--csv_in", type=click.Path(exists=True), required=True)
@click.option("--csv_out", type=click.Path(), required=True)
@click.option("--col_name", required=True)
def cli(csv_in: str, csv_out: str, col_name: str):
    """
    Add a column with a constant value to a TSV file
    :param csv_in:
    :param csv_out:
    :param col_name:
    :return:
    """

    in_frame = pd.read_csv(csv_in)
    print(list(in_frame.columns))
    in_frame[col_name] = ""
    print(list(in_frame.columns))
    print(in_frame)
    in_frame.to_csv(csv_out, index=False)


if __name__ == "__main__":
    cli()
