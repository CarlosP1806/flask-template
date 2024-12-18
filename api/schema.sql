-- Create song table (with minimal attributes)
CREATE TABLE IF NOT EXISTS song (
    id INT PRIMARY KEY AUTO_INCREMENT,
    title VARCHAR(255) NOT NULL,
    artist VARCHAR(255) NOT NULL
);

-- Create playlist table (with minimal attributes)
CREATE TABLE IF NOT EXISTS playlist (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create many-to-many relationship table between songs and playlists
CREATE TABLE IF NOT EXISTS playlist_song (
    playlist_id INT,
    song_id INT,
    PRIMARY KEY (playlist_id, song_id),
    FOREIGN KEY (playlist_id) REFERENCES playlist(id) ON DELETE CASCADE,
    FOREIGN KEY (song_id) REFERENCES song(id) ON DELETE CASCADE
);