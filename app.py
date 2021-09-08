from flask import Flask, request, render_template, url_for, g
import sys
sys.path.insert(1, '/home/lmconsole/frontend/network-vis 3/static')
import generate_topology as rt
sys.path.insert(1, '/home/lmconsole')
import nv_module
from lmconsole import *
# Flask constructor
app = Flask(__name__,
            static_folder='static',
            template_folder='templates')
# A decorator used to tell the application
# which URL is associated function

list_of_ips=[]

@app.route('/', methods =["GET", "POST"])
@app.route('/main.html')
def listener():
    if request.method == "POST":
       # getting input with ip's in HTML form
       ip = request.form.get("ip_addr")
       list_of_ips = ip.split(",")
       app.logger.info(list_of_ips)
       main_dict=nv_module.nv_topology(list_of_ips)
       TOPOLOGY_DICT = rt.generate_topology_json(main_dict)
       #Use only for debugging !!!
       #print(TOPOLOGY_DICT)
       CACHED_TOPOLOGY = rt.read_cached_topology()
       rt.write_topology_file(TOPOLOGY_DICT)
       rt.write_topology_cache(TOPOLOGY_DICT)
    return render_template("main.html")

@app.route('/main.html')
def current_topology():
    return render_template("main.html",the_title=' Current Topology')


@app.route('/diff_page.html')
def diffrence_page():
    app.logger.info(list_of_ips)
    return render_template("diff_page.html",the_title='Topology Diffrence')

if __name__=='__main__':
    app.run(debug=True,host='0.0.0.0')

