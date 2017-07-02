import re
from .utils import singleton


@singleton
class Broadcast(object):
    radio_list = []
    app = None
    updated_events = {}
    
    OKGREEN = '\033[92m'
    ENDC = '\033[0m'

    def __init__(self, app=None):
        self.app = app

    def send(self, events='some_events', *args, **kargs):
        # 遍历radio列表并调用事件，事件不存在或未被截断继续在radio列表内遍历
        # 使用正则表达式修改事件名称
        for oldRe, newRe in self.updated_events.items():
            # 比对正则表达式是否匹配，匹配则替换
            new_events = re.sub(oldRe, newRe, events)
            if new_events != events:
                if self.app and self.app.debug:
                    print('BROADCAST INFO: \033[92m [event replace] \033[0m event \'{}\' replace to \'{}\''.format(
                        events, new_events))
                events = new_events
                
        filted_radio_list = []
        for radio in self.radio_list:
            if radio.filter(events):
                filted_radio_list.append(radio)
        for radio in filted_radio_list:
            func = getattr(radio, events, None)
            if func:
                stop = func(*args, **kargs)
                if self.app and self.app.debug:
                    print('BROADCAST INFO: \033[94m [event run] \033[0m event \'{}\' run at events handler \'{}\''.format(
                        events, func.__name__))
                if stop:
                    if self.app and self.app.debug:
                        print('BROADCAST INFO: \033[95m [event stop] \033[0m event \'{}\' stop at events handler \'{}\''.format(
                            events, func.__name__))
                    break
            else:
                if self.app and self.app.debug:
                    print("BROADCAST INFO: \033[93m [handler not funoud] \033[0m there are not events handler '{}' in radio '{}'".format(
                        events, radio.__class__.__name__))

    def replace_event(self, old_events_Re_str, new_events_Re_str):
        self.updated_events.update({old_events_Re_str: new_events_Re_str})

    def register(self, radio):
        # 将radio记录到radio列表
        if radio not in self.radio_list:
            self.radio_list.append(radio())

    def unregister(self, radio):
        # 将radio记录到radio列表
        if radio in self.radio_list:
            self.radio_list.remove(radio())

class Radio():

    def filter(self, events):
        # 如果返回true则响应events标记的事件，建议使用正则表达是进行判断
        return False

    def some_events(self, *args, **kargs):
        # events 处理函数，处理由broadcast发送的事件
        # 返回 True 这停止该事件的传播
        return True
    # radio是一个泛类
