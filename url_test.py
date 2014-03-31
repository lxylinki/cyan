from string import Template
import cyan
import views

if __name__=='__main__':
    cyan.route('hello_cyan', views.hello_cyan)
    cyan.route('seeyou_cyan', views.seeyou_cyan)
    cyan.runapp('localhost', 20143, views.devcyan)
