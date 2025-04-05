from nicegui import ui, app
from datetime import datetime

class Ui:
    def __init__(self, controlcenter, interval):
        self.interval = interval
        self.delaydata = [0, 0, 0, 0, 0, 0, 0, 0]
        #
        # live delay chart
        #
        with ui.column().classes('w-full items-center'):
            result = ui.label().classes('mr-auto')
            with ui.button(icon='menu'):
                with ui.menu() as menu:
                    ui.menu_item('Shutdown Sum Of Delay', self.shutdown)
        self.chart = ui.highchart({
            'title': {'text': 'Sum Of Delay - ' + controlcenter},
            'subtitle': {'text': self.timestamp()},
            'chart': {'type': 'bar'},
            'xAxis': {'categories': ['freight', 'longdistance', 'regional', 'city', 'special', 'loco', 'construction', 'other']},
            'yAxis': {'title': {'text': 'delay [min]'}},
            'plotOptions': {
                'series': {
                    'dataLabels': {
                        'enabled': True,
                        'format': '{y}',
                        'style': {
                            'color': 'black',
                            'fontWeight': 'bold',
                            'textOutline': 'none',
                        },
                    }
                }
            },
            'series': [
                {'name': 'Delay per Train Type', 'data': self.delaydata, 'color': '#86bac1'}
            ],
        }).classes('h-256')
        
        self.freighttrack = [0]
        self.longdistancetrack = [0]
        self.regionaltrack = [0]
        self.citytrack = [0]
        self.specialtrack = [0]
        self.locotrack = [0]
        self.constructiontrack = [0]
        self.othertrack = [0]
        self.time = [0.0]
        #
        # track record
        #
        self.timedata = {
            'data': [
                {
                    'type': 'scatter',
                    'name': 'freight',
                    'x': self.time,
                    'y': self.freighttrack,
                },
                {
                    'type': 'scatter',
                    'name': 'longdistance',
                    'x': self.time,
                    'y': self.longdistancetrack,
                },
                {
                    'type': 'scatter',
                    'name': 'regional',
                    'x': self.time,
                    'y': self.regionaltrack,
                },
                {
                    'type': 'scatter',
                    'name': 'city',
                    'x': self.time,
                    'y': self.citytrack,
                },
                {
                    'type': 'scatter',
                    'name': 'special',
                    'x': self.time,
                    'y': self.specialtrack,
                },
                {
                    'type': 'scatter',
                    'name': 'loco',
                    'x': self.time,
                    'y': self.locotrack,
                },
                {
                    'type': 'scatter',
                    'name': 'construction',
                    'x': self.time,
                    'y': self.constructiontrack,
                },
                {
                    'type': 'scatter',
                    'name': 'other',
                    'x': self.time,
                    'y': self.othertrack,
                },
            ],
            'layout': {
                'margin': {'l': 40, 'r': 0, 't': 30, 'b': 40},
                'plot_bgcolor': '#E5ECF6',
                'xaxis': {'gridcolor': 'white', 'title': {'text': 'Elapsed shift time [min]'}},
                'yaxis': {'gridcolor': 'white', 'title': {'text': 'Delay [min]'}},
                'title': {'text': 'Sum Of Delay - ' + controlcenter},
            },
        }
        self.timetrack = ui.plotly(self.timedata).classes('w-full h-256')
        
    def update(self, newdata):
        # live chart
        self.chart.options['series'][0]['data']= newdata
        self.delaydata = newdata
        self.chart.options['subtitle']['text']= self.timestamp()
        self.chart.update()

        # time track record
        self.time.append(self.time[len(self.time)-1] + self.interval/60)
        self.freighttrack.append(newdata[0])
        self.longdistancetrack.append(newdata[1])
        self.regionaltrack.append(newdata[2])
        self.citytrack.append(newdata[3])
        self.specialtrack.append(newdata[4])
        self.locotrack.append(newdata[5])
        self.constructiontrack.append(newdata[6])
        self.othertrack.append(newdata[7])
        self.timetrack.update()
        return True

    def timestamp(self):
        return 'last updated: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def shutdown(self):
        app.shutdown()
        ui.run_javascript('window.close()')
