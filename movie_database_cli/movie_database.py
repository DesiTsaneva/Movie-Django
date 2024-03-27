import click
import sqlite3

# Database initialization
conn = sqlite3.connect('movie_database.db')
cursor = conn.cursor()

# Create movies table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        description TEXT,
        release_date TEXT,
        director TEXT,
        genre TEXT,
        user_rating REAL
    )
''')
conn.commit()

# CLI commands
@click.group()
def cli():
    """CLI Movie Database Application"""

@cli.command()
def movlst():
    """List all movies"""
    cursor.execute('SELECT * FROM movies')
    movies = cursor.fetchall()
    if movies:
        click.echo("Movie Listing:")
        for movie in movies:
            click.echo(f"ID: {movie[0]}, Title: {movie[1]}, Genre: {movie[5]}")
    else:
        click.echo("No movies in the database.")

@cli.command()
@click.argument('movie_id', type=int)
def movdt(movie_id):
    """Display details of a movie"""
    cursor.execute('SELECT * FROM movies WHERE id = ?', (movie_id,))
    movie = cursor.fetchone()
    if movie:
        click.echo("Movie Details:")
        click.echo(f"Title: {movie[1]}")
        click.echo(f"Description: {movie[2]}")
        click.echo(f"Release Date: {movie[3]}")
        click.echo(f"Director: {movie[4]}")
        click.echo(f"Genre: {movie[5]}")
        click.echo(f"User Rating: {movie[6]}")
    else:
        click.echo("Movie not found.")

@cli.command()
@click.argument('query')
def movsrch(query):
    """Search movies by title"""
    cursor.execute('SELECT * FROM movies WHERE title LIKE ?', (f'%{query}%',))
    movies = cursor.fetchall()
    if movies:
        click.echo("Search Results:")
        for movie in movies:
            click.echo(f"ID: {movie[0]}, Title: {movie[1]}, Genre: {movie[5]}")
    else:
        click.echo("No movies found.")

@cli.command()
@click.argument('title')
@click.argument('description')
@click.argument('release_date')
@click.argument('director')
@click.argument('genre')
def movadd(title, description, release_date, director, genre):
    """Add a new movie"""
    cursor.execute('''
        INSERT INTO movies (title, description, release_date, director, genre, user_rating)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (title, description, release_date, director, genre, 0.0))
    conn.commit()
    click.echo("Movie added successfully.")

@cli.command()
@click.argument('movie_id', type=int)
def movfv(movie_id):
    """Mark a movie as favorite"""
    cursor.execute('UPDATE movies SET user_rating = 1.0 WHERE id = ?', (movie_id,))
    conn.commit()
    click.echo("Movie marked as favorite.")

if __name__ == '__main__':
    cli()
