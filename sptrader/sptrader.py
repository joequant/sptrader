from cffi import FFI
import atexit
import os
location = os.path.dirname(os.path.realpath(__file__))
dll_location = os.path.join(location, "..", "dll")
ffi = FFI()
ffi.cdef("""
typedef signed long int __int64_t;
typedef unsigned long int __uint64_t;

typedef char            tinyint;
typedef unsigned char   u_tinyint;
typedef unsigned char   u_char;
typedef unsigned short  u_short;
typedef unsigned int    u_int;
typedef unsigned long   u_long;
typedef __int64_t          bigint;
typedef __uint64_t u_bigint;

typedef char STR4[4];
typedef char STR16[16];
typedef char STR40[40];

typedef struct
{
    int32_t Qty;     
    int32_t DepQty;  
    int32_t LongQty; 
    int32_t ShortQty;
    double TotalAmt; 
    double DepTotalAmt;
    double LongTotalAmt;
    double ShortTotalAmt;
	double PLBaseCcy;
	double PL;       
    double ExchangeRate; 
    STR16 AccNo;         
    STR16 ProdCode;      
    char LongShort;      
    tinyint DecInPrice;  
} SPApiPos;

typedef struct
{
    double Price;        
    double StopLevel;    
    double UpLevel;      
    double UpPrice;      
    double DownLevel;    
    double DownPrice;    
    bigint ExtOrderNo;   
    int32_t IntOrderNo;  
    int32_t Qty;         
    int32_t TradedQty;   
    int32_t TotalQty;    
    int32_t ValidTime;   
    int32_t SchedTime;   
    int32_t TimeStamp;   
    uint32_t OrderOptions;
    STR16 AccNo;          
    STR16 ProdCode;       
    STR16 Initiator;      
    STR16 Ref;            
    STR16 Ref2;           
    STR16 GatewayCode;    
    STR40 ClOrderId;      
    char BuySell;         
    char StopType;        
    char OpenClose;       
    tinyint CondType;     
    tinyint OrderType;    
    tinyint ValidType;    
    tinyint Status;       
    tinyint DecInPrice;   
	tinyint OrderAction;
	int32_t UpdateTime;
	int32_t UpdateSeqNo;
} SPApiOrder;

typedef struct
{
    bigint BidExtOrderNo; 
    bigint AskExtOrderNo; 
    long BidAccOrderNo;   
    long AskAccOrderNo;   
    double BidPrice;      
    double AskPrice;      
    long BidQty;          
    long AskQty;          
    long SpecTime;        
   	u_long OrderOptions;
    STR16 ProdCode;        
    STR16 AccNo;           
	STR40 ClOrderId;
    STR40 OrigClOrdId;
    tinyint OrderType;     
    tinyint ValidType;     
    tinyint DecInPrice;    
} SPApiMMOrder;

typedef struct
{
	int32_t RecNo;	
    double Price;       
    bigint TradeNo;      
    bigint ExtOrderNo;   
    int32_t IntOrderNo;  
    int32_t Qty;         
    int32_t TradeDate;   
    int32_t TradeTime;   
    STR16 AccNo;         
    STR16 ProdCode;      
    STR16 Initiator;     
    STR16 Ref;           
    STR16 Ref2;          
    STR16 GatewayCode;   
    STR40 ClOrderId;     
    char BuySell;        
    char OpenClose;      
    tinyint Status;      
    tinyint DecInPrice;  
	double OrderPrice;
	STR40 TradeRef;
	int32_t TotalQty;
	int32_t RemainingQty;
	int32_t TradedQty;
	double AvgTradedPrice;
} SPApiTrade;

typedef struct
{
    double Margin;	
    double ContractSize;
    STR16 MarketCode;
    STR16 InstCode;
    STR40 InstName;
    STR40 InstName1;
    STR40 InstName2;
    STR4 Ccy;	
    char DecInPrice;
    char InstType;
} SPApiInstrument;

typedef struct
{
   STR16 ProdCode;	
   char ProdType;	
   STR40 ProdName;	
   STR16 Underlying;	
   STR16 InstCode;	
   int32_t ExpiryDate;	
   char CallPut;	
   int32_t Strike;	
   int32_t LotSize;	
   STR40 ProdName1;	
   STR40 ProdName2;	
   char OptStyle;	
   int32_t TickSize;	
}SPApiProduct;

typedef struct
{
    double Bid[20];    
    int32_t BidQty[20];
    int32_t BidTicket[20];
    double Ask[20];    
    int32_t AskQty[20];
    int32_t AskTicket[20];
    double Last[20];
    int32_t LastQty[20]; 
    int32_t LastTime[20];
    double Equil;        
    double Open;         
    double High;         
    double Low;          
    double Close;        
    int32_t CloseDate;   
    double TurnoverVol;  
    double TurnoverAmt;  
    int32_t OpenInt;     
    STR16 ProdCode;      
    STR40 ProdName;      
    char DecInPrice;     
	int32_t ExStateNo;        
	int32_t TradeStateNo;     
	bool Suspend;             
	int32_t ExpiryYMD;        
 	int32_t ContractYMD;      
	int32_t Timestamp;
} SPApiPrice;

typedef struct
{
    double Price;         
    int32_t Qty;          
    int32_t TickerTime;   
    int32_t DealSrc;      
    STR16 ProdCode;       
    char DecInPrice;      
} SPApiTicker;

typedef struct
{
	double NAV;    
    double BuyingPower;
    double CashBal;    
	double MarginCall;
    double CommodityPL;   
    double LockupAmt;     
    double CreditLimit;   
    double MaxMargin;     
    double MaxLoanLimit;  
    double TradingLimit;  
    double RawMargin;     
    double IMargin;       
    double MMargin;       
    double TodayTrans;    
    double LoanLimit;     
    double TotalFee;      
    double LoanToMR;	  
    double LoanToMV;	  
    STR16 AccName;        
    STR4 BaseCcy;         
    STR16 MarginClass;    
    STR16 TradeClass;     
    STR16 ClientId;       
    STR16 AEId;           
    char AccType;         
    char CtrlLevel;       
    char Active;          
    char MarginPeriod;    
} SPApiAccInfo;

typedef struct
{
    double CashBf; 
    double TodayCash;
    double NotYetValue;
    double Unpresented;
    double TodayOut;   
    STR4 Ccy;          
} SPApiAccBal;

typedef struct
{
    STR4 Ccy;
    double Rate;
} SPApiCcyRate;

typedef void (__stdcall *LoginReplyAddr)(long ret_code, char* ret_msg);
typedef void (__stdcall *ConnectedReplyAddr)(long host_type, long con_status);
typedef void (__stdcall *ApiPriceUpdateAddr)(SPApiPrice *price);
typedef void (__stdcall *ApiTickerUpdateAddr)(SPApiTicker *ticker);
typedef void (__stdcall *AccountLoginReplyAddr)(char *accNo, long ret_code, char* ret_msg);
typedef void (__stdcall *AccountLogoutReplyAddr)(long ret_code, char *ret_msg);

int SPAPI_SetLanguageId(int langid);
int SPAPI_Initialize();
void SPAPI_SetLoginInfo(char *host, int port, char *license, char *app_id, char *user_id, char *password);
int SPAPI_Login();
int SPAPI_GetLoginStatus(char *user_id, short host_id);
int SPAPI_AddOrder(SPApiOrder *order);
int SPAPI_ChangeOrder(SPApiOrder *order, double org_price, long org_qty);
int SPAPI_GetOrderCount();
int SPAPI_GetOrder(int idx, SPApiOrder *order);
int SPAPI_DeleteOrder(SPApiOrder *order);

int SPAPI_GetPosCount();
int SPAPI_GetPos(int idx, SPApiPos *pos);
int SPAPI_GetPosByProduct(char *prod_code, SPApiPos *pos);

int SPAPI_GetTradeCount();
int SPAPI_GetTrade(int idx, SPApiTrade *trade);
int SPAPI_GetTradeByTradeNo(long int_order_no, bigint trade_no,
    SPApiTrade *trade);

int SPAPI_SubscribePrice(char *prod_code, int mode);
int SPAPI_GetPriceCourt();
int SPAPI_GetPrice(int idx, SPApiPrice *price);
int SPAPI_GetPriceByCode(char *prod_code, SPApiPrice *price);

int SPAPI_LoadInstrumentList();

int SPAPI_GetInstrumentCount();
int SPAPI_GetInstrument(int idx, SPApiInstrument *inst);
int SPAPI_GetInstrumentByCode(char *inst_code, SPApiInstrument *inst);

int SPAPI_GetProductCount();
int SPAPI_GetProduct(int idx, SPApiProduct *prod);
int SPAPI_GetProductByCode(char *inst_code, SPApiProduct *prod);

int SPAPI_GetAccBalCount();
int SPAPI_GetAccBal(int idx, SPApiAccBal *prod);
int SPAPI_GetAccBalByCurrency(char *inst_code, SPApiAccBal *prod);

int SPAPI_SubscribeTicker(char *prod_code, int mode);
int SPAPI_GetAccInfo(SPApiAccInfo *acc_info);
int SPAPI_Logout(char *user_id);

void SPAPI_RegisterLoginReply(LoginReplyAddr addr);
void SPAPI_RegisterApiPriceUpdate(ApiPriceUpdateAddr addr);
void SPAPI_RegisterTickerUpdate(ApiTickerUpdateAddr addr);
void SPAPI_RegisterAccountLoginReply(AccountLoginReplyAddr addr);
void SPAPI_RegisterAccountLogoutReply(AccountLogoutReplyAddr addr);
void SPAPI_Uninitialize();
""")
ffi.dlopen(os.path.join(dll_location, "libeay32.dll"))
ffi.dlopen(os.path.join(dll_location, "ssleay32.dll"))
sp = ffi.dlopen(os.path.join(dll_location, "spapidllm64.dll"))

# Remember to convert unicode strings to byte strings otherwise
# ctypes will assume that the characters are wchars and not
# ordinary characters

class SPTrader(object):
    ffi = ffi
    def __init__(self):
        sp.SPAPI_SetLanguageId(0)
        sp.SPAPI_Initialize()
        self.user = None
    def set_login_info(self,
                       host,
                       port,
                       license,
                       app_id,
                       user_id,
                       password):
        self.user = user_id.encode("utf-8")
        sp.SPAPI_SetLoginInfo(host.encode("utf-8"),
                              port,
                              license.encode("utf-8"),
                              app_id.encode("utf-8"),
                              user_id.encode("utf-8"),
                              password.encode("utf-8"))
    def login(self, callback=None):
        retval = sp.SPAPI_Login()
        if callback != None:
            sp.SPAPI_RegisterLoginReply(callback)
        return retval
    def get_login_status(self, status_id):
        if self.user == None:
            return -1
        return sp.SPAPI_GetLoginStatus(self.user, status_id)
    def logout(self):
        user = self.user
        if user != None:
            self.user = None
            return sp.SPAPI_Logout(user)

        
#def cleanup():
#    sp.SPAPI_Uninitialize()

#atexit.register(cleanup)
