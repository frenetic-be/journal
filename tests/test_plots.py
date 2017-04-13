# to use this, cd .. from this directory and type
# "python -m unittest tests.test_plots"

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))

import unittest as _unittest
import journal as lg
datetime = lg._dt
numpy = lg._numpy
plt = lg._plt

LOGFILE = 'tests/HumTemp_20150417.txt'

class TestTimeplot(_unittest.TestCase):

    def setUp(self):
        self.data = lg.read_csv(LOGFILE)

    def test_basic_plot(self):
        self.data.timeplot(self.data['temp enclosure'])
        plt.savefig('tests/plots/basic.png')

    def test_basic2_plot(self):
        self.data.timeplot(self.data['temp enclosure'],
                           ylabel='Temperature (in C)',
                           xlabel='Marshmallows',
#                            title ='A temperature plot',
                           color = 'r',
#                            linewidth = 4,
#                            marker = 's',
                           )
        plt.savefig('tests/plots/basic2.png')

    def test_basic_plot_title(self):
        self.data.timeplot(self.data['temp enclosure'],
                           ylabel='Temperature (in C)',
                            title ='A temperature plot',
                           )
        plt.savefig('tests/plots/basic_title.png')
        
    def test_no_grid(self):
        self.data.timeplot(self.data['temp enclosure'],
                           grid=False,
                           )
        plt.savefig('tests/plots/no_grid.png')
        
    def test_no_legend(self):
        self.data.timeplot(self.data['temp enclosure'],
                           legend=False,
                           )
        plt.savefig('tests/plots/no_legend.png')
    
    def test_tupled_data(self):
        
        self.data.timeplot((self.data['temp enclosure'],))
        plt.savefig('tests/plots/tupled_data_1.png')

        self.data.timeplot((self.data['temp enclosure'],
                            self.data['temp dome']))
        plt.savefig('tests/plots/tupled_data_2.png')

        self.data.timeplot((self.data['temp enclosure'],
                            self.data['temp dome']),
                           color='r',
                           linewidth=3,
                           marker='+')
        plt.savefig('tests/plots/tupled_data_3.png')

        self.data.timeplot((self.data['temp enclosure'],
                            self.data['temp dome']),
                           color=('r', 'g'),
                           lw=(3, 1),
                           marker=('+', 's'))
        plt.savefig('tests/plots/tupled_data_4.png')
        
    def test_all_data(self):
        
        self.data.timeplot()
        plt.savefig('tests/plots/all_data.png')
        
    def test_time_format_seconds(self):
        self.data.timeplot(self.data['temp enclosure'], time_format='secs')
        plt.savefig('tests/plots/time_format_seconds.png')

    def test_time_format_minutes(self):
        self.data.timeplot(self.data['temp enclosure'], time_format='mins')
        plt.savefig('tests/plots/time_format_minutes.png')

    def test_time_format_hours(self):
        self.data.timeplot(self.data['temp enclosure'], time_format='hours')
        plt.savefig('tests/plots/time_format_hours.png')
    
    def test_time_format_days(self):
        self.data.timeplot(self.data['temp enclosure'], time_format='days')
        plt.savefig('tests/plots/time_format_days.png')

    def test_time_format_jds(self):
        self.data.timeplot(self.data['temp enclosure'], time_format='jd')
        plt.savefig('tests/plots/time_format_jds.png')
        
    def test_time_format_auto(self):
        self.data.timeplot(self.data['temp enclosure'], time_format='')
        plt.savefig('tests/plots/time_format_auto.png')

    def test_time_format_custom(self):
        self.data.timeplot(self.data['temp enclosure'], time_format='%H:%M')
        plt.savefig('tests/plots/time_format_custom.png')

    def test_two_axes(self):
        self.data.timeplot(self.data['temp enclosure'],
                           right_data=self.data['hum enclosure'])
        plt.savefig('tests/plots/two_axes.png')
        self.data.timeplot(self.data['temp enclosure'],
                           right_data=self.data['hum enclosure'],
                           time_format='%H:%M',
                           title='Humidity and temperature data',
                           ylabel='Temperature (in C)',
                           right_label='Humidity (in %)',
                           color='g',
                           right_color='b',
                           )
        plt.savefig('tests/plots/two_axes_2.png')
