// Copyright (C) Bitquant Research Laboratories (Asia) Limited
// released under terms of the Simplified BSD License

const char *SP_SUFFIX = "20161214";

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
	int32_t Qty;                    //上日仓位
	int32_t DepQty;                 //存储仓位
	int32_t LongQty;                //今日长仓
    int32_t ShortQty;               //今日短仓
    double TotalAmt;             //上日成交
    double DepTotalAmt;          //上日持仓总数(数量*价格)
    double LongTotalAmt;         //今日长仓总数(数量*价格)
    double ShortTotalAmt;        //今日短仓总数(数量*价格)
    double PLBaseCcy;            //盈亏(基本货币)
    double PL;                   //盈亏
    double ExchangeRate;         //汇率
    STR16 AccNo;                 //用户
    STR16 ProdCode;              //合约代码
    char LongShort;              //上日持仓买卖方向
    tinyint DecInPrice;          //小数点
} SPApiPos;

typedef struct
{
    double Price;              //价格
    double StopLevel;          //止损价格
    double UpLevel;            //上限水平
    double UpPrice;            //上限价格
    double DownLevel;          //下限水平
    double DownPrice;          //下限价格
    bigint ExtOrderNo;         //外部指示
	int32_t IntOrderNo;           //用户订单编号
	int32_t Qty;                  //剩余数量
	int32_t TradedQty;            //已成交数量
	int32_t TotalQty;             //全部数量
	int32_t ValidTime;            //有效时间
	int32_t SchedTime;            //预订发送时间
    int32_t TimeStamp;            //服务器接收订单时间
    uint32_t OrderOptions;
    STR16 AccNo;               //用户帐号
    STR16 ProdCode;            //合约代号
    STR16 Initiator;           //下单用户
    STR16 Ref;                 //参考
    STR16 Ref2;                //参考2
    STR16 GatewayCode;         //网关
    STR40 ClOrderId;           //用户自定义指令代号
    char BuySell;              //买卖方向
    char StopType;             //止损类型
    char OpenClose;            //开平仓
    tinyint CondType;          //订单条件类型
    tinyint OrderType;         //订单类型
    tinyint ValidType;         //订单有效类型
    tinyint Status;            //状态
    tinyint DecInPrice;        //合约小数位
	tinyint OrderAction;
	int32_t UpdateTime;
	int32_t UpdateSeqNo;
} SPApiOrder;

typedef struct
{
    int32_t RecNo;
    double Price;              //成交价格
    bigint TradeNo;            //成交编号
    bigint ExtOrderNo;         //外部指示
	int32_t IntOrderNo;           //用户订单编号
	int32_t Qty;                  //成交数量
	int32_t TradeDate;            //成交日期
    int32_t TradeTime;            //成交时间
    STR16 AccNo;               //用户
    STR16 ProdCode;            //合约代码
    STR16 Initiator;           //下单用户
    STR16 Ref;                 //参考
    STR16 Ref2;                //参考2
    STR16 GatewayCode;         //网关
    STR40 ClOrderId;           //用户自定义指令代号
    char BuySell;              //买卖方向
    char OpenClose;            //开平仓
    tinyint Status;            //状态
	tinyint DecInPrice;        //小数位
	double OrderPrice;
	STR40 TradeRef;
	int32_t TotalQty;
	int32_t RemainingQty;
	int32_t TradedQty;
	double AvgTradedPrice;
} SPApiTrade;


#define REQMODE_UNSUBSCRIBE     0
#define REQMODE_SUBSCRIBE       1
#define REQMODE_SNAPSHOT        2

typedef struct
{
    STR16 MarketCode;
    STR40 MarketName;
} SPApiMarket;

typedef struct
{
    double Margin;
    double ContractSize;
    STR16 MarketCode;
    STR16 InstCode;
    STR40 InstName;
    STR40 InstName1; //new added
    STR40 InstName2; //new added
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

#define SP_MAX_DEPTH    20
#define SP_MAX_LAST     20
typedef struct
{
    double Bid[SP_MAX_DEPTH];     //买入价
	int32_t BidQty[SP_MAX_DEPTH];    //买入量
	int32_t BidTicket[SP_MAX_DEPTH]; //买指令数量
    double Ask[SP_MAX_DEPTH];     //卖出价
	int32_t AskQty[SP_MAX_DEPTH];    //卖出量
	int32_t AskTicket[SP_MAX_DEPTH]; //卖指令数量
    double Last[SP_MAX_LAST];     //成交价
	int32_t LastQty[SP_MAX_LAST];    //成交数量
    int32_t LastTime[SP_MAX_LAST];   //成交时间
    double Equil;                 //平衡价
    double Open;                  //开盘价
    double High;                  //最高价
    double Low;                   //最低价
    double Close;                 //收盘价
    int32_t CloseDate;               //收市日期
    double TurnoverVol;           //总成交量
    double TurnoverAmt;           //总成交额
    int32_t OpenInt;                 //未平仓
    STR16 ProdCode;               //合约代码
    STR40 ProdName;               //合约名称
    char DecInPrice;              //合约小数位
    int32_t Timestamp;
} SPApiPrice;

typedef struct
{
    double Price;              //价格
	int32_t Qty;                  //成交量
	int32_t TickerTime;           //时间
    int32_t DealSrc;              //来源
    STR16 ProdCode;            //合约代码
    char DecInPrice;           //小数位
} SPApiTicker;

typedef struct
{
    double NAV;              // 资产净值
    double BuyingPower;      // 购买力
    double CashBal;          // 现金结余
    double MarginCall;       //追收金额
    double CommodityPL;      //商品盈亏
    double LockupAmt;        //冻结金额
    double CreditLimit;      // 信貸限額
    double MaxMargin;        // 最高保証金
    double MaxLoanLimit;     // 最高借貸上限
    double TradingLimit;     // 信用交易額
    double RawMargin;        // 原始保證金
    double IMargin;          //  基本保証金
    double MMargin;           // 維持保証金
    double TodayTrans;        // 交易金額
    double LoanLimit;         // 證券可按總值
    double TotalFee;          //  費用總額
	double LoanToMR;
	double LoanToMV;
    STR16 AccName;            //  戶口名稱
    STR4 BaseCcy;             // 基本貨幣
    STR16 MarginClass;        // 保証金類別
    STR16 TradeClass;         // 交易類別
    STR16 ClientId;           // 客戶
    STR16 AEId;               //  經紀
    char AccType;             // 戶口類別
    char CtrlLevel;           //  控制級數
    char Active;              //  生效
    char MarginPeriod;         // 時段
} SPApiAccInfo;

typedef struct
{
    double CashBf;          //上日结余
    double TodayCash;       //今日存取
    double NotYetValue;     //未交收
    double Unpresented;     //未兑现
    double TodayOut;        //提取要求
    STR4 Ccy;               //货币
} SPApiAccBal;

typedef struct
{
	u_short HostType;
	char Host[100];
	u_short Port;
	bool SecureConnection;
	bool IsConnected;
	u_short LoginStatus;
} SPConnectionInfo;

typedef struct
{
    bigint BidExtOrderNo;   //Bid(买)单外部指示
    bigint AskExtOrderNo;   //Ask(沽)单外部指示
    long BidAccOrderNo;     //Bid(买)单编号
    long AskAccOrderNo;     //Ask(沽)单编号
    double BidPrice;          //Bid(买)单价格
    double AskPrice;          //Ask(沽)单价格
    long BidQty;            //Bid(买)单数量
    long AskQty;            //Ask(沽)单数量
    long SpecTime;          //预订发送时间 //箇璹祇癳丁 
   	u_long OrderOptions;    //0=默认,1=T+1
    STR16 ProdCode;         //合约代号 //腹 
    STR16 AccNo;            //用户帐号 //ノめ眀腹 
	STR40 ClOrderId;
    STR40 OrigClOrdId;
    tinyint OrderType;      //订单类型 //璹虫摸  
    tinyint ValidType;      //订单有效类型 //璹虫Τ摸 
    tinyint DecInPrice;     //合约小数位 //计 
} SPApiMMOrder;


enum LangNoEnum { ENG, TCHI, SCHI, TCHI_UNICODE, SCHI_UNICODE};


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
  virtual void OnApiAccountControlReply(long ret_code, char *ret_msg) = 0;
  virtual void OnApiLoadTradeReadyPush(long rec_no, const SPApiTrade *trade) = 0;
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
    virtual void OnApiAccountControlReply(long ret_code, char *ret_msg) final {
    };
    virtual void OnApiLoadTradeReadyPush(long rec_no, const SPApiTrade *trade) final {
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
