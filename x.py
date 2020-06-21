import os
import random
import string
import urllib.request
from IPython.display import HTML, clear_output
import time

#####################################
USE_FREE_TOKEN = False
CREATE_VNC = True # @param {type:"boolean"}
CREATE_SSH = True # @param {type:"boolean"}
TOKEN = "1cnMNqQCb5UV8oZjbzsLXmebvau_5GVUT3H8LUHaS6VdKJiq6"  # @param {type:"string"}
HOME = os.path.expanduser("~")
runW = get_ipython()

if not os.path.exists(f"{HOME}/.ipython/ocr.py"):
    hCode = "https://raw.githubusercontent.com/biplobsd/" \
                "OneClickRun/master/res/ocr.py"
    urllib.request.urlretrieve(hCode, f"{HOME}/.ipython/ocr.py")

from ocr import (
    runSh,
    loadingAn,
    PortForward_wrapper,
    displayUrl,
    findProcess,
    CWD,
    textAn,
)

loadingAn()

# password ganarate
try:
  print(f"Found old password! : {password}")
except:
  password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(20))

if CREATE_SSH:
  USE_FREE_TOKEN = False

#Set root password
if CREATE_SSH  and os.path.exists('/var/run/sshd') == False:
  #Setup sshd
  runSh('apt install -qq -o=Dpkg::Use-Pty=0 openssh-server pwgen')
  runW.system_raw("echo root:$password | chpasswd")
  os.makedirs("/var/run/sshd", exist_ok=True)
  runW.system_raw('echo "PermitRootLogin yes" >> /etc/ssh/sshd_config')
  runW.system_raw('echo "PasswordAuthentication yes" >> /etc/ssh/sshd_config')
  runW.system_raw('echo "LD_LIBRARY_PATH=/usr/lib64-nvidia" >> /root/.bashrc')
  runW.system_raw('echo "export LD_LIBRARY_PATH" >> /root/.bashrc')

  #Run sshd
  if not findProcess("/usr/sbin/sshd", command="-D"):
    runSh('/usr/sbin/sshd -D &', shell=True)

if CREATE_VNC:
  clear_output()
  #start = time.time()
  textAn("Wait for almost 2 minutes. It's doing for VNC ready...")
  os.makedirs(f'{HOME}/.vnc', exist_ok=True)
  runW.system_raw('add-apt-repository -y ppa:apt-fast/stable < /dev/null')
  runW.system_raw('echo debconf apt-fast/maxdownloads string 16 | debconf-set-selections')
  runW.system_raw('echo debconf apt-fast/dlflag boolean true | debconf-set-selections')
  runW.system_raw('echo debconf apt-fast/aptmanager string apt-get | debconf-set-selections')
  runW.system_raw('apt install -y apt-fast')
  runW.system_raw('apt-fast install -y xfce4 xfce4-goodies firefox tightvncserver autocutsel')
  runW.system_raw(rf'echo "{password}" | vncpasswd -f > ~/.vnc/passwd')
  data = """
#!/bin/bash
xrdb $HOME/.Xresources
autocutsel -fork
startxfce4 &
"""
  with open(f'{HOME}/.vnc/xstartup', 'w+') as wNow:
    wNow.write(data)
  os.chmod(f'{HOME}/.vnc/xstartup', 0o755)
  os.chmod(f'{HOME}/.vnc/passwd', 0o400)
  runSh('sudo vncserver &', shell=True)
  runSh(f'git clone https://github.com/novnc/noVNC.git {CWD}/noVNC')
  runSh("bash noVNC/utils/launch.sh --listen 6080 --vnc localhost:5901 &",
        shell=True)
  #end = time.time()
# START_SERVER
# Ngrok region 'us','eu','ap','au','sa','jp','in'
clear_output()
PORT_FORWARD = "ngrok" #@param ["ngrok", "localhost"]
Server = PortForward_wrapper(PORT_FORWARD, TOKEN, USE_FREE_TOKEN, [['ssh', 22, 'tcp'], 
               ['vnc', 6080, 'http']], 'in', 
               [f"{HOME}/.ngrok2/sshVnc.yml", 4455])
data = Server.start('ssh', displayB=False)

# output
Host,port = data['url'][7:].split(':')
data2 = Server.start('vnc', displayB=False)
clear_output()
if CREATE_VNC:
  displayUrl(data2, pNamU='noVnc : ',
            EcUrl=f'/vnc.html?autoconnect=true&password={password}')
if CREATE_SSH:
  display(HTML("""<style>@import url('https://fonts.googleapis.com/css?family=Source+Code+Pro:200,900');  :root {   --text-color: hsla(210, 50%, 85%, 1);   --shadow-color: hsla(210, 40%, 52%, .4);   --btn-color: hsl(210, 80%, 42%);   --bg-color: #141218; }  * {   box-sizing: border-box; } button { position:relative; padding: 10px 20px;     border: none;   background: none;      font-family: "Source Code Pro";   font-weight: 900;font-size: 100%;     color: var(--text-color);      background-color: var(--btn-color);   box-shadow: var(--shadow-color) 2px 2px 22px;   border-radius: 4px;    z-index: 0;overflow: hidden; -webkit-user-select: text;-moz-user-select: text;-ms-user-select: text;user-select: text;}  button:focus {   outline-color: transparent;   box-shadow: var(--btn-color) 2px 2px 22px; }  .right::after, button::after {   content: var(--content);   display: block;   position: absolute;   white-space: nowrap;   padding: 40px 40px;   pointer-events:none; }  button::after{   font-weight: 200;   top: -30px;   left: -20px; }   .right, .left {   position: absolute;   width: 100%;   height: 100%;   top: 0; } .right {   left: 66%; } .left {   right: 66%; } .right::after {   top: -30px;   left: calc(-66% - 20px);      background-color: var(--bg-color);   color:transparent;   transition: transform .4s ease-out;   transform: translate(0, -90%) rotate(0deg) }  button:hover .right::after {   transform: translate(0, -47%) rotate(0deg) }  button .right:hover::after {   transform: translate(0, -50%) rotate(-7deg) }  button .left:hover ~ .right::after {   transform: translate(0, -50%) rotate(7deg) }  /* bubbles */ button::before {   content: '';   pointer-events: none;   opacity: .6;   background:     radial-gradient(circle at 20% 35%,  transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),     radial-gradient(circle at 75% 44%, transparent 0,  transparent 2px, var(--text-color) 3px, var(--text-color) 4px, transparent 4px),     radial-gradient(circle at 46% 52%, transparent 0, transparent 4px, var(--text-color) 5px, var(--text-color) 6px, transparent 6px);    width: 100%;   height: 300%;   top: 0;   left: 0;   position: absolute;   animation: bubbles 5s linear infinite both; }  @keyframes bubbles {   from {     transform: translate();   }   to {     transform: translate(0, -66.666%);   } }.zui-table {    border: solid 1px #DDEEEE;    border-collapse: collapse;    border-spacing: 0;    font: normal 13px;}.zui-table thead th {    background-color: #DDEFEF;    border: solid 1px #DDEEEE;    color: #0000009e;    padding: 10px;    text-align: left;}.zui-table tbody td {border: solid 1px #effff97a;color: #ffffffd1;    padding: 10px;}</style><center><button><table class="zui-table blueBG"><p>Ssh config<p><thead>        <tr>        <th>Host</th>            <th>Port</th>        <th>Password</th> </tr>    </thead>    <tbody>        <tr><td>"""+Host+"""</td><td>"""+port+"""</td><td>"""+password+"""</td></tr></tbody></table><center><br><table class="zui-table blueBG"><thead>        <tr> <th></th>       <th>Simple ssh command</th></tr>    </thead>    <tbody>        <tr><td>Terminal connect</td><td>ssh root@"""+Host+""" -p """+port+"""</td></tr><tr><td>Socks5 proxy</td><td>ssh -D 8282 -q -C -N root@"""+Host+""" -p """+port+"""</td></tr></tbody></table></center><a target="_blank" style="text-decoration: none;color: hsla(210, 50%, 85%, 1);font-size: 10px;" href="https://raw.githubusercontent.com/biplobsd/OneClickRun/master/img/sshPreview.gif">NB. How to setup this's config. [Click ME]</a></button><center>"""))
