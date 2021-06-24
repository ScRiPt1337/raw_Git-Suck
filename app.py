try:
    import requests
    from bs4 import BeautifulSoup
    from flask import Flask, render_template, request
    import os
except:
    import os
    os.system("sudo apt-get install python3-pip")
    os.system("sudo apt-get install python3-pip")
    os.system("python3 -m pip install Flask")
    os.system("python3 -m pip install bs4")
    os.system("python3 -m pip install requests")
    import requests
    from bs4 import BeautifulSoup
    from flask import Flask, render_template, request

app = Flask(__name__)


@app.route('/')
def index():
    giturl = str(request.base_url) + "raw?git=https://raw.githubusercontent.com/gogs/gogs/master/public/js/gogs.js"
    return render_template("index.html", urlx=giturl)


def rawtogit(s):
    str1 = ""
    z = 1
    for ele in s:
        if z >= 4:
            str1 += "/" + ele
        else:
            str1 += ele
        z = z + 1
    return str1


@app.route('/raw')
def rawgit():
    git = request.args.get('git')
    if git.startswith("https://raw.githubusercontent.com"):
        git = git.replace("https://raw.githubusercontent.com", "https://github.com").split("/")
        git[1] = "//"
        git.insert(5, 'blob')
        git = rawtogit(git)
        try:
            soup = BeautifulSoup(requests.get(git).content.decode(), 'html.parser')
            divs = soup.findAll("table", {"class": "highlight tab-size js-file-line-container"})
            data = []
            for div in divs:
                rows = div.findAll('tr')
                for row in rows:
                    new_data = row.text.replace("\n\n", "")
                    data.append(new_data)
            holyshit = ''.join(data).replace("\n\n", "\n")
            #print(holyshit)
            return render_template("response", data=''.join(holyshit))
        except Exception as e:
            return e
    else:
        return "not a valid raw.githubusercontent.com url"


if __name__ == '__main__':
    app.run(os.getenv('PORT'))
