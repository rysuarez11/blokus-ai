const API_BASE_URL = "http://127.0.0.1:5000";

export const fetchPieces = async () => {
    try {
        const response = await fetch("http://127.0.0.1:5000/get_pieces");
        if (!response.ok) {
            throw new Error(`Failed to fetch pieces: ${response.statusText}`);
        }
        const data = await response.json();

        // Include static mapping for player images
        const playerImages = [
            "/static/player_1.png", // Player 1 image
            "/static/player_2.png", // Player 2 image
            "/static/player_3.png", // Player 3 image
            "/static/player_4.png", // Player 4 image
        ];

        return { pieces: data.pieces, playerImages }; // Return both pieces and player images
    } catch (error) {
        console.error("Error fetching pieces:", error);
        throw error;
    }
};


// Fetch player colors
export const fetchPlayerColors = async () => {
    try {
        const response = await fetch(`${API_BASE_URL}/get_player_colors`);
        if (!response.ok) {
            throw new Error(`Failed to fetch player colors: ${response.statusText}`);
        }
        const data = await response.json();
        return data.colors;
    } catch (error) {
        console.error("Error fetching player colors:", error);
        throw error;
    }
};
