import click


@click.group()
def cvt():
    # Name for the Covid Visualization Tool
    pass


@cvt.command()
@click.argument('data_location', '-d')
def import_data(data_location: str):
    # Import Covid Dataset
    pass
    # TODO: User would be required to enter a full path which will first be verified.
