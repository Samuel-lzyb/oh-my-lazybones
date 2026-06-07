import typer
app = typer.Typer(name="lazy", help="oh-my-lazybones CLI")

@app.command()
def search(query: str):
    """搜索技能"""
    typer.echo(f"Searching for: {query}")

if __name__ == "__main__":
    app()