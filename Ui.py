from nicegui import ui, app
from datetime import datetime

class Ui:
    def __init__(self, controlcenter):
        self.delaydata = [0, 0, 0, 0, 0, 0, 0, 0]
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
        #self.button = ui.button('Close', on_click=self.close_ui)
        
        
    def update(self, newdata):
        self.chart.options['series'][0]['data']= newdata
        self.delaydata = newdata
        self.chart.options['subtitle']['text']= self.timestamp()
        self.chart.update()
        return True

    def timestamp(self):
        return 'last updated: ' + datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    def shutdown(self):
        app.shutdown()
        ui.run_javascript('window.close()')
