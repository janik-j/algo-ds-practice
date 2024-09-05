import click
from .web.app import app

@click.command()
@click.option('--port', default=5000, help='Port to run the web app on')
def main(port):
    """Run the DS & Algo Learner web application."""
    click.echo(f"Starting DS & Algo Learner web app on port {port}")
    app.run(port=port)

if __name__ == '__main__':
    main()
