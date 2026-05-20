async function loadISS() {

    const response = await fetch(
        "http://localhost:8000/iss/latest"
    )

    const data = await response.json()

    document.getElementById("iss-data").innerHTML = `
        <p>Latitude: ${data.latitude}</p>
        <p>Longitude: ${data.longitude}</p>
    `
}


async function loadAPOD() {

    const response = await fetch(
        "http://localhost:8000/apod/latest"
    )

    const data = await response.json()

    document.getElementById("apod-data").innerHTML = `
        <h3>${data.title}</h3>

        <img src="${data.image_url}" />

        <p>${data.explanation}</p>
    `
}


async function loadAsteroids() {

    const response = await fetch(
        "http://localhost:8000/asteroids"
    )

    const data = await response.json()

    let html = ""

    data.slice(0, 5).forEach(asteroid => {

        html += `
            <div>
                <h3>${asteroid.name}</h3>

                <p>Diameter: ${asteroid.diameter}</p>

                <p>Velocity: ${asteroid.velocity}</p>

                <p>Hazardous: ${asteroid.hazardous}</p>

                <hr>
            </div>
        `
    })

    document.getElementById("asteroid-data").innerHTML = html
}


loadISS()

loadAPOD()

loadAsteroids()