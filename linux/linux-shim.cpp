extern "C" {
typedef signed long int __int64_t;
typedef unsigned long int __uint64_t;
typedef int int32_t;
typedef unsigned int uint32_t;

typedef char            tinyint;
typedef unsigned char   u_tinyint;
typedef unsigned char   u_char;
typedef unsigned short  u_short;
typedef unsigned int    u_int;
typedef unsigned long   u_long;
typedef long long       bigint;
typedef unsigned long long u_bigint;

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

typedef void ( *LoginReplyAddr)(long ret_code, char *ret_msg);
typedef void ( *ConnectedReplyAddr)(long host_type, long con_status);
typedef void ( *ApiOrderRequestFailedAddr)(tinyint action,
    SPApiOrder *order, long err_code, char *err_msg);
typedef void ( *ApiOrderReportAddr)(long rec_no, SPApiOrder *order);
typedef void ( *ApiOrderBeforeSendReportAddr)(SPApiOrder *order);
typedef void ( *AccountLoginReplyAddr)(char *accNo,
    long ret_code, char* ret_msg);
typedef void ( *AccountLogoutReplyAddr)(long ret_code, char* ret_msg);
typedef void ( *AccountInfoPushAddr)(SPApiAccInfo *acc_info);
typedef void ( *AccountPositionPushAddr)(SPApiPos *pos);
typedef void ( *UpdatedAccountPositionPushAddr)(SPApiPos *pos);
typedef void ( *UpdatedAccountBalancePushAddr)(SPApiAccBal *acc_bal);
typedef void ( *ApiTradeReportAddr)(long rec_no, SPApiTrade *trade);
typedef void ( *ApiPriceUpdateAddr)(SPApiPrice *price);
typedef void ( *ApiTickerUpdateAddr)(SPApiTicker *ticker);
typedef void ( *PswChangeReplyAddr)(long ret_code, char *ret_msg);
typedef void ( *ProductListByCodeReplyAddr)(char *inst_code,
    bool is_ready, char *ret_msg);
typedef void ( *InstrumentListReplyAddr)(bool is_ready,
    char *ret_msg);
typedef void ( *BusinessDateReplyAddr)(long business_date);
typedef void ( *ApiMMOrderBeforeSendReportAddr)
    (SPApiMMOrder *mm_order);
typedef void ( *ApiMMOrderRequestFailedAddr)(SPApiMMOrder *mm_order,
    long err_code, char *err_msg);
typedef void ( *ApiQuoteRequestReceivedAddr)(char *product_code,
    char buy_sell, long qty);


void  _Z24SPAPI_RegisterLoginReplyPFvlPcE(LoginReplyAddr addr);
void SPAPI_RegisterLoginReply(LoginReplyAddr addr){
  _Z24SPAPI_RegisterLoginReplyPFvlPcE(addr);
}

void _Z29SPAPI_RegisterConnectingReplyPFvllE(ConnectedReplyAddr addr);
void SPAPI_RegisterConnectingReply(ConnectedReplyAddr addr){
  _Z29SPAPI_RegisterConnectingReplyPFvllE(addr);
}

void _Z25SPAPI_RegisterOrderReportPFvlP10SPApiOrderE(ApiOrderReportAddr addr);
void SPAPI_RegisterOrderReport(ApiOrderReportAddr addr){
  _Z25SPAPI_RegisterOrderReportPFvlP10SPApiOrderE(addr);
}

void _Z32SPAPI_RegisterOrderRequestFailedPFvcP10SPApiOrderlPcE(ApiOrderRequestFailedAddr addr);
void SPAPI_RegisterOrderRequestFailed(ApiOrderRequestFailedAddr addr){
  _Z32SPAPI_RegisterOrderRequestFailedPFvcP10SPApiOrderlPcE(addr);
}

void _Z35SPAPI_RegisterOrderBeforeSendReportPFvP10SPApiOrderE(ApiOrderBeforeSendReportAddr addr);
void SPAPI_RegisterOrderBeforeSendReport(ApiOrderBeforeSendReportAddr addr){
  _Z35SPAPI_RegisterOrderBeforeSendReportPFvP10SPApiOrderE(addr);
}

void _Z31SPAPI_RegisterAccountLoginReplyPFvPclS_E(AccountLoginReplyAddr addr);
void SPAPI_RegisterAccountLoginReply(AccountLoginReplyAddr addr){
  _Z31SPAPI_RegisterAccountLoginReplyPFvPclS_E(addr);
}

void _Z32SPAPI_RegisterAccountLogoutReplyPFvlPcE(AccountLogoutReplyAddr addr);
void SPAPI_RegisterAccountLogoutReply(AccountLogoutReplyAddr addr){
  _Z32SPAPI_RegisterAccountLogoutReplyPFvlPcE(addr);
}

void _Z29SPAPI_RegisterAccountInfoPushPFvP12SPApiAccInfoE(AccountInfoPushAddr addr);
void SPAPI_RegisterAccountInfoPush(AccountInfoPushAddr addr){
  _Z29SPAPI_RegisterAccountInfoPushPFvP12SPApiAccInfoE(addr);
}

void SPAPI_RegisterAccountPositionPush(AccountPositionPushAddr addr){}
void
SPAPI_RegisterUpdatedAccountPositionPush(UpdatedAccountPositionPushAddr addr){}
void
SPAPI_RegisterUpdatedAccountBalancePush(UpdatedAccountBalancePushAddr addr){}
void SPAPI_RegisterTradeReport(ApiTradeReportAddr addr){}
void SPAPI_RegisterApiPriceUpdate(ApiPriceUpdateAddr addr){}
void SPAPI_RegisterTickerUpdate(ApiTickerUpdateAddr addr){}
void SPAPI_RegisterPswChangeReply(PswChangeReplyAddr addr){}
void SPAPI_RegisterProductListByCodeReply(ProductListByCodeReplyAddr addr){}
void SPAPI_RegisterInstrumentListReply(InstrumentListReplyAddr addr){}
void SPAPI_RegisterBusinessDateReply(BusinessDateReplyAddr addr){}
void SPAPI_RegisterMMOrderRequestFailed(ApiMMOrderRequestFailedAddr addr){}
void SPAPI_RegisterMMOrderBeforeSendReport(
    ApiMMOrderBeforeSendReportAddr addr){}
void SPAPI_RegisterQuoteRequestReceivedReport(
    ApiQuoteRequestReceivedAddr addr){}

int  SPAPI_Initialize(){}
void SPAPI_SetLoginInfo(char *host,
    int port, char *license, char *app_id, char *user_id, char *password){}
int  SPAPI_Login(){}
int  SPAPI_GetLoginStatus(char *user_id, short host_id){}
int  SPAPI_AddOrder(SPApiOrder *order){}
int SPAPI_AddInactiveOrder(SPApiOrder* order){}
int SPAPI_ChangeOrder(char *user_id,
    SPApiOrder* order, double org_price, long org_qty){}
int SPAPI_ChangeOrderBy(char *user_id,
    char *acc_no, long accOrderNo, double org_price,
    long org_qty, double newPrice, long newQty){}
int SPAPI_DeleteOrderBy(char *user_id,
    char *acc_no, long accOrderNo, char* productCode, char* clOrderId){}
int SPAPI_DeleteAllOrders(char *user_id, char *acc_no){}
int SPAPI_ActivateAllOrders(char *user_id, char *acc_no){}
int SPAPI_InactivateAllOrders(char *user_id, char *acc_no){}
int SPAPI_ActivateOrderBy(char *user_id, char *acc_no, long accOrderNo){}
int SPAPI_InactivateOrderBy(char *user_id, char *acc_no, long accOrderNo){}
int  SPAPI_GetOrderCount(char *user_id, char* acc_no){}
int  SPAPI_GetOrderByOrderNo(char *user_id, char *acc_no,
    long int_order_no, SPApiOrder *order){}
int  SPAPI_GetPosCount(char *user_id){}
int  SPAPI_GetPosByProduct(char *user_id, char *prod_code, SPApiPos *pos){}
void SPAPI_Uninitialize(){}
int SPAPI_Logout(char *user_id){}
int SPAPI_AccountLogin(char *user_id, char *acc_no){}
int SPAPI_AccountLogout(char *user_id, char *acc_no){}
int  SPAPI_GetTradeCount(char *user_id, char *acc_no){}
int SPAPI_SubscribePrice(char *user_id, char *prod_code, int mode){}
int SPAPI_SubscribeTicker(char *user_id, char *prod_code, int mode){}
int SPAPI_ChangePassword(char *user_id, char *old_password,
    char *new_password){}
int SPAPI_GetDllVersion(char *dll_ver_no, char *dll_rel_no, char *dll_suffix){}
int SPAPI_GetAccBalCount(char* user_id){}
int SPAPI_GetAccBalByCurrency(char *user_id, char *ccy, SPApiAccBal *acc_bal){}
int SPAPI_GetCcyRateByCcy(char *user_id, char *ccy, double *rate){}
int SPAPI_GetAccInfo(char *user_id, SPApiAccInfo *acc_info){}
int SPAPI_GetPriceByCode(char *user_id, char *prod_code, SPApiPrice *price){}
int SPAPI_SetApiLogPath(char *path){}

int SPAPI_LoadProductInfoListByCode(char *inst_code){}
int SPAPI_GetProductCount(){}
int SPAPI_GetProductByCode(char *prod_code, SPApiProduct *prod){}

int SPAPI_LoadInstrumentList(){}
int SPAPI_GetInstrumentCount(){}
int SPAPI_GetInstrumentByCode(char *inst_code, SPApiInstrument *inst){}
int SPAPI_SetLanguageId(int langid){}

int SPAPI_SendMarketMakingOrder(char *user_id, SPApiMMOrder *mm_order){}
int SPAPI_SubscribeQuoteRequest(char *user_id, char *prod_code, int mode){}
int SPAPI_SubscribeAllQuoteRequest(char *user_id, int mode){}

int SPAPI_GetAllTradesByArray(char *user_id, char *acc_no,
    SPApiTrade* apiTradeList){}
int SPAPI_GetOrdersByArray(char *user_id, char *acc_no,
    SPApiOrder* apiOrderList){}
int SPAPI_GetAllAccBalByArray(char *user_id, SPApiAccBal* apiAccBalList){}
int SPAPI_GetInstrumentByArray(SPApiInstrument* apiInstList){}
int SPAPI_GetProductByArray(SPApiProduct* apiProdList){}
}
