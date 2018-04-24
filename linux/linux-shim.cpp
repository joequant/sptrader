// Copyright (C) Bitquant Research Laboratories (Asia) Limited
// released under terms of the GPLv3+ License

const char *SP_SUFFIX = "20160718";

#include <cstddef>
#include <string.h>
#include <iostream>
#include <vector>
  template <typename T>
  class FStore {
    T _func;
  public:
    FStore() {
      _func = nullptr;
    }
    template <typename ...Types>
    void operator()(Types... args) {
      if (_func)
	_func(args...);
    }
    void set(T& f) {
      _func = f;
    }
  };

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

using STR4 = char[4];
using STR16 = char[16];
using STR40 = char[40];

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

using LoginReplyAddr = void(*)(long ret_code, char *ret_msg);
using ConnectedReplyAddr = void (*)(long host_type, long con_status);
using ApiOrderRequestFailedAddr = void (*)(tinyint action,
					   const SPApiOrder *order,
					   long err_code, char *err_msg);
using ApiOrderReportAddr = void (*)(long rec_no, const SPApiOrder *order);
using ApiOrderBeforeSendReportAddr = void (*)(const SPApiOrder *order);
using AccountLoginReplyAddr = void (*)(char *accNo,
    long ret_code, char*);
using AccountLogoutReplyAddr = void (*)(long ret_code, char* ret_msg);
using AccountInfoPushAddr = void (*)(const SPApiAccInfo *acc_info);
using AccountPositionPushAddr = void (*)(const SPApiPos *pos);
using UpdatedAccountPositionPushAddr = void (*)(const SPApiPos *pos);
using UpdatedAccountBalancePushAddr = void (*)(const SPApiAccBal *acc_bal);
using ApiTradeReportAddr = void (*)(long rec_no, const SPApiTrade *trade);
using ApiPriceUpdateAddr = void (*)(const SPApiPrice *price);
using ApiTickerUpdateAddr = void (*)(const SPApiTicker *ticker);
using PswChangeReplyAddr = void (*)(long ret_code, char *ret_msg);
using ProductListByCodeReplyAddr = void (*)(char *inst_code,
    bool is_ready, char *ret_msg);
using InstrumentListReplyAddr = void (*)(bool is_ready,
    char *ret_msg);
using BusinessDateReplyAddr = void (*)(long business_date);
using ApiMMOrderBeforeSendReportAddr = void (*)
    (SPApiMMOrder *mm_order);
using ApiMMOrderRequestFailedAddr = void (*)(SPApiMMOrder *mm_order,
    long err_code, char *err_msg);
using ApiQuoteRequestReceivedAddr = void (*)(char *product_code,
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

#define DECLARE_PROXY(X,Y) \
  static FStore<Y##Addr> _s_##Y ; void X(Y##Addr addr) { _s_##Y.set(addr); }
  
  DECLARE_PROXY(SPAPI_RegisterLoginReply,LoginReply);
  DECLARE_PROXY(SPAPI_RegisterConnectingReply,ConnectedReply);
  DECLARE_PROXY(SPAPI_RegisterOrderReport,ApiOrderReport);
  DECLARE_PROXY(SPAPI_RegisterOrderRequestFailed,ApiOrderRequestFailed);
  DECLARE_PROXY(SPAPI_RegisterOrderBeforeSendReport,ApiOrderBeforeSendReport);
  DECLARE_PROXY(SPAPI_RegisterAccountLoginReply,AccountLoginReply);
  DECLARE_PROXY(SPAPI_RegisterAccountLogoutReply,AccountLogoutReply);
  DECLARE_PROXY(SPAPI_RegisterAccountInfoPush,AccountInfoPush);
  DECLARE_PROXY(SPAPI_RegisterAccountPositionPush,AccountPositionPush);
  DECLARE_PROXY(SPAPI_RegisterUpdatedAccountPositionPush,
		UpdatedAccountPositionPush);
  DECLARE_PROXY(SPAPI_RegisterUpdatedAccountBalancePush,
		UpdatedAccountBalancePush);
  DECLARE_PROXY(SPAPI_RegisterTradeReport, ApiTradeReport);
  DECLARE_PROXY(SPAPI_RegisterApiPriceUpdate, ApiPriceUpdate);
  DECLARE_PROXY(SPAPI_RegisterTickerUpdate, ApiTickerUpdate);
  DECLARE_PROXY(SPAPI_RegisterPswChangeReply, PswChangeReply);
  DECLARE_PROXY(SPAPI_RegisterProductListByCodeReply,
		ProductListByCodeReply);
  DECLARE_PROXY(SPAPI_RegisterInstrumentListReply, InstrumentListReply);
  DECLARE_PROXY(SPAPI_RegisterBusinessDateReply, BusinessDateReply);
  DECLARE_PROXY(SPAPI_RegisterMMOrderRequestFailed,
		ApiMMOrderRequestFailed);
  DECLARE_PROXY(SPAPI_RegisterMMOrderBeforeSendReport,
		ApiMMOrderBeforeSendReport);
  DECLARE_PROXY(SPAPI_RegisterQuoteRequestReceivedReport,
		ApiQuoteRequestReceived);
  
  class ApiProxyWrapperReplyStatic: public ApiProxyWrapperReply {
public:
    ApiProxyWrapperReplyStatic(void){};
    ~ApiProxyWrapperReplyStatic(void){};
    virtual void OnTest() {};
    virtual void OnLoginReply(long ret_code,char *ret_msg) final {
      _s_LoginReply(ret_code, ret_msg);
    };
    virtual void OnConnectedReply(long host_type,long con_status) final {
      _s_ConnectedReply(host_type, con_status);
    };
    virtual void OnApiOrderRequestFailed(tinyint action,
					 const SPApiOrder *order,
					 long err_code,
					 char *err_msg) final {
      _s_ApiOrderRequestFailed(action, order, err_code, err_msg);
    };
    virtual void OnApiOrderReport(long rec_no, const SPApiOrder *order) final {
      _s_ApiOrderReport(rec_no, order);
    };
    virtual void OnApiOrderBeforeSendReport(const SPApiOrder *order) final {
      _s_ApiOrderBeforeSendReport(order);
    };
    virtual void OnAccountLoginReply(char *accNo, long ret_code,
				     char* ret_msg) final {
      _s_AccountLoginReply(accNo, ret_code, ret_msg);
    };
    virtual void OnAccountLogoutReply(long ret_code, char* ret_msg) final {
      _s_AccountLogoutReply(ret_code, ret_msg);
    };
    virtual void OnAccountInfoPush(const SPApiAccInfo *acc_info) final {
      _s_AccountInfoPush(acc_info);
    };
    virtual void OnAccountPositionPush(const SPApiPos *pos) final {
      _s_AccountPositionPush(pos);
    };
    virtual void OnUpdatedAccountPositionPush(const SPApiPos *pos) final {
      _s_UpdatedAccountPositionPush(pos);
    };
    virtual void OnUpdatedAccountBalancePush(const SPApiAccBal *acc_bal) final {
      _s_UpdatedAccountBalancePush(acc_bal);
    };
    virtual void OnApiTradeReport(long rec_no, const SPApiTrade *trade) final {
      _s_ApiTradeReport(rec_no, trade);
    };
    virtual void OnApiPriceUpdate(const SPApiPrice *price) final {
      _s_ApiPriceUpdate(price);
    };
    virtual void OnApiTickerUpdate(const SPApiTicker *ticker) final {
      _s_ApiTickerUpdate(ticker);
    };

    virtual void OnPswChangeReply(long ret_code, char *ret_msg) final {
      _s_PswChangeReply(ret_code, ret_msg);
    };
    virtual void OnProductListByCodeReply(char *inst_code,
					  bool is_ready, char *ret_msg) final {
      _s_ProductListByCodeReply(inst_code, is_ready, ret_msg);
    };
    virtual void OnInstrumentListReply(bool is_ready, char *ret_msg) final {
      _s_InstrumentListReply(is_ready, ret_msg);
    };
    virtual void OnBusinessDateReply(long business_date) final {
      _s_BusinessDateReply(business_date);
    };
    virtual void OnApiMMOrderBeforeSendReport(SPApiMMOrder *mm_order) final {
      _s_ApiMMOrderBeforeSendReport(mm_order);
    };
    virtual void OnApiMMOrderRequestFailed(SPApiMMOrder *mm_order, long err_code, char *err_msg) final {
	_s_ApiMMOrderRequestFailed(mm_order, err_code, err_msg);
    };
    virtual void OnApiQuoteRequestReceived(char *product_code, char buy_sell, long qty) final {
      _s_ApiQuoteRequestReceived(product_code, buy_sell, qty);
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

int  SPAPI_Initialize(){
  int retval = api_proxy_wrapper.SPAPI_Initialize();
  api_proxy_wrapper.SPAPI_RegisterApiProxyWrapperReply(&wrapper_reply);
  char dll_ver_no[64];
  char dll_rel_no[64];
  char dll_suffix[64];
  api_proxy_wrapper.SPAPI_GetDllVersion(dll_ver_no, dll_rel_no, dll_suffix);
  if (strcmp(dll_suffix, SP_SUFFIX)) {
    std::cerr << "Version mismatch: "
	      << dll_suffix
	      << " versus " << SP_SUFFIX
	      << std::endl;
	exit(1);
      }
  return retval;
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

  // declare function

auto  SPAPI_Login(){
  return api_proxy_wrapper.SPAPI_Login();
}
auto  SPAPI_GetLoginStatus(char *user_id, short host_id){
  return api_proxy_wrapper.SPAPI_GetLoginStatus(user_id, host_id);
}
auto  SPAPI_AddOrder(SPApiOrder *order){
  return api_proxy_wrapper.SPAPI_AddOrder(order);
}
auto SPAPI_AddInactiveOrder(SPApiOrder* order){
  return api_proxy_wrapper.SPAPI_AddInactiveOrder(order);
}
auto SPAPI_ChangeOrder(char *user_id,
    SPApiOrder* order, double org_price, long org_qty){
  return api_proxy_wrapper.SPAPI_ChangeOrder(user_id,
					     order, org_price, org_qty);
}
auto SPAPI_ChangeOrderBy(char *user_id,
    char *acc_no, long accOrderNo, double org_price,
    long org_qty, double newPrice, long newQty){
  return api_proxy_wrapper.SPAPI_ChangeOrderBy(user_id,
					       acc_no, accOrderNo, org_price,
					       org_qty, newPrice, newQty);
}
auto SPAPI_DeleteOrderBy(char *user_id,
    char *acc_no, long accOrderNo, char* productCode, char* clOrderId){
  return api_proxy_wrapper.SPAPI_DeleteOrderBy(user_id,
					       acc_no, accOrderNo,
					       productCode, clOrderId);
}
auto SPAPI_DeleteAllOrders(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_DeleteAllOrders(user_id, acc_no);
}
auto SPAPI_ActivateAllOrders(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_ActivateAllOrders(user_id, acc_no);
}
auto SPAPI_InactivateAllOrders(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_InactivateAllOrders(user_id, acc_no);
}
auto SPAPI_ActivateOrderBy(char *user_id, char *acc_no, long accOrderNo){
  return api_proxy_wrapper.SPAPI_ActivateOrderBy(user_id, acc_no, accOrderNo);
}
auto SPAPI_InactivateOrderBy(char *user_id, char *acc_no, long accOrderNo){
  return api_proxy_wrapper.SPAPI_InactivateOrderBy(user_id, acc_no, accOrderNo);
}
auto  SPAPI_GetOrderCount(char *user_id, char* acc_no){
  return api_proxy_wrapper.SPAPI_GetOrderCount(user_id, acc_no);
}
auto  SPAPI_GetOrderByOrderNo(char *user_id, char *acc_no,
    long int_order_no, SPApiOrder *order){
  return api_proxy_wrapper.SPAPI_GetOrderByOrderNo(user_id, acc_no,
						   int_order_no, order);
}
auto  SPAPI_GetPosCount(char *user_id){
  return api_proxy_wrapper.SPAPI_GetPosCount(user_id);
}
auto  SPAPI_GetPosByProduct(char *user_id, char *prod_code, SPApiPos *pos){
  return api_proxy_wrapper.SPAPI_GetPosByProduct(user_id, prod_code, pos);
}
auto SPAPI_Uninitialize(){
  return api_proxy_wrapper.SPAPI_Uninitialize();
}
auto SPAPI_Logout(char *user_id){
  return api_proxy_wrapper.SPAPI_Logout(user_id);
}
auto SPAPI_AccountLogin(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_AccountLogin(user_id, acc_no);
}
auto SPAPI_AccountLogout(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_AccountLogout(user_id, acc_no);
}
auto  SPAPI_GetTradeCount(char *user_id, char *acc_no){
  return api_proxy_wrapper.SPAPI_GetTradeCount(user_id, acc_no);
}
auto SPAPI_SubscribePrice(char *user_id, char *prod_code, int mode){
  return api_proxy_wrapper.SPAPI_SubscribePrice(user_id, prod_code, mode);
}
auto SPAPI_SubscribeTicker(char *user_id, char *prod_code, int mode){
  return api_proxy_wrapper.SPAPI_SubscribeTicker(user_id, prod_code, mode);
}
auto SPAPI_ChangePassword(char *user_id, char *old_password,
    char *new_password){
  return api_proxy_wrapper.SPAPI_ChangePassword(user_id, old_password,
						new_password);
}
auto SPAPI_GetDllVersion(char *dll_ver_no, char *dll_rel_no, char *dll_suffix){
  return api_proxy_wrapper.SPAPI_GetDllVersion(dll_ver_no, dll_rel_no, dll_suffix);
}
auto SPAPI_GetAccBalCount(char* user_id){
  return api_proxy_wrapper.SPAPI_GetAccBalCount(user_id);
}
auto SPAPI_GetAccBalByCurrency(char *user_id, char *ccy, SPApiAccBal *acc_bal){
  return api_proxy_wrapper.SPAPI_GetAccBalByCurrency(user_id, ccy, acc_bal);
}
auto SPAPI_GetCcyRateByCcy(char *user_id, char *ccy, double *rate){
  return api_proxy_wrapper.SPAPI_GetCcyRateByCcy(user_id, ccy, *rate);
}
auto SPAPI_GetAccInfo(char *user_id, SPApiAccInfo *acc_info){
  return api_proxy_wrapper.SPAPI_GetAccInfo(user_id, acc_info);
}
auto SPAPI_GetPriceByCode(char *user_id, char *prod_code, SPApiPrice *price){
  return api_proxy_wrapper.SPAPI_GetPriceByCode(user_id, prod_code, price);
}
auto SPAPI_SetApiLogPath(char *path){
  return api_proxy_wrapper.SPAPI_SetApiLogPath(path);
}

auto SPAPI_LoadProductInfoListByCode(char *inst_code){
  return api_proxy_wrapper.SPAPI_LoadProductInfoListByCode(inst_code);
}
auto SPAPI_GetProductCount(){
  return api_proxy_wrapper.SPAPI_GetProductCount();
}
auto SPAPI_GetProductByCode(char *prod_code, SPApiProduct *prod){
  return api_proxy_wrapper.SPAPI_GetProductByCode(prod_code, prod);
}

auto SPAPI_LoadInstrumentList(){
  return api_proxy_wrapper.SPAPI_LoadInstrumentList();
}
auto SPAPI_GetInstrumentCount(){
  return api_proxy_wrapper.SPAPI_GetInstrumentCount();
}
auto SPAPI_GetInstrumentByCode(char *inst_code, SPApiInstrument *inst){
  return api_proxy_wrapper.SPAPI_GetInstrumentByCode(inst_code, inst);
}
auto SPAPI_SetLanguageId(int langid){
  api_proxy_wrapper.SPAPI_SetLanguageId(langid);
}

auto SPAPI_SendMarketMakingOrder(char *user_id, SPApiMMOrder *mm_order){
  return api_proxy_wrapper.SPAPI_SendMarketMakingOrder(user_id, mm_order);
}
auto SPAPI_SubscribeQuoteRequest(char *user_id, char *prod_code, int mode){
  return api_proxy_wrapper.SPAPI_SubscribeQuoteRequest(user_id, prod_code,
						       mode);
}

auto SPAPI_SubscribeAllQuoteRequest(char *user_id, int mode){
  return api_proxy_wrapper.SPAPI_SubscribeAllQuoteRequest(user_id, mode);
}

auto SPAPI_GetAllTradesByArray(char *user_id, char *acc_no,
    SPApiTrade* apiTradeList){
  return api_proxy_wrapper.SPAPI_GetAllTradesByArray(user_id, acc_no,
						     apiTradeList);
}
auto SPAPI_GetOrdersByArray(char *user_id, char *acc_no,
    SPApiOrder* apiOrderList){
  return api_proxy_wrapper.SPAPI_GetOrdersByArray(user_id, acc_no,
						  apiOrderList);
}

auto SPAPI_GetAllAccBalByArray(char *user_id, SPApiAccBal* apiAccBalList){
  return api_proxy_wrapper.SPAPI_GetAllAccBalByArray(user_id,
						     apiAccBalList);
}

auto SPAPI_GetInstrumentByArray(SPApiInstrument* apiInstList){
  return api_proxy_wrapper.SPAPI_GetInstrumentByArray(apiInstList);
}

auto SPAPI_GetProductByArray(SPApiProduct* apiProdList){
  return api_proxy_wrapper.SPAPI_GetProductByArray(apiProdList);
}
}
