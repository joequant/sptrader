#include <vector>
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
    const SPApiOrder *order, long err_code, char *err_msg);
typedef void ( *ApiOrderReportAddr)(long rec_no, const SPApiOrder *order);
typedef void ( *ApiOrderBeforeSendReportAddr)(const SPApiOrder *order);
typedef void ( *AccountLoginReplyAddr)(char *accNo,
    long ret_code, char* ret_msg);
typedef void ( *AccountLogoutReplyAddr)(long ret_code, char* ret_msg);
typedef void ( *AccountInfoPushAddr)(const SPApiAccInfo *acc_info);
typedef void ( *AccountPositionPushAddr)(const SPApiPos *pos);
typedef void ( *UpdatedAccountPositionPushAddr)(const SPApiPos *pos);
typedef void ( *UpdatedAccountBalancePushAddr)(const SPApiAccBal *acc_bal);
typedef void ( *ApiTradeReportAddr)(long rec_no, const SPApiTrade *trade);
typedef void ( *ApiPriceUpdateAddr)(const SPApiPrice *price);
typedef void ( *ApiTickerUpdateAddr)(const SPApiTicker *ticker);
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

using namespace std;

class ApiProxyWrapperReply {
public:
	ApiProxyWrapperReply(void){};
	~ApiProxyWrapperReply(void){};
	virtual void OnTest() = 0;
	virtual void OnLoginReply(long ret_code,char *ret_msg) = 0;
	virtual void OnConnectedReply(long host_type,long con_status) = 0;
	virtual void OnApiOrderRequestFailed(tinyint action, const SPApiOrder *order, long err_code, char *err_msg) = 0;
	virtual void OnApiOrderReport(long rec_no, const SPApiOrder *order) = 0;
	virtual void OnApiOrderBeforeSendReport(const SPApiOrder *order) = 0;
	virtual void OnAccountLoginReply(char *accNo, long ret_code, char* ret_msg) = 0;
	virtual void OnAccountLogoutReply(long ret_code, char* ret_msg) = 0;
	virtual void OnAccountInfoPush(const SPApiAccInfo *acc_info) = 0;
	virtual void OnAccountPositionPush(const SPApiPos *pos) = 0;
	virtual void OnUpdatedAccountPositionPush(const SPApiPos *pos) = 0;
	virtual void OnUpdatedAccountBalancePush(const SPApiAccBal *acc_bal) = 0;
	virtual void OnApiTradeReport(long rec_no, const SPApiTrade *trade) = 0;
	virtual void OnApiPriceUpdate(const SPApiPrice *price) = 0;
	virtual void OnApiTickerUpdate(const SPApiTicker *ticker) = 0;
	virtual void OnPswChangeReply(long ret_code, char *ret_msg) = 0;
	virtual void OnProductListByCodeReply(char *inst_code, bool is_ready, char *ret_msg) = 0;
	virtual void OnInstrumentListReply(bool is_ready, char *ret_msg) = 0;
	virtual void OnBusinessDateReply(long business_date) = 0;
	virtual void OnApiMMOrderBeforeSendReport(SPApiMMOrder *mm_order) = 0;
	virtual void OnApiMMOrderRequestFailed(SPApiMMOrder *mm_order, long err_code, char *err_msg) = 0;
	virtual void OnApiQuoteRequestReceived(char *product_code, char buy_sell, long qty) = 0;
};

  class ApiProxyWrapperReplyStatic: public ApiProxyWrapperReply {
public:
	ApiProxyWrapperReplyStatic(void){};
	~ApiProxyWrapperReplyStatic(void){};
    static LoginReplyAddr _login_reply;
    virtual void OnTest() {};
    virtual void OnLoginReply(long ret_code,char *ret_msg) {
      if (_login_reply)
	_login_reply(ret_code, ret_msg);
    }
    static ConnectedReplyAddr _connected_reply;
    virtual void OnConnectedReply(long host_type,long con_status) {
      if (_connected_reply)
	_connected_reply(host_type, con_status);
    };
    static ApiOrderRequestFailedAddr _api_order_request_failed;
    virtual void OnApiOrderRequestFailed(tinyint action,
					 const SPApiOrder *order,
					 long err_code,
					 char *err_msg) {
      if (_api_order_request_failed)
	_api_order_request_failed(action, order, err_code, err_msg);
    };
    static ApiOrderReportAddr _api_order_report;
    virtual void OnApiOrderReport(long rec_no, const SPApiOrder *order) {
      if (_api_order_report)
	_api_order_report(rec_no, order);
    };
    static ApiOrderBeforeSendReportAddr _api_order_before_send_report;
    virtual void OnApiOrderBeforeSendReport(const SPApiOrder *order) {
      if (_api_order_before_send_report)
	_api_order_before_send_report(order);
    };
    static AccountLoginReplyAddr _account_login_reply;
    virtual void OnAccountLoginReply(char *accNo, long ret_code,
				     char* ret_msg) {
      if (_account_login_reply)
	_account_login_reply(accNo, ret_code, ret_msg);
    };
    static AccountLogoutReplyAddr _account_logout_reply;
    virtual void OnAccountLogoutReply(long ret_code, char* ret_msg) {
      if (_account_logout_reply)
	_account_logout_reply(ret_code, ret_msg);
    };
    static AccountInfoPushAddr _account_info_push;
    virtual void OnAccountInfoPush(const SPApiAccInfo *acc_info) {
      if (_account_info_push)
	_account_info_push(acc_info);
    };
    static AccountPositionPushAddr _account_position_push;
    virtual void OnAccountPositionPush(const SPApiPos *pos) {
      if (_account_position_push)
	_account_position_push(pos);
    };
    static UpdatedAccountPositionPushAddr _updated_account_position_push;
    virtual void OnUpdatedAccountPositionPush(const SPApiPos *pos) {
      if (_updated_account_position_push)
	_updated_account_position_push(pos);
    };
    static UpdatedAccountBalancePushAddr _updated_account_balance_push;
    virtual void OnUpdatedAccountBalancePush(const SPApiAccBal *acc_bal) {
      if (_updated_account_balance_push)
      _updated_account_balance_push(acc_bal);
    };
    static ApiTradeReportAddr _api_trade_report;
    virtual void OnApiTradeReport(long rec_no, const SPApiTrade *trade) {
      if (_api_trade_report)
	_api_trade_report(rec_no, trade);
    };
    static ApiPriceUpdateAddr _api_price_update;
    virtual void OnApiPriceUpdate(const SPApiPrice *price) {
      if (_api_price_update)
	_api_price_update(price);
    };
    static ApiTickerUpdateAddr _api_ticker_update;
    virtual void OnApiTickerUpdate(const SPApiTicker *ticker) {
      if (_api_ticker_update)
	_api_ticker_update(ticker);
    };
    static PswChangeReplyAddr _psw_change_reply;
    virtual void OnPswChangeReply(long ret_code, char *ret_msg) {
      if (_psw_change_reply)
	_psw_change_reply(ret_code, ret_msg);
    };
    static ProductListByCodeReplyAddr _product_list_by_code_reply;
    virtual void OnProductListByCodeReply(char *inst_code,
					  bool is_ready, char *ret_msg) {
      if (_product_list_by_code_reply)
	_product_list_by_code_reply(inst_code, is_ready, ret_msg);
    };
    static InstrumentListReplyAddr _instrument_list_reply;
    virtual void OnInstrumentListReply(bool is_ready, char *ret_msg) {
      if (_instrument_list_reply)
	_instrument_list_reply(is_ready, ret_msg);
    };
    static BusinessDateReplyAddr _business_date_reply;
    virtual void OnBusinessDateReply(long business_date) {
      if (_business_date_reply)
	_business_date_reply(business_date);
    };
    static ApiMMOrderBeforeSendReportAddr _api_mm_order_before_send_report;
    virtual void OnApiMMOrderBeforeSendReport(SPApiMMOrder *mm_order) {
      if (_api_mm_order_before_send_report)
	_api_mm_order_before_send_report(mm_order);
    };
    static ApiMMOrderRequestFailedAddr _api_mm_order_request_failed;
    virtual void OnApiMMOrderRequestFailed(SPApiMMOrder *mm_order, long err_code, char *err_msg) {
      if (_api_mm_order_request_failed)
	_api_mm_order_request_failed(mm_order, err_code, err_msg);
    };
    static ApiQuoteRequestReceivedAddr _api_quote_request_received;
    virtual void OnApiQuoteRequestReceived(char *product_code, char buy_sell, long qty) {
      if (_api_quote_request_received)
	_api_quote_request_received(product_code, buy_sell, qty);
    };
};

  
  static ApiProxyWrapperReplyStatic wrapper_reply;  
class ApiProxyWrapper {
public:
	ApiProxyWrapper(void);
	~ApiProxyWrapper(void);

	void SPAPI_RegisterApiProxyWrapperReply(ApiProxyWrapperReply* apiProxyWrapperReply);
	int SPAPI_Initialize();
	void SPAPI_SetLoginInfo(char *host, int port, char *license, char *app_id, char *user_id, char *password);
	int SPAPI_Login();
	int SPAPI_GetLoginStatus(char *user_id, short host_id);
	int SPAPI_AddOrder(SPApiOrder *order);
	int SPAPI_AddInactiveOrder(SPApiOrder* order);
	int SPAPI_ChangeOrder(char *user_id, SPApiOrder* order, double org_price, long org_qty);
	int SPAPI_ChangeOrderBy(char *user_id, char *acc_no, long accOrderNo, double org_price, long org_qty, double newPrice, long newQty);
	int SPAPI_DeleteOrderBy(char *user_id, char *acc_no, long accOrderNo, char* productCode, char* clOrderId);
	int SPAPI_DeleteAllOrders(char *user_id, char *acc_no);
	int SPAPI_ActivateAllOrders(char *user_id, char *acc_no);
	int SPAPI_InactivateAllOrders(char *user_id, char *acc_no);
	int SPAPI_ActivateOrderBy(char *user_id, char *acc_no, long accOrderNo);
	int SPAPI_InactivateOrderBy(char *user_id, char *acc_no, long accOrderNo);
	int SPAPI_GetOrderCount(char *user_id, char* acc_no);
	int SPAPI_GetOrderByOrderNo(char *user_id, char *acc_no, long int_order_no, SPApiOrder *order);
	int SPAPI_GetActiveOrders(char *user_id, char *acc_no, vector<SPApiOrder>& apiOrderList);
	int SPAPI_GetPosCount(char *user_id);
	int SPAPI_GetPosByProduct(char *user_id, char *prod_code, SPApiPos *pos);
	void SPAPI_Uninitialize();
	int SPAPI_Logout(char *user_id);
	int SPAPI_AccountLogin(char *user_id, char *acc_no);
	int SPAPI_AccountLogout(char *user_id, char *acc_no);
	int SPAPI_GetTradeCount(char *user_id, char *acc_no);
	int SPAPI_GetAllTrades(char *user_id, char *acc_no, vector<SPApiTrade>& apiTradeList);
	int SPAPI_SubscribePrice(char *user_id, char *prod_code, int mode);
	int SPAPI_SubscribeTicker(char *user_id, char *prod_code, int mode);
	int SPAPI_ChangePassword(char *user_id, char *old_password, char *new_password);
	int SPAPI_GetDllVersion(char *dll_ver_no, char *dll_rel_no, char *dll_suffix);
	int SPAPI_GetAccBalCount(char* user_id);
	int SPAPI_GetAccBalByCurrency(char *user_id, char *ccy, SPApiAccBal *acc_bal);
	int SPAPI_GetAllAccBal(char *user_id, vector<SPApiAccBal>& apiAccBalList);
	int SPAPI_GetCcyRateByCcy(char *user_id, char *ccy, double &rate);
	int SPAPI_GetAccInfo(char *user_id, SPApiAccInfo *acc_info);
	int SPAPI_GetPriceByCode(char *user_id, char *prod_code, SPApiPrice *price);
	int SPAPI_SetApiLogPath(char *path);
	int SPAPI_LoadProductInfoListByCode(char *inst_code);
	int SPAPI_GetProductCount();
	int SPAPI_GetProduct(vector<SPApiProduct>& apiProdList);
	int SPAPI_GetProductByCode(char *prod_code, SPApiProduct *prod);
	int SPAPI_LoadInstrumentList();
	int SPAPI_GetInstrumentCount();
	int SPAPI_GetInstrument(vector<SPApiInstrument>& apiInstList);
	int SPAPI_GetInstrumentByCode(char *inst_code, SPApiInstrument *inst);
	void SPAPI_SetLanguageId(int langid);
	int SPAPI_SendMarketMakingOrder(char *user_id, SPApiMMOrder *mm_order);
	int SPAPI_SubscribeQuoteRequest(char *user_id, char *prod_code, int mode);
	int SPAPI_SubscribeAllQuoteRequest(char *user_id, int mode);
    int SPAPI_GetAllAccBalByArray(char *acc_no, SPApiAccBal* apiAccBalList);
    int SPAPI_GetOrdersByArray(char* userId, char* acc_no, SPApiOrder* apiOrderList);
    int SPAPI_GetAllTradesByArray(char* userId, char* acc_no, SPApiTrade* apiTradeList);
    int SPAPI_GetInstrumentByArray(SPApiInstrument* apiInstList);
    int SPAPI_GetProductByArray(SPApiProduct* apiProdList);
    
private:

};

static ApiProxyWrapper api_proxy_wrapper;
  ApiProxyWrapper::ApiProxyWrapper() {
    SPAPI_RegisterApiProxyWrapperReply(&wrapper_reply);
  }
  ApiProxyWrapper::~ApiProxyWrapper() {}


void SPAPI_RegisterLoginReply(LoginReplyAddr addr){
  wrapper_reply._login_reply = addr;
}

void SPAPI_RegisterConnectingReply(ConnectedReplyAddr addr){
  wrapper_reply._connected_reply = addr;
}

void SPAPI_RegisterOrderReport(ApiOrderReportAddr addr){
  wrapper_reply._api_order_report = addr;
}

void SPAPI_RegisterOrderRequestFailed(ApiOrderRequestFailedAddr addr){
  wrapper_reply._api_order_request_failed = addr;
}

void SPAPI_RegisterOrderBeforeSendReport(ApiOrderBeforeSendReportAddr addr){
  wrapper_reply._api_order_before_send_report = addr;
}

void SPAPI_RegisterAccountLoginReply(AccountLoginReplyAddr addr){
  wrapper_reply._account_login_reply = addr;
}

void SPAPI_RegisterAccountLogoutReply(AccountLogoutReplyAddr addr){
  wrapper_reply._account_logout_reply = addr;
}

void SPAPI_RegisterAccountInfoPush(AccountInfoPushAddr addr){
  wrapper_reply._account_info_push = addr;
}

void SPAPI_RegisterAccountPositionPush(AccountPositionPushAddr addr){
  wrapper_reply._account_position_push = addr;
}
void
SPAPI_RegisterUpdatedAccountPositionPush(UpdatedAccountPositionPushAddr addr){
  wrapper_reply._updated_account_position_push = addr;
}
void
SPAPI_RegisterUpdatedAccountBalancePush(UpdatedAccountBalancePushAddr addr){
  wrapper_reply._updated_account_balance_push = addr;
}
void SPAPI_RegisterTradeReport(ApiTradeReportAddr addr){
  wrapper_reply._api_trade_report = addr;
}
void SPAPI_RegisterApiPriceUpdate(ApiPriceUpdateAddr addr){
  wrapper_reply._api_price_update = addr;
}
void SPAPI_RegisterTickerUpdate(ApiTickerUpdateAddr addr){
  wrapper_reply._api_ticker_update = addr;
}
void SPAPI_RegisterPswChangeReply(PswChangeReplyAddr addr){
  wrapper_reply._psw_change_reply = addr;
}
void SPAPI_RegisterProductListByCodeReply(ProductListByCodeReplyAddr addr){
  wrapper_reply._product_list_by_code_reply = addr;
}
void SPAPI_RegisterInstrumentListReply(InstrumentListReplyAddr addr){
  wrapper_reply._instrument_list_reply = addr;
}
void SPAPI_RegisterBusinessDateReply(BusinessDateReplyAddr addr){
  wrapper_reply._business_date_reply = addr;
}
void SPAPI_RegisterMMOrderRequestFailed(ApiMMOrderRequestFailedAddr addr){
  wrapper_reply._api_mm_order_request_failed = addr;
}
void SPAPI_RegisterMMOrderBeforeSendReport(
    ApiMMOrderBeforeSendReportAddr addr){
  wrapper_reply._api_mm_order_before_send_report = addr;
}
void SPAPI_RegisterQuoteRequestReceivedReport(
    ApiQuoteRequestReceivedAddr addr){
  wrapper_reply._api_quote_request_received = addr;
}

int  SPAPI_Initialize(){
  return api_proxy_wrapper.SPAPI_Initialize();
}
void SPAPI_SetLoginInfo(char *host,
    int port, char *license, char *app_id, char *user_id, char *password){
  return api_proxy_wrapper.SPAPI_SetLoginInfo(host,
					      port,
					      license,
					      app_id,
					      user_id,
					      password);
}
int  SPAPI_Login(){
  return api_proxy_wrapper.SPAPI_Login();
}
int  SPAPI_GetLoginStatus(char *user_id, short host_id){
  return api_proxy_wrapper.SPAPI_GetLoginStatus(user_id, host_id);
}
int  SPAPI_AddOrder(SPApiOrder *order){
  return api_proxy_wrapper.SPAPI_AddOrder(order);
}
int SPAPI_AddInactiveOrder(SPApiOrder* order){
  return api_proxy_wrapper.SPAPI_AddInactiveOrder(order);
}
int SPAPI_ChangeOrder(char *user_id,
    SPApiOrder* order, double org_price, long org_qty){
  return api_proxy_wrapper.SPAPI_ChangeOrder(user_id,
					     order, org_price, org_qty);
}
int SPAPI_ChangeOrderBy(char *user_id,
    char *acc_no, long accOrderNo, double org_price,
    long org_qty, double newPrice, long newQty){
  return api_proxy_wrapper.SPAPI_ChangeOrderBy(user_id,
					       acc_no, accOrderNo, org_price,
					       org_qty, newPrice, newQty);
}
int SPAPI_DeleteOrderBy(char *user_id,
    char *acc_no, long accOrderNo, char* productCode, char* clOrderId){
  return api_proxy_wrapper.SPAPI_DeleteOrderBy(user_id,
					       acc_no, accOrderNo,
					       productCode, clOrderId);
}
int SPAPI_DeleteAllOrders(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_DeleteAllOrders(user_id, acc_no);
}
int SPAPI_ActivateAllOrders(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_ActivateAllOrders(user_id, acc_no);
}
int SPAPI_InactivateAllOrders(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_InactivateAllOrders(user_id, acc_no);
}
int SPAPI_ActivateOrderBy(char *user_id, char *acc_no, long accOrderNo){
  return api_proxy_wrapper.SPAPI_ActivateOrderBy(user_id, acc_no, accOrderNo);
}
int SPAPI_InactivateOrderBy(char *user_id, char *acc_no, long accOrderNo){
  return api_proxy_wrapper.SPAPI_InactivateOrderBy(user_id, acc_no, accOrderNo);
}
int  SPAPI_GetOrderCount(char *user_id, char* acc_no){
  return api_proxy_wrapper.SPAPI_GetOrderCount(user_id, acc_no);
}
int  SPAPI_GetOrderByOrderNo(char *user_id, char *acc_no,
    long int_order_no, SPApiOrder *order){
  return api_proxy_wrapper.SPAPI_GetOrderByOrderNo(user_id, acc_no,
						   int_order_no, order);
}
int  SPAPI_GetPosCount(char *user_id){
  return api_proxy_wrapper.SPAPI_GetPosCount(user_id);
}
int  SPAPI_GetPosByProduct(char *user_id, char *prod_code, SPApiPos *pos){
  return api_proxy_wrapper.SPAPI_GetPosByProduct(user_id, prod_code, pos);
}
void SPAPI_Uninitialize(){
  return api_proxy_wrapper.SPAPI_Uninitialize();
}
int SPAPI_Logout(char *user_id){
  return api_proxy_wrapper.SPAPI_Logout(user_id);
}
int SPAPI_AccountLogin(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_AccountLogin(user_id, acc_no);
}
int SPAPI_AccountLogout(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_AccountLogout(user_id, acc_no);
}
int  SPAPI_GetTradeCount(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_GetTradeCount(user_id, acc_no);
}
int SPAPI_SubscribePrice(char *user_id, char *prod_code, int mode){
  return api_proxy_wrapper.SPAPI_SubscribePrice(user_id, prod_code, mode);
}
int SPAPI_SubscribeTicker(char *user_id, char *prod_code, int mode){
  return api_proxy_wrapper.SPAPI_SubscribeTicker(user_id, prod_code, mode);
}
int SPAPI_ChangePassword(char *user_id, char *old_password,
    char *new_password){
  return api_proxy_wrapper.SPAPI_ChangePassword(user_id, old_password,
						new_password);
}
int SPAPI_GetDllVersion(char *dll_ver_no, char *dll_rel_no, char *dll_suffix){
  return api_proxy_wrapper.SPAPI_GetDllVersion(dll_ver_no, dll_rel_no, dll_suffix);
}
int SPAPI_GetAccBalCount(char* user_id){
  return api_proxy_wrapper.SPAPI_GetAccBalCount(user_id);
}
int SPAPI_GetAccBalByCurrency(char *user_id, char *ccy, SPApiAccBal *acc_bal){
  return api_proxy_wrapper.SPAPI_GetAccBalByCurrency(user_id, ccy, acc_bal);
}
int SPAPI_GetCcyRateByCcy(char *user_id, char *ccy, double *rate){
  return api_proxy_wrapper.SPAPI_GetCcyRateByCcy(user_id, ccy, *rate);
}
int SPAPI_GetAccInfo(char *user_id, SPApiAccInfo *acc_info){
  return api_proxy_wrapper.SPAPI_GetAccInfo(user_id, acc_info);
}
int SPAPI_GetPriceByCode(char *user_id, char *prod_code, SPApiPrice *price){
  return api_proxy_wrapper.SPAPI_GetPriceByCode(user_id, prod_code, price);
}
int SPAPI_SetApiLogPath(char *path){
  return api_proxy_wrapper.SPAPI_SetApiLogPath(path);
}

int SPAPI_LoadProductInfoListByCode(char *inst_code){
  return api_proxy_wrapper.SPAPI_LoadProductInfoListByCode(inst_code);
}
int SPAPI_GetProductCount(){
  return api_proxy_wrapper.SPAPI_GetProductCount();
}
int SPAPI_GetProductByCode(char *prod_code, SPApiProduct *prod){
  return api_proxy_wrapper.SPAPI_GetProductByCode(prod_code, prod);
}

int SPAPI_LoadInstrumentList(){
  return api_proxy_wrapper.SPAPI_LoadInstrumentList();
}
int SPAPI_GetInstrumentCount(){
  return api_proxy_wrapper.SPAPI_GetInstrumentCount();
}
int SPAPI_GetInstrumentByCode(char *inst_code, SPApiInstrument *inst){
  return api_proxy_wrapper.SPAPI_GetInstrumentByCode(inst_code, inst);
}
int SPAPI_SetLanguageId(int langid){
  api_proxy_wrapper.SPAPI_SetLanguageId(langid);
}

int SPAPI_SendMarketMakingOrder(char *user_id, SPApiMMOrder *mm_order){
  return api_proxy_wrapper.SPAPI_SendMarketMakingOrder(user_id, mm_order);
}
int SPAPI_SubscribeQuoteRequest(char *user_id, char *prod_code, int mode){
  return api_proxy_wrapper.SPAPI_SubscribeQuoteRequest(user_id, prod_code,
						       mode);
}
int SPAPI_SubscribeAllQuoteRequest(char *user_id, int mode){
  return api_proxy_wrapper.SPAPI_SubscribeAllQuoteRequest(user_id, mode);
}

int SPAPI_GetAllTradesByArray(char *user_id, char *acc_no,
    SPApiTrade* apiTradeList){
  return api_proxy_wrapper.SPAPI_GetAllTradesByArray(user_id, acc_no,
						     apiTradeList);
}
int SPAPI_GetOrdersByArray(char *user_id, char *acc_no,
    SPApiOrder* apiOrderList){
  return api_proxy_wrapper.SPAPI_GetOrdersByArray(user_id, acc_no,
						  apiOrderList);
}
int SPAPI_GetAllAccBalByArray(char *user_id, SPApiAccBal* apiAccBalList){
  return api_proxy_wrapper.SPAPI_GetAllAccBalByArray(user_id,
						     apiAccBalList);
}
int SPAPI_GetInstrumentByArray(SPApiInstrument* apiInstList){
  return api_proxy_wrapper.SPAPI_GetInstrumentByArray(apiInstList);
}
int SPAPI_GetProductByArray(SPApiProduct* apiProdList){
  return api_proxy_wrapper.SPAPI_GetProductByArray(apiProdList);
}

}
  LoginReplyAddr ApiProxyWrapperReplyStatic::_login_reply ;
  ConnectedReplyAddr ApiProxyWrapperReplyStatic::_connected_reply ;
  ApiOrderRequestFailedAddr ApiProxyWrapperReplyStatic::_api_order_request_failed ;
  ApiOrderReportAddr ApiProxyWrapperReplyStatic::_api_order_report ;
  ApiOrderBeforeSendReportAddr ApiProxyWrapperReplyStatic::_api_order_before_send_report ;
  AccountLoginReplyAddr ApiProxyWrapperReplyStatic::_account_login_reply ;
  AccountLogoutReplyAddr ApiProxyWrapperReplyStatic::_account_logout_reply ;
  AccountInfoPushAddr ApiProxyWrapperReplyStatic::_account_info_push ;
  AccountPositionPushAddr ApiProxyWrapperReplyStatic::_account_position_push ;
  UpdatedAccountPositionPushAddr ApiProxyWrapperReplyStatic::_updated_account_position_push ;
  UpdatedAccountBalancePushAddr ApiProxyWrapperReplyStatic::_updated_account_balance_push ;
  ApiTradeReportAddr ApiProxyWrapperReplyStatic::_api_trade_report ;
  ApiPriceUpdateAddr ApiProxyWrapperReplyStatic::_api_price_update ;
  ApiTickerUpdateAddr ApiProxyWrapperReplyStatic::_api_ticker_update ;
  PswChangeReplyAddr ApiProxyWrapperReplyStatic::_psw_change_reply ;
  ProductListByCodeReplyAddr ApiProxyWrapperReplyStatic::_product_list_by_code_reply ;
  InstrumentListReplyAddr ApiProxyWrapperReplyStatic::_instrument_list_reply ;
  BusinessDateReplyAddr ApiProxyWrapperReplyStatic::_business_date_reply ;
  ApiMMOrderBeforeSendReportAddr ApiProxyWrapperReplyStatic::_api_mm_order_before_send_report ;
  ApiMMOrderRequestFailedAddr ApiProxyWrapperReplyStatic::_api_mm_order_request_failed ;
  ApiQuoteRequestReceivedAddr ApiProxyWrapperReplyStatic::_api_quote_request_received ;

