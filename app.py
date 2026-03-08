from flask import Flask, render_template, request, jsonify, send_file
import aiohttp
import asyncio
import time

app = Flask(__name__)

URL="https://discord.com/api/v9/unique-username/username-attempt-unauthed"

available=[]

async def check_username(session,username):

    async with session.post(URL,json={"username":username}) as r:

        if r.status==200:

            data=await r.json()

            if not data.get("taken"):

                available.append(username)

                return {"username":username,"status":"available"}

            return {"username":username,"status":"taken"}

        return {"username":username,"status":"error"}


async def run_checker(usernames):

    connector=aiohttp.TCPConnector(limit=30)

    async with aiohttp.ClientSession(connector=connector) as session:

        tasks=[check_username(session,u) for u in usernames]

        results=await asyncio.gather(*tasks)

    return results


@app.route("/")
def home():

    return render_template("index.html")


@app.route("/check",methods=["POST"])
def check():

    start=time.time()

    usernames=request.json["usernames"]

    results=asyncio.run(run_checker(usernames))

    speed=round(len(usernames)/(time.time()-start),2)

    with open("available.txt","w") as f:

        for u in available:
            f.write(u+"\n")

    return jsonify({
        "results":results,
        "speed":speed
    })


@app.route("/download")
def download():

    return send_file("available.txt",as_attachment=True)


app.run(debug=True)
