#include "builtin.hpp"
#include "socket.hpp"
#include "sys.hpp"
#include "random.hpp"
#include "struct.hpp"
#include "math.hpp"
#include "time.hpp"
#include "negamax.hpp"

#ifndef DEPTH
#define DEPTH 3
#endif


namespace __negamax__ {

str *const_0, *const_1, *const_10, *const_11, *const_12, *const_13, *const_14, *const_15, *const_16, *const_2, *const_3, *const_4, *const_5, *const_6, *const_7, *const_8, *const_9;

using __struct__::calcsize;
using __struct__::unpack;
using __struct__::pack;
using __random__::choice;
using __time__::time;

tuple2<__ss_int, __ss_int> *__109, *me, *you;
list<tuple2<__ss_int, __ss_int> *> *moves;
TronClient *tron;
str *STRUCT_DOWN_FRAME, *STRUCT_UP_LOGIN, *STRUCT_UP_MOVE, *__name__, *host;
list<list<__ss_bool> *> *a;
__ss_int IPPROTO_TCP, PORT, TCP_NODELAY, TCP_QUICKACK, __ss_SHUT_RDWR, port;
double OO, starttime;


str * default_1;
__ss_int  default_3;
str * default_0;
str * default_2;
double  default_4;

static inline list<list<__ss_bool> *> *list_comp_0();
static inline list<list<__ss_bool> *> *list_comp_1();
static inline list<tuple2<__ss_int, __ss_int> *> *list_comp_2(__ss_int y, __ss_int x);
static inline list<list<double> *> *list_comp_3();
class list_comp_4 : public __iter<__ss_bool> {
public:
    list<double>::for_in_loop __60;
    double v;
    list<list<double> *>::for_in_loop __56;
    __iter<list<double> *> *__54;
    list<list<double> *> *__53;
    list<double> *__57, *row;
    __ss_int __55, __59;
    __iter<double> *__58;

    list<list<double> *> *dyou;
    int __last_yield;

    list_comp_4(list<list<double> *> *dyou);
    __ss_bool __get_next();
};

class list_comp_5 : public __iter<__ss_bool> {
public:
    list<double>::for_in_loop __68;
    double v;
    list<list<double> *>::for_in_loop __64;
    __iter<list<double> *> *__62;
    list<list<double> *> *__61;
    list<double> *__65, *row;
    __ss_int __63, __67;
    __iter<double> *__66;

    list<list<double> *> *dme;
    int __last_yield;

    list_comp_5(list<list<double> *> *dme);
    __ss_bool __get_next();
};

class list_comp_6 : public __iter<__ss_int> {
public:
    __ss_int __69, __70, __71, __72, i, j;

    list<list<double> *> *dme;
    int __last_yield;

    list_comp_6(list<list<double> *> *dme);
    __ss_int __get_next();
};

class list_comp_7 : public __iter<__ss_int> {
public:
    __ss_int __73, __74, __75, __76, i, j;

    list<list<double> *> *dyou;
    int __last_yield;

    list_comp_7(list<list<double> *> *dyou);
    __ss_int __get_next();
};

class list_comp_8 : public __iter<tuple2<__ss_int, __ss_int> *> {
public:
    __ss_bool __102, __103, __104;
    __ss_int __100, __101, __98, __99, i, j;

    int __last_yield;

    list_comp_8();
    tuple2<__ss_int, __ss_int> * __get_next();
};

static inline list<list<__ss_bool> *> *list_comp_9();

static inline list<list<__ss_bool> *> *list_comp_0() {
    __ss_int _, __1, __2;

    list<list<__ss_bool> *> *__ss_result = new list<list<__ss_bool> *>();

    FAST_FOR(_,0,50,1,1,2)
        __ss_result->append(((new list<__ss_bool>(1,False)))->__mul__(49));
    END_FOR

    return __ss_result;
}

static inline list<list<__ss_bool> *> *list_comp_1() {
    __ss_int _, __20, __21;

    list<list<__ss_bool> *> *__ss_result = new list<list<__ss_bool> *>();

    FAST_FOR(_,0,50,1,20,21)
        __ss_result->append(((new list<__ss_bool>(1,False)))->__mul__(49));
    END_FOR

    return __ss_result;
}

static inline list<tuple2<__ss_int, __ss_int> *> *list_comp_2(__ss_int y, __ss_int x) {
    tuple2<__ss_int, __ss_int> *__22;
    tuple2<tuple2<__ss_int, __ss_int> *, tuple2<__ss_int, __ss_int> *> *__23;
    __ss_bool __27, __28, __29;
    __iter<tuple2<__ss_int, __ss_int> *> *__24;
    __ss_int __25, nx, ny;
    tuple2<tuple2<__ss_int, __ss_int> *, tuple2<__ss_int, __ss_int> *>::for_in_loop __26;

    list<tuple2<__ss_int, __ss_int> *> *__ss_result = new list<tuple2<__ss_int, __ss_int> *>();

    __23 = (new tuple2<tuple2<__ss_int, __ss_int> *, tuple2<__ss_int, __ss_int> *>(4,(new tuple2<__ss_int, __ss_int>(2,(x-1),y)),(new tuple2<__ss_int, __ss_int>(2,(x+1),y)),(new tuple2<__ss_int, __ss_int>(2,x,(y-1))),(new tuple2<__ss_int, __ss_int>(2,x,(y+1)))));
    FOR_IN(__22,__23,23,25,26)
        __22 = __22;
        nx = __22->__getfirst__();
        ny = __22->__getsecond__();
        if (((0<=nx)&&(nx<50) and (0<=ny)&&(ny<49) and __NOT((a->__getfast__(nx))->__getfast__(ny)))) {
            __ss_result->append((new tuple2<__ss_int, __ss_int>(2,nx,ny)));
        }
    END_FOR

    return __ss_result;
}

static inline list<list<double> *> *list_comp_3() {
    __ss_int _, __30, __31;

    list<list<double> *> *__ss_result = new list<list<double> *>();

    FAST_FOR(_,0,50,1,30,31)
        __ss_result->append(((new list<double>(1,OO)))->__mul__(49));
    END_FOR

    return __ss_result;
}

list_comp_4::list_comp_4(list<list<double> *> *dyou) {
    this->dyou = dyou;
    __last_yield = -1;
}

__ss_bool list_comp_4::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FOR_IN(row,dyou,53,55,56)
        FOR_IN(v,row,57,59,60)
            __result = ___bool((v==OO));
            return __result;
            __after_yield_0:;
        END_FOR

    END_FOR

    __stop_iteration = true;
}

list_comp_5::list_comp_5(list<list<double> *> *dme) {
    this->dme = dme;
    __last_yield = -1;
}

__ss_bool list_comp_5::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FOR_IN(row,dme,61,63,64)
        FOR_IN(v,row,65,67,68)
            __result = ___bool(__eq(v, OO));
            return __result;
            __after_yield_0:;
        END_FOR

    END_FOR

    __stop_iteration = true;
}

list_comp_6::list_comp_6(list<list<double> *> *dme) {
    this->dme = dme;
    __last_yield = -1;
}

__ss_int list_comp_6::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(i,0,50,1,69,70)
        FAST_FOR(j,0,49,1,71,72)
            if (__ne((dme->__getfast__(i))->__getfast__(j), OO)) {
                __result = len(near(i, j));
                return __result;
                __after_yield_0:;
            }
        END_FOR

    END_FOR

    __stop_iteration = true;
}

list_comp_7::list_comp_7(list<list<double> *> *dyou) {
    this->dyou = dyou;
    __last_yield = -1;
}

__ss_int list_comp_7::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(i,0,50,1,73,74)
        FAST_FOR(j,0,49,1,75,76)
            if (((dyou->__getfast__(i))->__getfast__(j)!=OO)) {
                __result = len(near(i, j));
                return __result;
                __after_yield_0:;
            }
        END_FOR

    END_FOR

    __stop_iteration = true;
}

list_comp_8::list_comp_8() {
    __last_yield = -1;
}

tuple2<__ss_int, __ss_int> * list_comp_8::__get_next() {
    if(!__last_yield) goto __after_yield_0;
    __last_yield = 0;

    FAST_FOR(i,0,50,1,98,99)
        FAST_FOR(j,0,49,1,100,101)
            if (__AND(((tron->full)->__getfast__(i))->__getfast__(j), __AND(__NOT((a->__getfast__(i))->__getfast__(j)), ___bool(__ne((new tuple2<__ss_int, __ss_int>(2,i,j)), me)), 103), 102)) {
                __result = (new tuple2<__ss_int, __ss_int>(2,i,j));
                return __result;
                __after_yield_0:;
            }
        END_FOR

    END_FOR

    __stop_iteration = true;
}

static inline list<list<__ss_bool> *> *list_comp_9() {
    __iter<list<__ss_bool> *> *__106;
    list<__ss_bool> *row;
    list<list<__ss_bool> *> *__105;
    __ss_int __107;
    list<list<__ss_bool> *>::for_in_loop __108;

    list<list<__ss_bool> *> *__ss_result = new list<list<__ss_bool> *>();

    __105 = tron->full;
    __ss_result->resize(len(__105));
    FOR_IN(row,__105,105,107,108)
        __ss_result->units[__107] = row->__slice__(0, 0, 0, 0);
    END_FOR

    return __ss_result;
}

/**
class TronClient
*/

class_ *cl_TronClient;

void *TronClient::_recv() {
    list<__ss_bool> *__13;
    str *__3, *a, *outcome;
    __ss_int __10, __11, __12, __4, __9, i, j, k;
    __ss_bool __5, __6, __7, __8;

    __3 = (this->sock)->recv(calcsize(STRUCT_DOWN_FRAME), 0);
    __4 = 0;
    this->_t = __struct__::unpack_int('<', 'i', 1, __3, &__4);
    this->_x = __struct__::unpack_int('<', 'i', 1, __3, &__4);
    this->_y = __struct__::unpack_int('<', 'i', 1, __3, &__4);
    a = __struct__::unpack_str('<', 's', 307, __3, &__4);
    (this->sock)->setsockopt(IPPROTO_TCP, TCP_QUICKACK, 1);
    this->_t = (this->_t-1);
    this->_x = (this->_x-1);
    this->_y = (this->_y-1);
    if ((this->_x!=(-1))) {
        this->t = (this->_t+1);
        if (((this->_t>1) and ((this->x!=this->_x) or (this->y!=this->_y)))) {
            this->dropped = (this->dropped+1);
        }
        this->x = this->_x;
        this->y = this->_y;
    }
    else {
        this->_close();
        outcome = (TronClient::OUTCOME)->__getfast__((this->_y+1));
        this->__init__();
        this->outcome = outcome;
    }

    FAST_FOR(i,0,50,1,9,10)

        FAST_FOR(j,0,49,1,11,12)
            k = ((i*49)+j);
            (this->full)->__getfast__(i)->__setitem__(j, ___bool(((((ord(a->__getfast__(__divs(k, 8)))>>__mods(k, 8)))&(1))==1)));
        END_FOR

    END_FOR

    return NULL;
}

__ss_bool TronClient::ended() {
    __ss_bool __14, __15, __16, __17, err;

    if (__NOT(___bool(this->sock))) {
        return True;
    }
    err = False;
    if ((this->t>=0)) {
        ASSERT(__AND(___bool(((__abs((this->_x-this->x))+__abs((this->_y-this->y)))<=(this->t-this->_t))), __OR(___bool((this->t!=(this->_t+1))), ___bool(((__power((this->_x-this->x), 2)+__power((this->_y-this->y), 2))==1)), 15), 14), 0);
        try {
            (this->sock)->sendall(pack(3, STRUCT_UP_MOVE, ___box(((this->t+1))), ___box(((this->x+1))), ___box(((this->y+1)))), 0);
        } catch (IOError *) {
            err = True;
        }
    }
    try {
        this->_recv();
    } catch (IOError *) {
        err = True;
    }
    if (err) {
        this->_close();
    }
    return __NOT(___bool(this->sock));
}

void *TronClient::start(str *user, str *pw, str *host, __ss_int port) {
    str *buf;

    this->sock = (new __socket__::socket(__socket__::default_0, __socket__::default_1, 0));
    (this->sock)->connect((new tuple2<str *, __ss_int>(2,host,port)));
    (this->sock)->setsockopt(IPPROTO_TCP, TCP_NODELAY, 1);
    buf = const_0;
    if ((user!=NULL)) {
        buf = __add_strs(3, buf, const_1, pack(2, STRUCT_UP_LOGIN, user, pw));
    }
    buf = (buf)->__iadd__(const_2);
    (this->sock)->sendall(buf, 0);
    return NULL;
}

str *TronClient::__repr__() {
    
    return __modct(const_3, 6, (this->__class__)->__name__, ___box(this->dropped), ___box(this->t), ___box(this->x), ___box(this->y), this->outcome);
}

void *TronClient::__init__() {
    __ss_int __0;

    __0 = (-1);
    this->_t = __0;
    this->_x = __0;
    this->_y = __0;
    this->t = __0;
    this->x = __0;
    this->y = __0;
    this->outcome = const_4;
    this->sock = NULL;
    this->full = list_comp_0();
    this->dropped = 0;
    return NULL;
}

void *TronClient::_close() {
    
    (this->sock)->shutdown(__ss_SHUT_RDWR);
    try {
        (this->sock)->close();
    } catch (Exception *) {
    }
    this->sock = NULL;
    return NULL;
}

tuple2<str *, str *> *TronClient::OUTCOME;

void TronClient::__static__() {
    OUTCOME = (new tuple2<str *, str *>(4,const_5,const_6,const_7,const_5));
}

list<tuple2<__ss_int, __ss_int> *> *near(__ss_int x, __ss_int y) {
    
    return list_comp_2(y, x);
}

list<list<double> *> *bfs(tuple2<__ss_int, __ss_int> *me) {
    tuple2<__ss_int, __ss_int> *__38;
    list<double>::for_in_loop __37;
    list<tuple2<__ss_int, __ss_int> *> *__39;
    double __33, d;
    list<tuple2<__ss_int, __ss_int> *>::for_in_loop __42;
    list<list<double> *> *dist;
    list<double> *__32, *__34, *__43, *q;
    __iter<tuple2<__ss_int, __ss_int> *> *__40;
    __ss_int __36, __41, nx, ny, x, y;
    __iter<double> *__35;

#if 0
    q = (new list<double>(1,((double)(me))));
    dist = list_comp_3();
    dist->__getfast__(me->__getfirst__())->__setitem__(me->__getsecond__(), 0.0);

    FOR_IN(__33,q,34,36,37)
        __33 = __33;
        x = __33->__getitem__(0);
        y = __33->__getitem__(1);
        d = ((dist->__getfast__(x))->__getfast__(y))->__add__(1.0);

        FOR_IN(__38,near(x, y),39,41,42)
            __38 = __38;
            nx = __38->__getfirst__();
            ny = __38->__getsecond__();
            if (__eq((dist->__getfast__(nx))->__getfast__(ny), OO)) {
                dist->__getfast__(nx)->__setitem__(ny, d);
                q->append((new doubl(2,nx,ny)));
            }
        END_FOR

    END_FOR
#endif
    static __ss_int q_x[2450],q_y[2450];
    int l=1;
    q_x[0]=me->__getfirst__();
    q_y[0]=me->__getsecond__();
    dist = list_comp_3();
    dist->__getfast__(me->__getfirst__())->__setitem__(me->__getsecond__(), ((double )0));

    for(int i=0;i<l;++i){
        x =q_x[i];
        y =q_y[i];
        d = ((dist->__getfast__(x))->__getfast__(y)+1);
#define BFS_VISIT(nx,ny) \
            if (nx>=0&&ny>=0&&nx<50&&ny<49&&__NOT((a->__getfast__(nx))->__getfast__(ny))&&((dist->__getfast__(nx))->__getfast__(ny)==OO)) {\
                dist->__getfast__(nx)->__setitem__(ny, d);\
		q_x[l]=nx;\
		q_y[l++]=ny;\
            }
        BFS_VISIT((x+1),y);
        BFS_VISIT(x,(y+1));
        BFS_VISIT((x-1),y);
        BFS_VISIT(x,(y-1));

    }

    return dist;
}

__ss_int val(tuple2<__ss_int, __ss_int> *me, tuple2<__ss_int, __ss_int> *you) {
    tuple2<__ss_int, __ss_int> *__44;
    list<tuple2<__ss_int, __ss_int> *> *__45;
    double dx, dy;
    list<tuple2<__ss_int, __ss_int> *>::for_in_loop __48;
    list<list<double> *> *dme, *dyou;
    __iter<tuple2<__ss_int, __ss_int> *> *__46;
    __ss_int __47, __49, __50, __51, __52, i, j, s, x, y;

    dme = bfs(me);
    dyou = bfs(you);

    FOR_IN(__44,near(me->__getfirst__(), me->__getsecond__()),45,47,48)
        __44 = __44;
        x = __44->__getfirst__();
        y = __44->__getsecond__();
        if (((dyou->__getfast__(x))->__getfast__(y)!=OO)) {
            s = 0;

            FAST_FOR(i,0,50,1,49,50)

                FAST_FOR(j,0,49,1,51,52)
                    dx = (dyou->__getfast__(i))->__getfast__(j);
                    dy = (dme->__getfast__(i))->__getfast__(j);
                    s = (s+(___bool(__gt(dx, dy))-___bool(__gt(dy, dx))));
                END_FOR

            END_FOR

            return s;
        }
    END_FOR

    return ((20*(__sum(new list_comp_4(dyou))-__sum(new list_comp_5(dme))))+(88*(__sum(new list_comp_6(dme))-__sum(new list_comp_7(dyou)))));
}

double negamax(tuple2<__ss_int, __ss_int> *__77, tuple2<__ss_int, __ss_int> *__79, __ss_int depth, double alpha, double beta) {
    tuple2<__ss_int, __ss_int> *__78, *__80, *__81, *you;
    list<__ss_bool> *__86, *__87;
    double v;
    list<tuple2<__ss_int, __ss_int> *>::for_in_loop __85;
    list<tuple2<__ss_int, __ss_int> *> *__82;
    __iter<tuple2<__ss_int, __ss_int> *> *__83;
    __ss_int __84, mex, mey, nx, ny, youx, youy;

    __78 = __77;
    mex = __78->__getfirst__();
    mey = __78->__getsecond__();
    __80 = __79;
    youx = __80->__getfirst__();
    youy = __80->__getsecond__();
    if (__NOT(depth)) {
        return ((double)(val((new tuple2<__ss_int, __ss_int>(2,mex,mey)), (new tuple2<__ss_int, __ss_int>(2,youx,youy)))));
    }
    you = (new tuple2<__ss_int, __ss_int>(2,youx,youy));

    FOR_IN(__81,near(mex, mey),82,84,85)
        __81 = __81;
        nx = __81->__getfirst__();
        ny = __81->__getsecond__();
        a->__getfast__(nx)->__setitem__(ny, True);
        v = (-negamax(you, (new tuple2<__ss_int, __ss_int>(2,nx,ny)), (depth-1), (-beta), (-alpha)));
        a->__getfast__(nx)->__setitem__(ny, False);
        if ((v>=beta)) {
            return v;
        }
        if ((v>alpha)) {
            alpha = v;
        }
    END_FOR

    return alpha;
}

list<tuple2<__ss_int, __ss_int> *> *alphabeta(tuple2<__ss_int, __ss_int> *me, tuple2<__ss_int, __ss_int> *you, double alpha) {
    /**
    gets moves from negamax by expanding out the first ply
    */
    tuple2<__ss_int, __ss_int> *__88, *pos;
    list<tuple2<__ss_int, __ss_int> *> *__89, *moves;
    double v;
    list<tuple2<__ss_int, __ss_int> *>::for_in_loop __92;
    list<__ss_bool> *__93, *__94;
    __iter<tuple2<__ss_int, __ss_int> *> *__90;
    __ss_int __91, x, y;

    moves = (new list<tuple2<__ss_int, __ss_int> *>());

    FOR_IN(__88,near(me->__getfirst__(), me->__getsecond__()),89,91,92)
        __88 = __88;
        x = __88->__getfirst__();
        y = __88->__getsecond__();
        pos = (new tuple2<__ss_int, __ss_int>(2,x,y));
        ASSERT(__NOT((a->__getfast__(x))->__getfast__(y)), 0);
        a->__getfast__(x)->__setitem__(y, True);
        v = (-negamax(you, pos, DEPTH, (-OO), (1-alpha)));
        a->__getfast__(x)->__setitem__(y, False);
        if ((v>alpha)) {
            alpha = v;
            moves = (new list<tuple2<__ss_int, __ss_int> *>());
        }
        if ((v==alpha)) {
            moves->append(pos);
        }
    END_FOR

    print2(NULL,0,2, const_8, ___box(alpha));
    return moves;
}

void __init() {
    const_0 = new str("");
    const_1 = __char_cache[76];;
    const_2 = __char_cache[83];;
    const_3 = new str("<%s@%d/%d (%d,%d) %s>");
    const_4 = new str("ongoing");
    const_5 = new str("tie");
    const_6 = new str("win");
    const_7 = new str("lose");
    const_8 = new str("hope for");
    const_9 = new str("<iii307s");
    const_10 = new str("<iii");
    const_11 = new str("<256s256s");
    const_12 = new str("inf");
    const_13 = new str("localhost");
    const_14 = new str("negamax-0.1");
    const_15 = new str("35fad903-2ed3-4c95-8e91-bae44dbc52c3");
    const_16 = new str("no moves");

    __name__ = new str("__main__");

    TCP_NODELAY = 1;
    STRUCT_DOWN_FRAME = const_9;
    STRUCT_UP_MOVE = const_10;
    STRUCT_UP_LOGIN = const_11;
    IPPROTO_TCP = 6;
    TCP_NODELAY = 1;
    TCP_QUICKACK = 12;
    __ss_SHUT_RDWR = 2;
    PORT = 12345;
    OO = __float(const_12);
    default_0 = NULL;
    default_1 = NULL;
    default_2 = const_0;
    default_3 = PORT;
    cl_TronClient = new class_("TronClient");
    TronClient::__static__();
    a = list_comp_1();
    default_4 = (-OO);
    if (True) {
        tron = (new TronClient(1));
        host = const_13;
        port = PORT;
        if ((len(__sys__::argv)>1)) {
            host = (__sys__::argv)->__getfast__(1);
            if ((len(__sys__::argv)>2)) {
                port = __int((__sys__::argv)->__getfast__(2));
            }
        }
        tron->start(const_14, const_15, host, port);

        while (__NOT(tron->ended())) {
            starttime = time();
            me = (new tuple2<__ss_int, __ss_int>(2,tron->x,tron->y));
            you = next(new list_comp_8());
            a = list_comp_9();
            moves = alphabeta(me, you, default_4);
            if (___bool(moves)) {
                __109 = choice(moves);
                tron->x = __109->__getfirst__();
                tron->y = __109->__getsecond__();
            }
            else {
                print2(NULL,0,1, const_16);
                tron->x = (tron->x+1);
            }
            print2(NULL,0,1, ___box((time()-starttime)));
        }
        print2(NULL,0,1, tron);
    }
}

} // module namespace

int main(int __ss_argc, char **__ss_argv) {
    __shedskin__::__init();
    __struct__::__init();
    __socket__::__init();
    __math__::__init();
    __time__::__init();
    __random__::__init();
    __sys__::__init(__ss_argc, __ss_argv);
    __shedskin__::__start(__negamax__::__init);
}
