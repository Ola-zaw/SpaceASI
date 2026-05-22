const API =
"http://localhost:8000"



let map =
L.map(
"iss-map"
)
.setView(
[0,0],
2
)


L.tileLayer(
"https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
)
.addTo(
map
)



let marker =
L.marker(
[0,0]
)
.addTo(
map
)


let line=
L.polyline(
[],
{
color:"cyan",
weight:3
}
)
.addTo(
map
)

let path=[]


async function loadHistory(){

const response=
await fetch(
`${API}/iss/history`
)

const data=
await response.json()


path=
data.map(
p=>[
p.latitude,
p.longitude
]
)


line.setLatLngs(
path
)


if(
path.length
){

marker.setLatLng(
path[
path.length-1
]
)

map.fitBounds(
line.getBounds()
)

}

}

async function loadISS(){

const response=
await fetch(
`${API}/iss/latest`
)

const data=
await response.json()


marker.setLatLng(
[
data.latitude,
data.longitude
]
)


const newPoint=[
data.latitude,
data.longitude
]

const last=
path[
path.length-1
]

if(
!last
||
last[0]!==newPoint[0]
||
last[1]!==newPoint[1]
){

path.push(
newPoint
)

}


if(
path.length>90
){

path.shift()

}


line.setLatLngs(
path
)


if(
path.length===1
){

map.setView(
[
data.latitude,
data.longitude
],
3
)

}


document
.getElementById(
"iss-coords"
)
.innerHTML=

`
Latitude:
${data.latitude}

<br>

Longitude:
${data.longitude}
`

}



async function loadAPOD(){

const response=
await fetch(
`${API}/apod/latest`
)

const data=
await response.json()


document
.getElementById(
"apod-container"
)
.innerHTML=

`

<h4
class="apod-title">

${data.title}

</h4>


<img
class="apod-img"
src="${data.image_url}">


<div
class="apod-description">

${data.explanation}

</div>

`

}



async function loadAsteroids(){


const statsResponse=
await fetch(
`${API}/asteroids/stats`
)

const stats=
await statsResponse.json()



const response=
await fetch(
`${API}/asteroids`
)

const data=
await response.json()



document
.getElementById(
"stats"
)
.innerHTML=

`

Total:
${stats.total}

|

Dangerous:
${stats.hazardous}



`


let rows=""


data.forEach(
a=>{

rows+=`

<tr>

<td>

${a.name}

</td>


<td>

${Math.round(
a.diameter
)}

m

</td>


<td>

${Math.round(
a.miss_distance
)
.toLocaleString()}

km

</td>


<td>

${Math.round(
a.velocity
)
.toLocaleString()}

km/h

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
}">

${
a.hazardous
?
"🔴 YES"
:
"🟢 NO"
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
.innerHTML=
rows



createVelocityChart(
data
)


createDistanceChart(
data
)

}



function createVelocityChart(
data
){

new Chart(

document
.getElementById(
"asteroidsChart"
),

{

type:"bar",

data:{

labels:
data
.slice(0,8)
.map(
x=>
x.name
),

datasets:[{

label:
"Velocity",

data:
data
.slice(0,8)
.map(
x=>
x.velocity
)

}]

}

}

)

}



function createDistanceChart(
data
){

new Chart(

document
.getElementById(
"distanceChart"
),

{

type:"line",

data:{

labels:
data
.slice(0,8)
.map(
x=>
x.name
),

datasets:[{

label:
"Distance",

data:
data
.slice(0,8)
.map(
x=>
x.miss_distance
)

}]

}

}

)

}



loadHistory()

setTimeout(
loadISS,
500
)

loadAPOD()

loadAsteroids()


setInterval(
loadISS,
5000
)
