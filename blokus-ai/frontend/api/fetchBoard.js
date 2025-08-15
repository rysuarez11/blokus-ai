export const fetchBoard = async () => {
    try {
        const response = await fetch("http://127.0.0.1:5000/get_board");
        if (!response.ok) {
            throw new Error(`Failed to fetch board: ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error("Error fetching board:", error);
        throw error;
    }
};
