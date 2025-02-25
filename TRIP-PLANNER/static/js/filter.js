// Toggle chip selection
document.querySelectorAll('.chip').forEach((chip) => {
    chip.addEventListener('click', () => {
        chip.classList.toggle('active');
    });
});

// Hotel quality rating
const ratingStars = document.querySelectorAll('.rating span');
ratingStars.forEach((star, index) => {
    star.addEventListener('click', () => {
        ratingStars.forEach((s, i) => {
            s.classList.toggle('inactive', i > index);
        });
    });
});

function collectTravelData(destination) {
    const days = document.getElementById('days').value;
    const startDate = document.getElementById('start-date').value;
    const startLocation = document.getElementById('start-location').value;

    const selectedLifestyles = Array.from(document.querySelectorAll('.chip.active')).map(chip => chip.textContent);
    const selectedVehicles = Array.from(document.querySelectorAll('#vehicle input[type="checkbox"]:checked')).map(checkbox => checkbox.value);

    const hotelQuality = document.querySelectorAll('#hotel-quality span:not(.inactive)').length;
    const foodInclusion = document.querySelector('input[name="food"]:checked')?.value || 'Not specified';

    return {
        days: days,
        startDate: startDate,
        startLocation: startLocation,
        lifestyles: selectedLifestyles,
        vehicles: selectedVehicles,
        hotelQuality: hotelQuality,
        foodInclusion: foodInclusion,
        destination: destination,
    };
}

// รายชื่อปลายทางและปุ่มที่เกี่ยวข้อง
const destinations = [
    { id: 'generate-suphanburi', name: 'Suphan Buri' },
    { id: 'generate-samutsongKhram', name: 'Samut SongKhram' },
    { id: 'generate-NakhonPathom', name: 'Nakhon Pathom' },
    { id: 'generate-LopBuri', name: 'Lop Buri' },
    { id: 'generate-ayutthaya', name: 'Ayutthaya' },
    { id: 'generate-all-province', name: ['Ayutthaya', 'Suphan Buri', 'Samut SongKhram', 'Nakhon Pathom', 'Lop Buri'] },
];

// ผูก Event Listener ให้กับแต่ละปุ่ม
// ผูก Event Listener ให้กับแต่ละปุ่ม
destinations.forEach(destination => {
    const button = document.querySelector(`#${destination.id}`);
    if (button) {
        button.addEventListener('click', async () => {
            const travelData = collectTravelData(destination.name);

            try {
                const response = await fetch('http://127.0.0.1:5000/api/collect-travel-data', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify(travelData),
                });

                if (response.ok) {
                    const result = await response.json();
                    console.log('Data successfully sent:', result);

                    // Redirect to the show_data page with the travel data
                    const queryParams = new URLSearchParams(travelData).toString();
                    window.location.href = `/show_plan_a?${queryParams}`;
                } else {
                    console.error('Failed to send data:', response.statusText);
                }
            } catch (error) {
                console.error('Error sending travel data:', error);
            }
        });
    } else {
        console.error(`Button with ID ${destination.id} not found.`);
    }
});



