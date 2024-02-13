const popup = document.getElementById('popup');
const sidebar = document.getElementById('sidebar');
const paths = document.querySelectorAll('path');
const OFFSET_FROM_CURSOR = 10;

function openSidebar() {
    document.querySelector('.sidebar').style.left = '0';
    document.querySelector('.main-content').style.marginLeft = '500px';
}

function closeSidebar() {
    document.querySelector('.sidebar').style.left = '-500px';
    document.querySelector('.main-content').style.marginLeft = '0';
}



document.addEventListener('mousemove', (event) => {
    // Adjust position based on scroll
    const scrollLeft = window.pageXOffset || document.documentElement.scrollLeft;
    const scrollTop = window.pageYOffset || document.documentElement.scrollTop;

    popup.style.left = event.clientX + scrollLeft + OFFSET_FROM_CURSOR + 'px';
    popup.style.top = event.clientY + scrollTop + OFFSET_FROM_CURSOR + 'px';
});

paths.forEach(path => {
    path.addEventListener('mouseenter', (event) => {
        const title = event.target.getAttribute('title') + " " + event.target.dataset.region.toUpperCase();

        popup.innerHTML = title;
        popup.style.display = 'block';
    });

    path.addEventListener('mouseleave', () => {
        popup.style.display = 'none';
    });
});



// API_BASE_PATH = "http://127.0.0.1:5000/"
API_BASE_PATH = "https://reidan-api.vercel.app/"

let colorByRegionDict;

let a = fetch(API_BASE_PATH + "api/ph2022/colors_by_region")
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON from the response
    })
    .then(data => {
        // Use the data received from the API
        paths.forEach(path => {
            region = path.dataset.region
            // let [r, g, b] = data.data[region]
            let [r, g, b] = data.data["region iii"]
            path.style.fill = `rgb(${r}, ${g}, ${b})`
        })
    })
    .catch(error => {
        // Handle errors here
        console.error('There was a problem with the fetch operation:', error);
    });


function findCandidate() {
    let first_name = document.getElementById('first_name').value;
    let last_name = document.getElementById('last_name').value;

    api_search = "api/ph2022/candidate?"

    if (first_name && last_name) {
        api_search = api_search + `first_name=${first_name}&last_name=${last_name}`
    } else if (first_name) {
        api_search = api_search + `first_name=${first_name}`
    } else if (last_name) {
        api_search = api_search + `last_name=${last_name}`
    } else {
        api_search = ""
    }

    if (api_search) {
        fetch(API_BASE_PATH + api_search)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json(); // Parse the JSON from the response
            })
            .then(data => {
                let firstReturnedCandidate = Object.values(data.data)[0]; // "plain value"
                let full_name = firstReturnedCandidate.first_name + " " + firstReturnedCandidate.last_name
                let position = firstReturnedCandidate.position
                let party = firstReturnedCandidate.party
                let region_percents = firstReturnedCandidate.region_percents
                let candidate_total_votes = firstReturnedCandidate.total_votes
                let region_votes = firstReturnedCandidate.regions

                
                fetch(API_BASE_PATH + "api/ph2022/colors_by_candidate")
                    .then(response => {
                        if (!response.ok) {
                            throw new Error('Network response was not ok');
                        }
                        return response.json(); // Parse the JSON from the response
                    })
                    .then(data => {
                        // Use the data received from the API
                        paths.forEach(path => {
                            let region = path.dataset.region
                            let region_percent = region_percents[region]
                            let region_vote = region_votes[region]
                            let per_cand_region_percent = region_vote / candidate_total_votes
                            console.log(region_vote, candidate_total_votes, per_cand_region_percent)
                            let [r, g, b] = data.data[full_name]
                            
                            var radioButton1 = document.getElementById("percent_1");
                            var radioButton2 = document.getElementById("percent_2");
                            if (radioButton1.checked){
                                percent = region_percent
                            }
                            else if (radioButton2.checked){
                                percent = per_cand_region_percent}
                            else{
                                radioButton2.checked = true
                                percent = per_cand_region_percent
                            }

                            path.style.fill = `rgba(${r}, ${g}, ${b}, ${percent * 10})`
                            // path.style.fill = `rgba(${r}, ${g}, ${b}, ${region_percent * 10})`
                            path.addEventListener('mouseenter', (event) => {
                                const title = event.target.getAttribute('title') + " " + event.target.dataset.region.toUpperCase();
                                popup.innerHTML = title +"<br />"+ full_name.toUpperCase() + "<br />"+ position.toUpperCase() + "<br />"+ party.toUpperCase() + "<br/>" + region_vote+ ` (${region_percent *100}%)`;
                                popup.style.display = 'block';
                            });
                        
                            path.addEventListener('mouseleave', () => {
                                popup.style.display = 'none';
                            });
                        });
                    })
                    .catch(error => {
                        // Handle errors here
                        console.error('There was a problem with the fetch operation:', error);
                    });


            })
            .catch(error => {
                // Handle errors here
                console.error('There was a problem with the fetch operation:', error);
            });
    }
first_name = ""
last_name = ""
}

var positionsContainer = document.getElementById("positions-container");
fetch(API_BASE_PATH + "api/ph2022/position")
    .then(response => {
        if (!response.ok) {
            throw new Error('Network response was not ok');
        }
        return response.json(); // Parse the JSON from the response
    })
    .then(data => {
        // Use the data received from the API
        let positions = data.data
        for (var position in positions) {
            if (positions.hasOwnProperty(position)) {
            // Create a div element
            var divPositions = document.createElement("div");
            divPositions.id = `position-${position}`
            divPositions.classList.add("centrify")
            divPositions.classList.add("position")
            // divPositions.onclick = togglePositions(position)
            // Set div content
            // divPositions.innerHTML = position.toUpperCase();
            pos = position.replace(" ","_")
            divPositions.innerHTML = `<span onclick=togglePositions("${pos}")> ${position.toUpperCase()}</span>`
            // Append the div to the container
            positionsContainer.appendChild(divPositions);
            // var candidatesContainer = document.getElementById(`position-${position}`)
            var candidates = positions[position];
                for (var candidate in candidates){
                    if (candidates.hasOwnProperty(candidate)){
                        console.log("POSITION: " + position + ", CANDIDATE: " + candidate);
                        var divCandidates = document.createElement("div");
                        divCandidates.id = `candidate-${candidate}`
                        divCandidates.classList.add("centrify")
                        divCandidates.classList.add("candidate")
                        divCandidates.classList.add("hidden")
                        divCandidates.classList.add(position.replace(" ","_"))

                        var radioButton = document.createElement("input");

                        // Set attributes for the radio button
                        radioButton.setAttribute("type", "radio");
                        radioButton.setAttribute("name", candidate);
                        radioButton.setAttribute("value", candidate);
                        radioButton.setAttribute("id", candidate);
                        cand = candidate.split(" ")[0]
                        divCandidates.innerHTML = `<span onclick=searchCandidate("${cand}")>${candidate.toUpperCase()}</span>`;
                        positionsContainer.appendChild(divCandidates);

                    }
                }
            }
        }
        // positions.forEach(function(item) {
        //     // Create a div element
        //     var div = document.createElement("div");
            
        //     // Set div content
        //     div.innerHTML = "<h3>" + item + "</h3><p>" + "DESC" + "</p>";
            
        //     // Append the div to the container
        //     positionsContainer.appendChild(div);
        // });
    })
    .catch(error => {
        // Handle errors here
        console.error('There was a problem with the fetch operation:', error);
    });


function searchCandidate(candidate){
    document.getElementById('first_name').value = candidate;
    findCandidate()
}

function togglePositions(position){
    var elements = document.querySelectorAll(`.${position}`);
    elements.forEach(function(element) {
        element.classList.toggle("hidden");
      });

}