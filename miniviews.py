# a minimal example
import cyan

def helloworld(url, routes):
    return 'hello from cyan'

if __name__=='__main__':
    hello = cyan.app('helloworld')
    hello.route('/', helloworld)
    hello.run()

