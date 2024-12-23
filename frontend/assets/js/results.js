const BACKEND_URL = "https://auction-website.streamlit.app/";

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const response = await fetch(`${BACKEND_URL}/api/results`);
        const resultData = await response.json();

        if (resultData.success) {
            const resultsDiv = document.getElementById('results');
            const noResultsDiv = document.getElementById('no-results');

            const results = resultData.results;

            if (results && results.length > 0) {
                resultsDiv.innerHTML = `<p>Congratulations! You have been allocated:</p>`;
                results.forEach((allocation) => {
                    const allocationDetails = `
                        <p>
                            Phone: ${allocation.phone_number}<br>
                            Quantity: ${allocation.allocated_quantity}<br>
                            Price: ${allocation.price}
                        </p>
                    `;
                    resultsDiv.innerHTML += allocationDetails;
                });
                noResultsDiv.style.display = 'none';
            } else {
                noResultsDiv.style.display = 'block';
                resultsDiv.style.display = 'none';
            }
        } else {
            alert(resultData.message || "Failed to fetch auction results.");
        }
    } catch (error) {
        console.error('Error fetching auction results:', error);
    }
});