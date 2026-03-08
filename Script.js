async function startCheck(){

let text=document.getElementById("usernames").value

let usernames=text.split("\n")

let res=await fetch("/check",{

method:"POST",
headers:{"Content-Type":"application/json"},
body:JSON.stringify({usernames:usernames})

})

let data=await res.json()

let checked=0
let available=0
let taken=0

let resultsDiv=document.getElementById("results")

resultsDiv.innerHTML=""

data.results.forEach(r=>{

checked++

if(r.status==="available") available++
if(r.status==="taken") taken++

let div=document.createElement("div")

div.innerText=r.username+" → "+r.status

resultsDiv.appendChild(div)

})

document.getElementById("checked").innerText=checked
document.getElementById("available").innerText=available
document.getElementById("taken").innerText=taken
document.getElementById("speed").innerText=data.speed

}
