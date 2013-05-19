#ifndef __NEGAMAX_HPP
#define __NEGAMAX_HPP

using namespace __shedskin__;
namespace __negamax__ {

extern str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_2, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;

class TronClient;


extern tuple2<__ss_int, __ss_int> *__109, *me, *you;
extern __ss_int IPPROTO_TCP, PORT, TCP_NODELAY, TCP_QUICKACK, __ss_SHUT_RDWR, port;
extern list<tuple2<__ss_int, __ss_int> *> *moves;
extern str *STRUCT_DOWN_FRAME, *STRUCT_UP_LOGIN, *STRUCT_UP_MOVE, *__name__, *host;
extern list<list<__ss_bool> *> *a;
extern TronClient *tron;
extern double OO, starttime;


extern class_ *cl_TronClient;
class TronClient : public pyobj {
/**
non-threadsafe client which mimics the Turing API
*/
public:
    static tuple2<str *, str *> *OUTCOME;

    list<list<__ss_bool> *> *full;
    __ss_int _y;
    __ss_int _x;
    __ss_int _t;
    __socket__::socket *sock;
    __ss_int t;
    __ss_int y;
    __ss_int x;
    str *outcome;
    __ss_int dropped;

    TronClient() {}
    TronClient(int __ss_init) {
        this->__class__ = cl_TronClient;
        __init__();
    }
    static void __static__();
    void *_recv();
    __ss_bool ended();
    void *start(str *user, str *pw, str *host, __ss_int port);
    str *__repr__();
    void *__init__();
    void *_close();
};

extern str * default_1;
extern __ss_int  default_3;
extern str * default_0;
extern str * default_2;
extern double  default_4;

list<tuple2<__ss_int, __ss_int> *> *near(__ss_int x, __ss_int y);
list<list<double> *> *bfs(tuple2<__ss_int, __ss_int> *me);
__ss_int val(tuple2<__ss_int, __ss_int> *me, tuple2<__ss_int, __ss_int> *you);
double negamax(tuple2<__ss_int, __ss_int> *__77, tuple2<__ss_int, __ss_int> *__79, __ss_int depth, double alpha, double beta);
list<tuple2<__ss_int, __ss_int> *> *alphabeta(tuple2<__ss_int, __ss_int> *me, tuple2<__ss_int, __ss_int> *you, double alpha);

} // module namespace
#endif
