###############################################################################
#
# Copyright (C) 2016 Bitquant Research Laboratories (Asia) Limited
#
# Licensed under the GPLv3+ License
#
###############################################################################

from cffi import FFI
import atexit
import os
import struct
import cffi_to_py
import sys
from enum import Enum

if 8 * struct.calcsize("P") != 64:
    print("sptrader only supported for 64 bit")
    print("sptrader_api string needs to be checked for 32-bit")
    exit

location = os.path.dirname(os.path.realpath(__file__))
dll_location = os.path.join(location, "..", "dll")
ffi = FFI()
spapi_cdef = """
typedef signed long int __int64_t;
typedef unsigned long int __uint64_t;

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

typedef void (SPDLLCALL *LoginReplyAddr)(long ret_code, char *ret_msg);
typedef void (SPDLLCALL *ConnectedReplyAddr)(long host_type, long con_status);
typedef void (SPDLLCALL *ApiOrderRequestFailedAddr)(tinyint action,
    SPApiOrder *order, long err_code, char *err_msg);
typedef void (SPDLLCALL *ApiOrderReportAddr)(long rec_no, SPApiOrder *order);
typedef void (SPDLLCALL *ApiOrderBeforeSendReportAddr)(SPApiOrder *order);
typedef void (SPDLLCALL *AccountLoginReplyAddr)(char *accNo,
    long ret_code, char* ret_msg);
typedef void (SPDLLCALL *AccountLogoutReplyAddr)(long ret_code, char* ret_msg);
typedef void (SPDLLCALL *AccountInfoPushAddr)(SPApiAccInfo *acc_info);
typedef void (SPDLLCALL *AccountPositionPushAddr)(SPApiPos *pos);
typedef void (SPDLLCALL *UpdatedAccountPositionPushAddr)(SPApiPos *pos);
typedef void (SPDLLCALL *UpdatedAccountBalancePushAddr)(SPApiAccBal *acc_bal);
typedef void (SPDLLCALL *ApiTradeReportAddr)(long rec_no, SPApiTrade *trade);
typedef void (SPDLLCALL *ApiPriceUpdateAddr)(SPApiPrice *price);
typedef void (SPDLLCALL *ApiTickerUpdateAddr)(SPApiTicker *ticker);
typedef void (SPDLLCALL *PswChangeReplyAddr)(long ret_code, char *ret_msg);
typedef void (SPDLLCALL *ProductListByCodeReplyAddr)(char *inst_code,
    bool is_ready, char *ret_msg);
typedef void (SPDLLCALL *InstrumentListReplyAddr)(bool is_ready,
    char *ret_msg);
typedef void (SPDLLCALL *BusinessDateReplyAddr)(long business_date);
typedef void (SPDLLCALL *ApiMMOrderBeforeSendReportAddr)
    (SPApiMMOrder *mm_order);
typedef void (SPDLLCALL *ApiMMOrderRequestFailedAddr)(SPApiMMOrder *mm_order,
    long err_code, char *err_msg);
typedef void (SPDLLCALL *ApiQuoteRequestReceivedAddr)(char *product_code,
    char buy_sell, long qty);

void SPAPI_RegisterLoginReply(LoginReplyAddr addr);
void SPAPI_RegisterConnectingReply(ConnectedReplyAddr addr);
void SPAPI_RegisterOrderReport(ApiOrderReportAddr addr);
void SPAPI_RegisterOrderRequestFailed(ApiOrderRequestFailedAddr addr);
void SPAPI_RegisterOrderBeforeSendReport(ApiOrderBeforeSendReportAddr addr);
void SPAPI_RegisterAccountLoginReply(AccountLoginReplyAddr addr);
void SPAPI_RegisterAccountLogoutReply(AccountLogoutReplyAddr addr);
void SPAPI_RegisterAccountInfoPush(AccountInfoPushAddr addr);
void SPAPI_RegisterAccountPositionPush(AccountPositionPushAddr addr);
void
SPAPI_RegisterUpdatedAccountPositionPush(UpdatedAccountPositionPushAddr addr);
void
SPAPI_RegisterUpdatedAccountBalancePush(UpdatedAccountBalancePushAddr addr);
void SPAPI_RegisterTradeReport(ApiTradeReportAddr addr);
void SPAPI_RegisterApiPriceUpdate(ApiPriceUpdateAddr addr);
void SPAPI_RegisterTickerUpdate(ApiTickerUpdateAddr addr);
void SPAPI_RegisterPswChangeReply(PswChangeReplyAddr addr);
void SPAPI_RegisterProductListByCodeReply(ProductListByCodeReplyAddr addr);
void SPAPI_RegisterInstrumentListReply(InstrumentListReplyAddr addr);
void SPAPI_RegisterBusinessDateReply(BusinessDateReplyAddr addr);
void SPAPI_RegisterMMOrderRequestFailed(ApiMMOrderRequestFailedAddr addr);
void SPAPI_RegisterMMOrderBeforeSendReport(
    ApiMMOrderBeforeSendReportAddr addr);
void SPAPI_RegisterQuoteRequestReceivedReport(
    ApiQuoteRequestReceivedAddr addr);

int  SPAPI_Initialize();
void SPAPI_SetLoginInfo(char *host,
    int port, char *license, char *app_id, char *user_id, char *password);
int  SPAPI_Login();
int  SPAPI_GetLoginStatus(char *user_id, short host_id);
int  SPAPI_AddOrder(SPApiOrder *order);
int SPAPI_AddInactiveOrder(SPApiOrder* order);
int SPAPI_ChangeOrder(char *user_id,
    SPApiOrder* order, double org_price, long org_qty);
int SPAPI_ChangeOrderBy(char *user_id,
    char *acc_no, long accOrderNo, double org_price,
    long org_qty, double newPrice, long newQty);
int SPAPI_DeleteOrderBy(char *user_id,
    char *acc_no, long accOrderNo, char* productCode, char* clOrderId);
int SPAPI_DeleteAllOrders(char *user_id, char *acc_no);
int SPAPI_ActivateAllOrders(char *user_id, char *acc_no);
int SPAPI_InactivateAllOrders(char *user_id, char *acc_no);
int SPAPI_ActivateOrderBy(char *user_id, char *acc_no, long accOrderNo);
int SPAPI_InactivateOrderBy(char *user_id, char *acc_no, long accOrderNo);
int  SPAPI_GetOrderCount(char *user_id, char* acc_no);
int  SPAPI_GetOrderByOrderNo(char *user_id, char *acc_no,
    long int_order_no, SPApiOrder *order);
int  SPAPI_GetPosCount(char *user_id);
int  SPAPI_GetPosByProduct(char *user_id, char *prod_code, SPApiPos *pos);
void SPAPI_Uninitialize();
int SPAPI_Logout(char *user_id);
int SPAPI_AccountLogin(char *user_id, char *acc_no);
int SPAPI_AccountLogout(char *user_id, char *acc_no);
int  SPAPI_GetTradeCount(char *user_id, char *acc_no);
int SPAPI_SubscribePrice(char *user_id, char *prod_code, int mode);
int SPAPI_SubscribeTicker(char *user_id, char *prod_code, int mode);
int SPAPI_ChangePassword(char *user_id, char *old_password,
    char *new_password);
int SPAPI_GetDllVersion(char *dll_ver_no, char *dll_rel_no, char *dll_suffix);
int SPAPI_GetAccBalCount(char* user_id);
int SPAPI_GetAccBalByCurrency(char *user_id, char *ccy, SPApiAccBal *acc_bal);
int SPAPI_GetCcyRateByCcy(char *user_id, char *ccy, double *rate);
int SPAPI_GetAccInfo(char *user_id, SPApiAccInfo *acc_info);
int SPAPI_GetPriceByCode(char *user_id, char *prod_code, SPApiPrice *price);
int SPAPI_SetApiLogPath(char *path);

int SPAPI_LoadProductInfoListByCode(char *inst_code);
int SPAPI_GetProductCount();
int SPAPI_GetProductByCode(char *prod_code, SPApiProduct *prod);

int SPAPI_LoadInstrumentList();
int SPAPI_GetInstrumentCount();
int SPAPI_GetInstrumentByCode(char *inst_code, SPApiInstrument *inst);
int SPAPI_SetLanguageId(int langid);

int SPAPI_SendMarketMakingOrder(char *user_id, SPApiMMOrder *mm_order);
int SPAPI_SubscribeQuoteRequest(char *user_id, char *prod_code, int mode);
int SPAPI_SubscribeAllQuoteRequest(char *user_id, int mode);

int SPAPI_GetAllTradesByArray(char *user_id, char *acc_no,
    SPApiTrade* apiTradeList);
int SPAPI_GetOrdersByArray(char *user_id, char *acc_no,
    SPApiOrder* apiOrderList);
int SPAPI_GetAllAccBalByArray(char *user_id, SPApiAccBal* apiAccBalList);
int SPAPI_GetInstrumentByArray(SPApiInstrument* apiInstList);
int SPAPI_GetProductByArray(SPApiProduct* apiProdList);

"""
spapi = None
if os.name == "nt":
    ffi.cdef(spapi_cdef.replace("SPDLLCALL", "__stdcall"))
    ffi.dlopen(os.path.join(dll_location, "libeay32.dll"))
    ffi.dlopen(os.path.join(dll_location, "ssleay32.dll"))
    spapi = ffi.dlopen(os.path.join(dll_location, "spapidllm64.dll"))
else:
    ffi.cdef(spapi_cdef.replace("SPDLLCALL", ""))
    ffi.dlopen(os.path.join(dll_location, "libapiwrapper.so"),
               ffi.RTLD_GLOBAL | ffi.RTLD_NOW)
    spapi = ffi.dlopen(os.path.join(dll_location, "linux-shim.so"))

# Remember to convert unicode strings to byte strings otherwise
# ctypes will assume that the characters are wchars and not
# ordinary characters


class SPTrader(object):
    ffi = ffi
    api = spapi
    ffi_conv = cffi_to_py.FfiConverter(ffi)

    def __init__(self):
        self.api.SPAPI_SetLanguageId(0)
        self.api.SPAPI_Initialize()
        self.user = None
        self.acc_no = None

    def ready(self):
        if self.user is None:
            return -1
        else:
            return 0

    def register_login_reply(self, login_reply_func):
        self.api.SPAPI_RegisterLoginReply(login_reply_func)

    def register_connecting_reply(self, connected_reply_func):
        self.api.SPAPI_RegisterConnectingReply(connected_reply_func)

    def register_order_report(self, func):
        self.api.SPAPI_RegisterOrderReport(func)

    def register_order_request_failed(self, func):
        self.api.SPAPI_RegisterOrderRequestFailed(func)

    def register_order_before_send_report(self, func):
        self.api.SPAPI_RegisterOrderBeforeSendReport(func)

    def register_account_login_reply(self, func):
        self.api.SPAPI_RegisterAccountLoginReply(func)

    def register_account_logout_reply(self, func):
        self.api.SPAPI_RegisterAccountLogoutReply(func)

    def register_account_info_push(self, account_info_func):
        self.api.SPAPI_RegisterAccountInfoPush(account_info_func)

    def register_account_position_push(self, func):
        self.api.SPAPI_RegisterAccountPositionPush(func)

    def register_updated_account_position_push(self, func):
        self.api.SPAPI_RegisterUpdatedAccountPositionPush(func)

    def register_updated_account_balance_push(self, func):
        self.api.SPAPI_RegisterUpdatedAccountBalancePush(func)

    def register_trade_report(self, func):
        self.api.SPAPI_RegisterTradeReport(func)

    def register_price_update(self, func):
        self.api.SPAPI_RegisterApiPriceUpdate(func)

    def register_ticker_update(self, func):
        self.api.SPAPI_RegisterTickerUpdate(func)

    def register_psw_change_reply(self, func):
        self.api.SPAPI_RegisterPswChangeReply(func)

    def register_product_list_by_code_reply(self, func):
        self.api.SPAPI_RegisterProductListByCodeReply(func)

    def register_instrument_list_reply(self, func):
        self.api.SPAPI_RegisterInstrumentListReply(func)

    def register_business_date_reply(self, func):
        self.api.SPAPI_RegisterBusinessDateReply(func)

    def register_mm_order_request_failed(self, func):
        self.api.SPAPI_RegisterMMOrderRequestFailed(func)

    def register_mm_order_before_send_report(self, func):
        self.api.SPAPI_RegisterMMOrderBeforeSendReport(func)

    def register_quote_request_received_report(self, func):
        self.api.SPAPI_RegisterQuoteRequestReceivedReport(func)

    def load_instrument_list(self):
        return self.api.SPAPI_LoadInstrumentList()

    def set_login_info(self,
                       host,
                       port,
                       license,
                       app_id,
                       user_id,
                       password):
        self.user = user_id.encode("utf-8")
        self.acc_no = self.user
        self.api.SPAPI_SetLoginInfo(host.encode("utf-8"),
                                    port,
                                    license.encode("utf-8"),
                                    app_id.encode("utf-8"),
                                    self.user,
                                    password.encode("utf-8"))

    def login(self):
        return self.api.SPAPI_Login()

    def get_login_status(self, status_id):
        if self.user is None:
            return -1
        return self.api.SPAPI_GetLoginStatus(self.user, status_id)

    def get_instrument_count(self):
        return self.api.SPAPI_GetInstrumentCount()

    def get_instrument(self):
        count = self.get_instrument_count()
        if count <= 0:
            return []
        buffer = self.ffi.new("SPApiInstrument[%d]" % (count))
        if self.api.SPAPI_GetInstrumentByArray(buffer) == 0:
            return self.cdata_to_py(buffer)
        else:
            return []

    def get_product_count(self):
        return self.api.SPAPI_GetInstrumentCount()

    def get_product(self):
        count = self.get_product_count()
        if count <= 0:
            return []
        buffer = self.ffi.new("SPApiProduct[%d]" % (count))
        if self.api.SPAPI_GetProductByArray(buffer) == 0:
            return []
        return self.cdata_to_py(buffer)

    def get_acc_info(self):
        if self.user is None:
            return None
        buffer = self.ffi.new("SPApiAccInfo[1]")
        self.api.SPAPI_GetAccInfo(self.user, buffer)
        return self.cdata_to_py(buffer[0])

    def get_acc_bal_count(self):
        return self.api.SPAPI_GetAccBalCount(self.user)

    def get_order_count(self):
        return self.api.SPAPI_GetOrderCount(self.user, self.acc_no)

    def get_all_orders(self):
        if self.ready() != 0:
            return []
        count = self.get_order_count()
        if count <= 0:
            return []
        buffer = self.ffi.new("SPApiOrder[%d]" % (count))
        if self.api.SPAPI_GetOrdersByArray(self.user,
                                           self.acc_no,
                                           buffer) != 0:
            return []
        return self.cdata_to_py(buffer)

    def get_trade_count(self):
        return self.api.SPAPI_GetTradeCount(self.user, self.acc_no)

    def get_all_trades(self):
        if self.ready() != 0:
            return []
        count = self.get_trade_count()
        if count <= 0:
            return []
        buffer = self.ffi.new("SPApiTrade[%d]" % (count))
        if self.api.SPAPI_GetAllTradesByArray(self.user,
                                              self.acc_no,
                                              buffer) != 0:
            return []
        return self.cdata_to_py(buffer)

    def get_position_count(self):
        return SPAPI_GetPosCount(self.user)

    def get_price_by_code(self, code):
        price = self.ffi.new("SPApiPrice[1]")
        self.api.SPAPI_GetPriceByCode(self.user, code.encode("utf-8"), price)
        return self.cdata_to_py(price)

    def subscribe_price(self, prod, value):
        self.api.SPAPI_SubscribePrice(self.user,
                                      prod.encode("utf-8"), value)

    def subscribe_ticker(self, prod, value):
        self.api.SPAPI_SubscribeTicker(self.user,
                                       prod.encode("utf-8"), value)

    def logout(self):
        user = self.user
        if user is not None:
            self.user = None
            self.acc_no = None
            return self.api.SPAPI_Logout(user)

    def cdata_to_py(self, s):
        return self.ffi_conv.to_py(s)

    def fields(self, s):
        return self.ffi_conv.fields(s)

    def order_add(self, data):
        data['AccNo'] = self.acc_no
        data['Initiator'] = self.user
        buffer = self.ffi.new("SPApiOrder[1]")
        self.ffi_conv.from_py(buffer, data)
        if buffer is None:
            return -2
        return self.api.SPAPI_AddOrder(buffer)

    def order_add_inactive(self, data):
        data['AccNo'] = self.acc_no
        data['Initiator'] = self.user
        buffer = self.ffi.new("SPApiOrder[1]")
        self.ffi_conv.from_py(buffer, data)
        if buffer is None:
            return -2
        return self.api.SPAPI_AddInactiveOrder(buffer)

    def order_delete(self, data):
        accOrderNo = int(data['IntOrderNo'])
        return self.api.SPAPI_DeleteOrderBy(self.user,
                                            self.acc_no,
                                            accOrderNo,
                                            data['ProdCode'].encode("utf-8"),
                                            data['ClOrderId'].encode("utf-8"))

    def order_delete_all(self, data):
        return self.api.SPAPI_DeleteAllOrders(self.user,
                                              self.acc_no)

    def order_activate(self, data):
        accOrderNo = int(data['IntOrderNo'])
        return self.api.SPAPI_ActivateOrderBy(self.user,
                                              self.acc_no,
                                              accOrderNo)

    def order_inactivate(self, data):
        accOrderNo = int(data['IntOrderNo'])
        return self.api.SPAPI_InactivateOrderBy(self.user,
                                                self.acc_no,
                                                accOrderNo)

    def __del__(self):
        pass
#        self.api.SPAPI_Uninitialize()
