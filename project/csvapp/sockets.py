from socketio.namespace import BaseNamespace
from socketio.sdjango import namespace


@namespace('/battleship')
class BattleshipNamespace(BaseNamespace):
    def initialize(self):
        pass
        # self.session.player = self.player = \
        #     PlayerActor.start(self.request.user, self.socket).proxy()

    def disconnect(self, *args, **kwargs):
        super(BattleshipNamespace, self).disconnect(*args, **kwargs)

    # def get_initial_acl(self):
    #     return ['recv_connect']

    # def recv_connect(self):
    #     if self.request.user.is_authenticated():
    #         self.add_acl_method('on_joinqueue')
    #     else:
    #         self.disconnect()

    # def on_joinqueue(self):
    #     self.del_acl_method('on_joinqueue')
    #     self.add_acl_method('on_leavequeue')
    #     match_maker.join(self.player)

    # def on_leavequeue(self):
    #     self.del_acl_method('on_leavequeue')
    #     self.add_acl_method('on_joinqueue')
    #     match_maker.leave(self.player)
