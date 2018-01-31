from flask import Flask, render_template, request
from snow import status, status_ip, rel_incidents, nagios_stat, nagios_stat_ip, dboard
import os,re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('layout.html')

@app.route("/incident")
def incidents():
    return render_template('incidents.html')

@app.route("/dashboard")
def dashboard():
    values=dboard()
    labels = ["OK", "WARNING", "CRIT", "UNKNOWN", "PENDING"]
    colors = ["#008000", "#FFFF00", "#800000", "#FFA500", "#808080"]
    return render_template('chart.html', set=zip(values, labels, colors), set2=zip(values, labels, colors))
    #return render_template('dashboard2.html', set=zip(values, labels, colors))

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/search")
def search():
    return render_template('search.html')

@app.route("/res", methods=['GET', 'POST'])
def res():
    if request.method == 'POST':
        name = request.form['hostname']
        pieces = name.split('.')

        if len(pieces) != 4:
            nag_data = nagios_stat(name)
            data = status(name)
        else :
            nag_data = nagios_stat_ip(name)
            data = status_ip(name)

        nag_name, nag_ip, nag_state, nag_info = ([] for i in range(4))
        host_name, ip, loc, manage, host_id, install_status, class_name = ([] for i in range(7))

        if nag_data['hoststatuslist']['recordcount'] != '0':
            if nag_data['hoststatuslist']['recordcount'] == '1':
                nag_name.append(nag_data['hoststatuslist']['hoststatus']['name'])
                nag_ip.append(nag_data['hoststatuslist']['hoststatus']['address'])
                nag_state.append(nag_data['hoststatuslist']['hoststatus']['current_state'])
                nag_info.append(nag_data['hoststatuslist']['hoststatus']['status_text'])
            else:
                for list in nag_data['hoststatuslist']['hoststatus']:
                 nag_name.append(list['name'])
                 nag_ip.append(list['address'])
                 nag_state.append(list['current_state'])
                 nag_info.append(list['status_text'])

        if not data['result'] and nag_data['hoststatuslist']['recordcount'] != '0':
            snow_err = "Host Not found in SNOW"
            return render_template('res.html', nag_name=nag_name, nag_ip=nag_ip, nag_state=nag_state, nag_info=nag_info, snow_err=snow_err)

        else:
            number, state, desc, assigned_team, inc_id, work_notes = ([] for i in range(6))
            for dt in data['result']:
                host_name.append(dt['name'])
                ip.append(dt['ip_address'])
                host_id.append(dt['sys_id'])
                install_status.append(dt['install_status'])
                class_name.append(dt['sys_class_name'])
                if not dt['managed_by']:
                    manage.append('')
                else:
                    manage.append(dt['managed_by']['display_value'])
                if not dt['location']:
                    loc.append('')
                else:
                    loc.append(dt['location']['display_value'])
                sys_id=dt['sys_id']
                inc_data=rel_incidents(sys_id)

                if inc_data['result']:
                    for list in inc_data['result']:
                        number.append(list['number'])
                        inc_id.append(list['sys_id'])
                        state.append(list['state'])
                        desc.append(list['short_description'])
                        assigned_team.append(list['assignment_group']['display_value'])
                        notes=list['work_notes'].split('(Work notes)')
                        try:
                         work_notes.append(notes[1])
                        except:
                         work_notes.append('')
                else:
                    err = "Active Incidents are not found for this host"
            nagios_host = name
            return render_template('res.html', host_name=host_name, ip=ip ,output="There is some issue", loc=loc, manage=manage,install_status=install_status,class_name=class_name, nagios_host=nagios_host, number=number , state=state, desc=desc, assigned_team=assigned_team,work_notes=work_notes, host_id=host_id, inc_id=inc_id, nag_name=nag_name, nag_ip=nag_ip, nag_state=nag_state, nag_info=nag_info)

if __name__ == "__main__":
    app.run(host='10.80.3.123', port=80, debug=True, use_reloader=True)
