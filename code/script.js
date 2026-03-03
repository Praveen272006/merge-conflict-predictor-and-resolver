const API_KEY = 'YOU    dhsf R_OPENWEATHERMAP_API_KEY'; // Get free at openweathermap.org
const API_URL = 'https://api.openweathermap.org/data/2.5/weather';
const FORECAST_URL = 'https://api.openweathermap.org/data/2.5/forecast';

document.addEventListener('DOMContentLoaded', () => {
    const cityInput = document.getElementById('cityInput');
    const searchBtn = document.getElementById('searchBtn');
    const darkToggle = document.getElementById('darkToggle');
    const currentWeather = document.getElementById('currentWeather');
    const forecast = document.getElementById('forecast');

    darkToggle.addEventListener('click', () => {
        document.body.classList.toggle('dark');
        darkToggle.querySelector('i').classList.toggle('fa-moon');
        darkToggle.querySelector('i').classList.toggle('fa-sun');
    });

    searchBtn.addEventListener('click', getWeather);
    cityInput.addEventListener('keypress', (e) => { if (e.key === 'Enter') getWeather(); });

    async function getWeather() {
        const city = cityInput.value.trim();
        if (!city) return alert('Enter a city!');
        try {
            const res = await fetch(`${API_URL}?q=${city}&appid=${API_KEY}&units=metric`);
            const data = await res.json();
            if (data.cod !== 200) throw new Error(data.message);
            displayCurrent(data);
            getForecast(city);
        } catch (err) {
            alert('City not found!');
        }
    }

    function displayCurrent(data) {
        document.getElementById('cityName').textContent = data.name;
        document.getElementById('dateTime').textContent = new Date().toLocaleString();
        document.getElementById('temperature').textContent = `${Math.round(data.main.temp)}°C`;
        document.getElementById('description').textContent = data.weather[0].description;
        document.getElementById('humidity').innerHTML = `<i class="fas fa-tint"></i> ${data.main.humidity}%`;
        document.getElementById('windSpeed').innerHTML = `<i class="fas fa-wind"></i> ${data.wind.speed} m/s`;
        document.getElementById('visibility').innerHTML = `<i class="fas fa-eye"></i> ${data.visibility / 1000} km`;
        document.getElementById('weatherIcon').src = `https://openweathermap.org/img/wn/${data.weather[0].icon}@2x.png`;
        currentWeather.classList.remove('hidden');
        updateGauges(data.main.temp, data.main.humidity);
    }

    async function getForecast(city) {
        const res = await fetch(`${FORECAST_URL}?q=${city}&appid=${API_KEY}&units=metric`);
        const data = await res.json();
        const hourly = data.list.slice(0, 8);
        const list = document.getElementById('hourlyList');
        list.innerHTML = '';
        hourly.forEach(item => {
            const div = document.createElement('div');
            div.className = 'hourly-item';
            div.innerHTML = `
                <p>${new Date(item.dt * 1000).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}</p>
                <img src="<https://openweathermap.org/img/wn/${item.weather>[0].icon}.png">
                <p>${Math.round(item.main.temp)}°C</p>
            `;
            list.appendChild(div);
        });
        forecast.classList.remove('hidden');
    }

    function updateGauges(temp, humid) {
        const tempCtx = document.getElementById('tempGauge').getContext('2d');
        const humidCtx = document.getElementById('humidGauge').getContext('2d');
        drawGauge(tempCtx, temp / 50 * 180 + 90, temp);
        drawGauge(humidCtx, humid / 100 * 180 + 90, humid);
    }

    function drawGauge(ctx, angle, value) {
        ctx.clearRect(0, 0, 200, 200);
        ctx.beginPath();
        ctx.arc(100, 100, 80, Math.PI / 180 * 90, Math.PI / 180 * 270);
        ctx.strokeStyle = '#e0e0e0';
        ctx.lineWidth = 20;
        ctx.stroke();
        ctx.beginPath();
        ctx.arc(100, 100, 80, Math.PI / 180 * 90, Math.PI / 180 * angle);
        ctx.strokeStyle = '#4a90e2';
        ctx.stroke();
        ctx.fillStyle = '#333';
        ctx.font = 'bold 24px Arial';
        ctx.textAlign = 'center';
        ctx.fillText(`${value}`, 100, 115);
        ctx.font = '16px Arial';
        ctx.fillText(value > 30 ? '°C' : '%', 100, 140);
    }
});
