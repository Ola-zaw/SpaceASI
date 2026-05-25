const API = "http://localhost:8000";



const savedZoom =

localStorage.getItem(
"mapZoom"
)



const savedCenter =

JSON.parse(

localStorage.getItem(
"mapCenter"
)

||

"[0,0]"

)



let map =

L.map(

"iss-map",

{

zoomSnap:0,

maxZoom:8,

maxBounds:[
[-90,-180],
[90,180]
],

maxBoundsViscosity:1

}

)

.setView(

savedCenter,

savedZoom

?

Number(
savedZoom
)

:

2

)



if(
!savedZoom
){

map.fitBounds(

[

[0,-180],

[0,180]

]

)

}



map.setMinZoom(
map.getZoom()
)



L.tileLayer(

"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",

{

noWrap:true,

bounds:[
[-90,-180],
[90,180]
]

}

)

.addTo(
map
)



map.on(

"moveend",

()=>{

localStorage.setItem(

"mapZoom",

map.getZoom()

)


localStorage.setItem(

"mapCenter",

JSON.stringify(

[

map.getCenter().lat,

map.getCenter().lng

]

)

)

}

)



let marker =

L.marker(
[0,0]
)

.addTo(
map
)



let line =

L.polyline(

[],

{

color:"cyan",

weight:3,

smoothFactor:1

}

)

.addTo(
map
)


let pathSegments = [ [] ]; 

function trimHistory() {
    let totalPoints = pathSegments.reduce((sum, seg) => sum + seg.length, 0);
    if (totalPoints > 500) {
        pathSegments[0].shift(); 
        if (pathSegments[0].length === 0) {
            pathSegments.shift();
        }
    }
}

// async function loadHistory(){

// const response=

// await fetch(
// `${API}/iss/history`
// )

// const data=

// await response.json()

// if(
// !data.length
// ){

// return

// }

// pathSegments=[[]]


// pathSegments[0]=

// data.map(
// p=>
// [
// p.latitude,
// p.longitude
// ]
// )

// line.setLatLngs(
// pathSegments
// )

// marker.setLatLng(

// pathSegments[0][
// pathSegments[0].length-1
// ]

// )

// }

async function loadHistory(){

const response =

await fetch(
`${API}/iss/history`
)

const data =

await response.json()


if(
!data.length
){

return

}


let start = 0


for(

let i=data.length-1;

i>0;

i--

){

const curr =

new Date(
data[i].created_at
)


const prev =

new Date(
data[i-1].created_at
)


const diff =

(

curr

-

prev

)

/

1000


if(

diff

>

90

){

start=i

break

}

}


const history =

data.slice(
start
)


pathSegments=[[]]


pathSegments[0]=

history.map(

p=>

[

p.latitude,

p.longitude

]

)


line.setLatLngs(
pathSegments
)


marker.setLatLng(

pathSegments[0][

pathSegments[0].length-1

]

)

}

async function loadISS() {
    const response = await fetch(`${API}/iss/latest`);
    const data = await response.json();

    const newPoint = [data.latitude, data.longitude];
    let currentSegment = pathSegments[pathSegments.length - 1];

    if (currentSegment.length > 0) {
        let lastPoint = currentSegment[currentSegment.length - 1];
        
        if (Math.abs(newPoint[1] - lastPoint[1]) > 180) {
            pathSegments.push([]); 
            currentSegment = pathSegments[pathSegments.length - 1];
        }
    }

    currentSegment.push(newPoint);
    trimHistory();

    line.setLatLngs(pathSegments);
    marker.setLatLng(newPoint);

    document.getElementById("iss-coords").innerHTML = `
        Latitude: ${data.latitude.toFixed(4)} | Longitude: ${data.longitude.toFixed(4)}
    `;
}

async function loadAPOD() {

    const response =
        await fetch(
            `${API}/apod/latest`
        );

    const data =
        await response.json();


    let media;


    if (

        data.image_url.endsWith(".mp4")

        ||

        data.image_url.includes("youtube")

    ) {

        media = `

            <video
                class="apod-img"
                controls>

                <source
                    src="${data.image_url}">

            </video>

        `;

    }

    else {

        media = `

            <img
                class="apod-img"
                src="${data.image_url}"
                alt="${data.title}">

        `;

    }


    document
        .getElementById(
            "apod-container"
        )
        .innerHTML = `

            <h4 class="apod-title">

                ${data.title}

            </h4>

            ${media}

            <div class="apod-description">

                ${data.explanation}

            </div>

        `;

}

async function loadAsteroids() {

    const statsResponse =
    await fetch(
        `${API}/asteroids/stats`
    )

    const stats =
    await statsResponse.json()


    const response =
    await fetch(
        `${API}/asteroids`
    )

    const data =
    await response.json()



    document
    .getElementById(
        "stats"
    )
    .innerHTML =

    `

    Total:
    ${stats.total}

    |

    Dangerous:
    ${stats.hazardous}

    |

    ${stats.start_date}

    →

    ${stats.end_date}

    `

    const unique =

    Array.from(

    new Map(

    data.map(

    a=>

    [

    a.key,

    a

    ]

    )

    )

    .values()

    )



    const closest =

    unique

    .sort(

    (

    a,

    b

    )=>

    new Date(
    a.date
    )

    -

    new Date(
    b.date
    )

    )

    .slice(
    0,
    10
    )



    let rows = ""



    closest.forEach(

        a => {

            rows += `

            <tr>

                <td>

                    ${a.name}

                </td>

                <td>

                    ${a.diameter}m

                </td>

                <td>

                    ${a.miss_distance.toLocaleString()}km

                </td>

                <td>

                    ${a.velocity.toLocaleString()}km/h

                </td>

                <td>

                    ${a.date}

                </td>

                <td

                class="${
                    a.hazardous
                    ?
                    "hazard"
                    :
                    "safe"
                }"

                >

                ${
                    a.hazardous
                    ?
                    "YES"
                    :
                    "NO"
                }

                </td>

            </tr>

            `

        }

    )



    document
    .getElementById(
        "asteroids-table-body"
    )
    .innerHTML =
    rows



    createVelocityChart(
        closest
    )


    createDistanceChart(
        closest
    )

}


function createVelocityChart(data){

new Chart(

document.getElementById(
"asteroidsChart"
),

{

type:"bar",

data:{

labels:
data.map(
x=>
x.name
),

datasets:[{

label:
"Velocity (km/h)",

data:
data.map(
x=>
x.velocity
),

backgroundColor:

data.map(
x=>

x.hazardous

?

"#ff4444"

:

"#66ccff"

)

}]

},

options:{

maintainAspectRatio:false,

plugins:{

legend:{

labels:{

color:"#b0b0b0"

}

}

},

scales:{

x:{

ticks:{

color:"#b0b0b0",

maxRotation:45,

minRotation:45

},

grid:{

color:"#404b63",

display:false

}

},

y:{

beginAtZero:true,

ticks:{

color:"#b0b0b0",

maxTicksLimit:6

},

border:{

display:true,

color:"#404b63"

},

grid:{

color:"#404b63"

}

}

}

}

}

)

}

function createDistanceChart(data){

new Chart(

document.getElementById(
"distanceChart"
),

{

type:"line",

data:{

labels:
data.map(
x=>
x.name
),

datasets:[{

label:
"Distance (km)",

data:
data.map(
x=>
x.miss_distance
),

borderColor:
"#66ccff",

pointBackgroundColor:

data.map(
x=>

x.hazardous

?

"#ff4444"

:

"#66ccff"

),

pointRadius:6

}]

},

options:{

maintainAspectRatio:false,

plugins:{

legend:{

labels:{

color:"#b0b0b0"

}

}

},

scales:{

x:{

ticks:{

color:"#b0b0b0",

maxRotation:45,

minRotation:45

},

grid:{

color:"#404b63"

}

},

y:{

beginAtZero:true,

ticks:{

color:"#b0b0b0",

maxTicksLimit:6

},

grid:{

color:"#404b63"

}

}

}

}

}

)

}

async function init(){


loadHistory()


loadISS()


loadAPOD()


loadAsteroids()


}

init();
setInterval(loadISS, 5000);
