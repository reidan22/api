const popup = document.getElementById('popup');
const paths = document.querySelectorAll('path');
const OFFSET_FROM_CURSOR = 10;

document.addEventListener('mousemove', (event) => {
    // Adjust position based on scroll
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    popup.style.left = event.clientX + scrollLeft + OFFSET_FROM_CURSOR + 'px';
    popup.style.top = event.clientY + scrollTop + OFFSET_FROM_CURSOR + 'px';
});

paths.forEach(path => {
    path.addEventListener('mouseenter', (event) => {
        const title = event.target.getAttribute('title');

        popup.innerHTML = title;
        popup.style.display = 'block';
    });

    path.addEventListener('mouseleave', () => {
        popup.style.display = 'none';
    });
});


// API_PATH = "http://127.0.0.1:5000/api/ph2022/colors_by_region"
API_PATH = "https://reidan-api.vercel.app/api/ph2022/colors_by_region"
let colorByRegionDict;

let a = fetch(API_PATH)
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON from the response
    })
    .then(data => {
        // Use the data received from the API
        // console.log(data);
        console.log(data.data["region iii"])
        paths.forEach(path => {
            region = path.dataset.region
            let [r, g, b] = data.data[region]
            path.style.fill = `rgb(${r}, ${g}, ${b})`
        })
    })
    .catch(error => {
        // Handle errors here
        console.error('There was a problem with the fetch operation:', error);
    });